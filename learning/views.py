import json
import random

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from learning.models import Flashcard, Answer


def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    next_flashcard = random.choice(Flashcard.objects.all())
    context = {"user": user, "flashcard": next_flashcard}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def check_user_skills(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    correct_answers = (
        Answer.objects.all()
        .filter(user=request.user)
        .aggregate(Sum("correct_count"))["correct_count__sum"]
    )
    incorrect_answers = (
        Answer.objects.all()
        .filter(user=request.user)
        .aggregate(Sum("incorrect_count"))["incorrect_count__sum"]
    )
    correct_answers = 0 if correct_answers == None else correct_answers
    incorrect_answers = 0 if incorrect_answers == None else incorrect_answers
    info = {"correct_answers": correct_answers, "incorrect_answers": incorrect_answers}
    context = {"flashcard": flashcard, "info": info}
    return render(request, "check_user_skills.html", context)


@login_required(login_url="/login")
@require_http_methods(["POST"])
def get_answer(request):
    flashcard_id = request.POST["flashcard_id"]
    flashcard = Flashcard.objects.get(id=flashcard_id)
    data = json.dumps({"answer": flashcard.translated})
    return HttpResponse(data)


@login_required(login_url="/login")
@require_http_methods(["POST"])
def save_answer(request):
    is_correct = request.POST["is_correct"]
    flashcard = Flashcard.objects.get(id=request.POST["flashcard_id"])
    answer = Answer.objects.filter(user_id=request.user.id, flashcard=flashcard)
    if len(answer) == 0:
        a = Answer(
            user=request.user, flashcard=flashcard, correct_count=0, incorrect_count=0
        )
        a.save()
    answer = Answer.objects.get(user=request.user, flashcard=flashcard)

    if is_correct == "true":
        answer.correct_count += 1

    else:
        answer.incorrect_count += 1

    answer.save()

    next_flashcard = random.choice(Flashcard.objects.all())
    data = json.dumps(
        {"next_url": "/learning/check_user_skills/{}".format(next_flashcard.id)}
    )
    return HttpResponse(data)
