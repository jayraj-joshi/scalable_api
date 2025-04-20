from django.db import models
 
from user.models import UserModel
class Question(models.Model):
    DIFFICULTY = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    question_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='questions')
    questions = models.JSONField()  
    difficulty = models.CharField(choices=DIFFICULTY, max_length=10)
    attempted_by = models.PositiveIntegerField(default=0)   
    type = models.CharField(max_length=50)   
    topic = models.CharField(max_length=100)   

    def __str__(self):
        return f"{self.topic} - {self.difficulty}"


class Answer(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    given_answer = models.TextField()
    is_correct = models.BooleanField()
     

    def __str__(self):
        return f"{self.user.name} - Q{self.question.question_id} - {'Correct' if self.is_correct else 'Wrong'}"

