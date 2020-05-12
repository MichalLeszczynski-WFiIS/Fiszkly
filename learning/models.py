from django.db import models
import uuid
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Flashcard(models.Model):

    original = models.CharField(max_length=30)
    translated = ArrayField(models.CharField(max_length=100))
    original_language = models.CharField(max_length=2)


class Answer(models.Model):

    correct_count = models.IntegerField()
    incorrect_count = models.IntegerField()

    flashcard = models.ForeignKey(
        "learning.Flashcard", on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers"
    )
