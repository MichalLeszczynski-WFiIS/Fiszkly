from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Answer(models.Model):
    correct_count = models.IntegerField()
    incorrect_count = models.IntegerField()
    date = models.DateField(blank=True, null=True)
    flashcard = models.ForeignKey(
        "words.Flashcard", on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers"
    )
