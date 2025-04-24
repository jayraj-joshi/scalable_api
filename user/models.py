from django.db import models

 
from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    LANGUAGES = (
        ('hindi', 'Hindi'),
        ('english', 'English'),
    )

    CLASSES = (
        ('11', '11'),
        ('12', '12'),
        ('droper', 'Droper'),
    )

    user_id = models.BigAutoField(primary_key=True)  
    phone_number = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    language = models.CharField(choices=LANGUAGES, max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    academic_class = models.CharField(choices=CLASSES, max_length=10)

    def __str__(self):
        return self.name

