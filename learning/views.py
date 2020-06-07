import json
import random
from datetime import datetime

from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

from words.models import Flashcard, FlashcardGroup
from learning.models import Answer


@login_required(login_url="/login")
def index(request):
    flashcard_groups = FlashcardGroup.objects.all()
    return render(request, "index.html", {"flashcard_groups": flashcard_groups})


@login_required(login_url="/login")
def learn(request, category):
    if category == "all":
        flashcards = Flashcard.objects.all()
    elif category == "user":
        flashcards = Flashcard.objects.filter(author=request.user)
    else:
        flashcards = Flashcard.objects.filter(flashcardgroup__name=category)

    flashcard = random.choice(flashcards)

    # answers
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

    context = {"flashcard": flashcard, "category": category, "info": info}
    return render(request, "learn.html", context)


@login_required(login_url="/login")
@require_http_methods(["POST"])
def get_answer(request):
    flashcard_id = request.POST["flashcard_id"]
    flashcard = Flashcard.objects.get(id=flashcard_id)
    data = json.dumps({"answer": flashcard.translated_word})
    return HttpResponse(data)


@login_required(login_url="/login")
@require_http_methods(["POST"])
def save_answer(request):
    print(request.POST)
    is_correct = request.POST["is_correct"]
    flashcard = Flashcard.objects.get(id=request.POST["flashcard_id"])
    current_date = datetime.date(datetime.now())
    answer = Answer.objects.filter(user_id=request.user.id, flashcard=flashcard, date=current_date)
    if len(answer) == 0:
        a = Answer(
            user=request.user,
            flashcard=flashcard,
            correct_count=0,
            incorrect_count=0,
            date=current_date,
        )
        a.save()

    answer = Answer.objects.get(user=request.user, flashcard=flashcard, date=current_date)

    if is_correct == "true":
        answer.correct_count += 1
    else:
        answer.incorrect_count += 1

    answer.save()
    next_url = f"/learning/learn/{request.POST['category']}"
    data = json.dumps({"next_url": next_url})
    return HttpResponse(data)
