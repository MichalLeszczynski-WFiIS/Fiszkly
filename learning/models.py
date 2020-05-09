from django.db import models
import uuid
from django.conf import settings

# Create your models here.

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

class Answers(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()
