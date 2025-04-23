from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_questions, name='upload_questions'),
]
