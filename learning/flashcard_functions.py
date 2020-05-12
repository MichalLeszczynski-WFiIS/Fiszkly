from .models import Flashcard
import random


def get_random_flashcard():
    questions_count = Flashcard.objects.all().count()
    next_question_position = random.randint(0, questions_count - 1)
    return Flashcard.objects.all()[next_question_position]
