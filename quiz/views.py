from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from quiz.models import Question, questions_user
from user.models import UserModel
import random

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

        # Start with all questions matching filters
        questions = Question.objects.all()

        if chapters:
            chapter_list = [c.strip() for c in chapters.split(',')]
            questions = questions.filter(chapter_name__in=chapter_list)

        if topics:
            topic_list = [t.strip() for t in topics.split(',')]
            questions = questions.filter(topic__in=topic_list)

        if q_type:
            questions = questions.filter(type__iexact=q_type)

        # Exclude questions already attempted by the user
        attempted_question_ids = questions_user.objects.filter(user=user).values_list('question_id', flat=True)
        questions = questions.exclude(question_id__in=attempted_question_ids)

        # Limit to the number of questions specified
        if num_questions:
            try:
                num_questions = int(num_questions)
                questions = list(questions)
                random.shuffle(questions)  # Shuffle to randomize order
                questions = questions[:num_questions]
            except ValueError:
                return Response({"error": "num_questions must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the questions
        serialized_questions = [
            {
                "id": q.question_id,
                "question": q.questions.get("question", ""),
                "type": q.type,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "chapter_name": q.chapter_name
            }
            for q in questions
        ]

        return Response({"questions": serialized_questions}, status=status.HTTP_200_OK)
