from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Question)
admin.site.register(questions_user)