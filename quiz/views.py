from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quiz.models import Question, questions_user
from user.models import UserModel
from django.db import models
import random
import threading

from quiz.models import Question

from django.db import models
from quiz.models import Question



def generate_question(topic_name):
    # Placeholder for actual logic
    print(f"Generating more questions for topic: {topic_name}")


def background_task(user, question_ids, topics):
    # Increment attempted_by for each question
    for q_id in question_ids:
        Question.objects.filter(question_id=q_id).update(attempted_by=models.F('attempted_by') + 1)

    # print(f"Attempt count incremented for user {user} on questions {question_ids} on topic(s) {topics}")

    # If topics are provided, split and process each one
    if topics:
        topic_list = [t.strip() for t in topics.split(',')]
        for topic in topic_list:
            total = Question.objects.filter(topic=topic).count()
            attempted = Question.objects.filter(topic=topic, attempted_by__gte=1).count()
            ratio = f"{attempted}/{total}" if total > 0 else "0/0"
            print(f"[Topic: {topic}] Attempted ratio: {ratio}")
    else:
        print("No topic provided, skipping topic-wise ratio calculation.")

    # Increment attempted_by count for each question
    for q_id in question_ids:
        Question.objects.filter(question_id=q_id).update(attempted_by=models.F('attempted_by') + 1)

    # Handle multiple topics (comma-separated string)
    if topics:
        topic_list = [t.strip() for t in topics.split(',')]
        topic_filter = Question.objects.filter(topic__in=topic_list)
    else:
        topic_filter = Question.objects.all()  # Fallback to all questions if no topics provided

    total_questions = topic_filter.count()
    attempted_questions = topic_filter.filter(attempted_by__gte=1).count()

    ratio = f"{attempted_questions}/{total_questions}" if total_questions > 0 else "0/0"
    high_ratio_topics = []  # ✅ collect topics with ratio > 0.8

    if topics:
        topic_list = [t.strip() for t in topics.split(',')]
        for topic in topic_list:
            total = Question.objects.filter(topic=topic).count()
            attempted = Question.objects.filter(topic=topic, attempted_by__gte=1).count()

            ratio = attempted / total if total > 0 else 0
            print(f"[Topic: {topic}] Attempted ratio: {attempted}/{total} = {ratio:.2f}")

            if ratio >= 0.8:
                high_ratio_topics.append(topic)
                generate_question(topic)
    else:
        print("No topic provided, skipping topic-wise ratio calculation.")
    generate_question(high_ratio_topics)    
    print(high_ratio_topics)
    print(f"Attempt count incremented for user {user} on questions {question_ids} on topic(s) {topics}")
    # print(f"Attempted ratio for given topic(s): {ratio}")



class Generate_questions(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        chapters = request.GET.get('chapter_name')
        topics = request.GET.get('topic')
        q_type = request.GET.get('type')
        num_questions = request.GET.get('num_questions')

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserModel.objects.get(user_id=user_id)
        except UserModel.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        questions = Question.objects.all()

        if chapters:
            chapter_list = [c.strip() for c in chapters.split(',')]
            questions = questions.filter(chapter_name__in=chapter_list)

        if topics:
            topic_list = [t.strip() for t in topics.split(',')]
            questions = questions.filter(topic__in=topic_list)

        if q_type:
            questions = questions.filter(type__iexact=q_type)

        attempted_question_ids = questions_user.objects.filter(user=user).values_list('question_id', flat=True)
        questions = questions.exclude(question_id__in=attempted_question_ids)

        if num_questions:
            try:
                num_questions = int(num_questions)
                questions = list(questions)
                random.shuffle(questions)
                questions = questions[:num_questions]
            except ValueError:
                return Response({"error": "num_questions must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Send full JSON stored in `questions` field along with other metadata
        serialized_questions = [
            {
                "id": q.question_id,
                "question_data": q.questions,  # Full question JSON
                "type": q.type,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "chapter_name": q.chapter_name
            }
            for q in questions
        ]

        question_ids = [q.question_id for q in questions]
        threading.Thread(target=background_task, args=(user_id, question_ids,topics)).start()

        return Response({"questions": serialized_questions}, status=status.HTTP_200_OK)
