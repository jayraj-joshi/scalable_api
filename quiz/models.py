from django.db import models
 
from user.models import UserModel
class Question(models.Model):
    DIFFICULTY = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    question_id = models.BigAutoField(primary_key=True)
    questions = models.JSONField()  
    difficulty = models.CharField(choices=DIFFICULTY, max_length=10,null=True)
    attempted_by = models.PositiveIntegerField(default=0)   
    type = models.CharField(max_length=50)   
    topic = models.CharField(max_length=100)   
    chapter_name = models.CharField(max_length=100,null=True)   

    def __str__(self):
        return f"{self.topic} - {self.difficulty}"
 

class questions_user(models.Model):
    user = models.ForeignKey(UserModel, to_field='user_id', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    given_answer = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.name} - Q{self.question.question_id} - {'Correct' if self.is_correct else 'Wrong'}"




