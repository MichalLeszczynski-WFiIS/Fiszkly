from django.contrib import admin
from django import forms
from .models import Flashcard, Answer


class FlashcardAdmin(admin.ModelAdmin):
    list_display = ["original", "translated", "original_language"]


admin.site.register(Flashcard, FlashcardAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["correct_count", "incorrect_count"]


admin.site.register(Answer, AnswerAdmin)
