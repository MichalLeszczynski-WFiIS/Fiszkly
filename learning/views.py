from django.shortcuts import render, HttpResponse, redirect
from .question_functions import get_random_question_id

# from django.views.decorators.http import require_http_methods, require_POST
import json
from .models import Question, Answers
from .forms import QuestionForm
import random
from django.contrib.auth.decorators import login_required


def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
        questions = Question.objects.all()
    next_word_id = get_random_question_id()
    context = {"user": user, "question_id": next_word_id}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def test(request, id):
    # answer should be random or somethings but we need one right answer
    question = Question.objects.get(id=id)
    right_answer_id = random.randint(1, 3)
    question.right_answer_id = right_answer_id
    question.save()
    word = {"id": question.id, "content": question.question}
    other_aswers_ids = []
    if right_answer_id == 1:
        other_aswers_ids.extend([2, 3])
    elif right_answer_id == 2:
        other_aswers_ids.extend([1, 3])
    else:
        other_aswers_ids.extend([1, 2])
    answers = {
        right_answer_id: question.answer,
        other_aswers_ids[0]: "awful",
        other_aswers_ids[1]: "terrible",
    }
    info = []
    answer_count = (
        Answers.objects.all().filter(user_id=request.user.id, question_id=question.id).count()
    )
    if answer_count > 0:
        info = Answers.objects.get(user_id=request.user.id, question_id=question.id)
    context = {"word": word, "answers": answers, "answer_info": info}
    return render(request, "test.html", context)


@login_required
def save_answer(request):
    if request.method == "POST":
        next_word_id = get_random_question_id()
        answer_id = request.POST["answer_id"]
        word_id = request.POST["word_id"]
        question = Question.objects.get(id=word_id)
        if str(answer_id) == str(
            Question.objects.get(id=word_id).right_answer_id
        ):  # equal to right answer in the future
            data = json.dumps({"next_word_id": str(next_word_id), "is_correct": True})
            answers = Answers.objects.filter(user_id=request.user.id, question_id=question)
            if len(answers) == 0:
                a = Answers(
                    user_id=request.user,
                    question_id=question,
                    correct_answers=0,
                    incorrect_answers=0,
                )
                a.save()
            answer = Answers.objects.get(user_id=request.user.id, question_id=question)
            answer.correct_answers = answer.correct_answers + 1
            answer.save()
            return HttpResponse(data)
        else:
            data = json.dumps({"next_word_id": str(next_word_id), "is_correct": False})
            answers = Answers.objects.filter(user_id=request.user.id, question_id=question)
            if len(answers) == 0:
                a = Answers(
                    user_id=request.user,
                    question_id=question,
                    correct_answers=0,
                    incorrect_answers=0,
                )
                a.save()
            answer = Answers.objects.get(user_id=request.user.id, question_id=question)
            answer.incorrect_answers = answer.incorrect_answers + 1
            answer.save()
            return HttpResponse(data)
