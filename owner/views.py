from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage
import os
import json
from quiz.models import Question

ALLOWED_EXTENSIONS = ['json']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def upload_questions(request):
    if request.method == 'GET':
        # For GET requests, render the upload page
        return render(request, 'owner/upload_questions.html')

    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Only POST method is allowed"}, status=405)

    if 'file' not in request.FILES:
        return JsonResponse({"status": "error", "message": "No file part in the request"}, status=400)

    file = request.FILES['file']

    if file.name == '':
        return JsonResponse({"status": "error", "message": "No selected file"}, status=400)

    if not allowed_file(file.name):
        return JsonResponse({"status": "error", "message": "Invalid file type. Only JSON files are allowed"}, status=400)

    # Save uploaded file
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.name)

    with default_storage.open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Read and parse JSON file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            questions = data.get('questions', [])
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Error reading JSON: {str(e)}"})

    # Delete file after use
    if os.path.exists(file_path):
        os.remove(file_path)

    # Insert questions
    try:
        for q in questions:
            Question.objects.create(
                questions=q,  # whole question dict
                difficulty=q.get('difficulty', 'medium'),
                type=q.get('type', 'MCQ'),
                topic=q.get('topicname', 'General'),
                chapter_name='N/A'  # since your JSON doesn’t contain it
            )
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Insert error: {str(e)}"})

    return JsonResponse({"status": "success", "message": "All questions inserted successfully"})
