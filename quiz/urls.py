from django.urls import path
from .views import GetFilteredQuestionsAPIView

urlpatterns = [
    path('get-questions/', GetFilteredQuestionsAPIView.as_view(), name='get-questions'),
]
