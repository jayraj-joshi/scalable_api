from django.urls import path
from .views import Generate_questions

urlpatterns = [
    path('get-questions/', Generate_questions.as_view(), name='get-questions'),
]
