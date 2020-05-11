from .models import Question
import random


def get_random_question_id():
    questions_count = Question.objects.all().count()
    next_question_position = random.randint(0, questions_count - 1)
    return Question.objects.all()[next_question_position].id
