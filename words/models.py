from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Flashcard(models.Model):
    original_word = models.CharField(max_length=50)
    translated_word = models.CharField(max_length=100)
    original_language = models.CharField(max_length=2)
    translated_language = models.CharField(max_length=2)
    dictionary_entry = JSONField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

class FlashcardGroup(models.Model):
    name = models.CharField(max_length=50)
    flashcards = models.ManyToManyField(Flashcard)
