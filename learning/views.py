from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .flashcard_functions import get_random_flashcard
import json
from .models import Flashcard, Answer
import random
from django.contrib.auth.decorators import login_required


def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    next_flashcard = get_random_flashcard()
    context = {"user": user, "flashcard": next_flashcard}
    return render(request, "index.html", context)


@login_required(login_url="/login")
def test(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    info = []
    answer_count = Answer.objects.all().filter(user=request.user, flashcard=flashcard).count()
    if answer_count > 0:
        info = Answer.objects.get(user=request.user, flashcard=flashcard)
    context = {"flashcard": flashcard}
    return render(request, "test.html", context)


@login_required
def get_answer(request):
    if request.method == "POST":
        flashcard_id = request.POST["flashcard_id"]
        flashcard = Flashcard.objects.get(id=flashcard_id)
        data = json.dumps({"answer": flashcard.translated})
        return HttpResponse(data)


def save_answer(request):
    if request.method == "POST":
        is_correct = request.POST["is_correct"]
        flashcard = Flashcard.objects.get(id=request.POST["flashcard_id"])
        answer = Answer.objects.filter(user_id=request.user.id, flashcard=flashcard)
        if len(answer) == 0:
            a = Answer(user=request.user, flashcard=flashcard, correct_count=0, incorrect_count=0,)
            a.save()
        answer = Answer.objects.get(user=request.user, flashcard=flashcard)
        if is_correct:
            answer.correct_count += 1
            answer.save()
        else:
            answer.incorrect_count += 1
            answer.save()
        print(answer.correct_count)
        next_flashcard = get_random_flashcard()
        data = json.dumps({"next_url": "/learning/test/{}".format(next_flashcard.id)})
        return HttpResponse(data)
