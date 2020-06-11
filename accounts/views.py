import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Sum, Count, Q
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from accounts.forms import CreateUserForm
from learning.models import Answer
from words.models import Flashcard


def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for user {user}")
            return redirect("/login")

    context = {"form": form}
    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/learning")
        else:
            messages.info(request, "Username or password is incorect.")

    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("/login")


@login_required(login_url="/login")
def profile_page(request):
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

    result = (
        Answer.objects.values("date")
        .filter(user=request.user)
        .order_by("date")
        .annotate(correct=Sum("correct_count"))
        .annotate(incorrect=Sum("incorrect_count"))
    )
    result = list(result)
    data = {"dates": [], "correct": [], "incorrect": [], "all": [], "percentage": []}
    correct_sum, incorrect_sum = 0, 0
    for el in result:
        correct_sum += el["correct"]
        incorrect_sum += el["incorrect"]
        data["dates"].append(str(el["date"]))
        data["correct"].append(correct_sum)
        data["incorrect"].append(incorrect_sum)
        data["all"].append(correct_sum + incorrect_sum)
        data["percentage"].append(correct_sum / (correct_sum + incorrect_sum) * 100)

    answers = (
        Answer.objects.values("flashcard_id")
        .filter(Q(user=request.user.id) & (~Q(correct_count=0) | ~Q(incorrect_count=0)))
        .annotate(correct=Sum("correct_count"))
        .annotate(incorrect=Sum("incorrect_count"))
    )
    answers = list(answers)
    answers.sort(key=lambda answer: answer["correct"] / (answer["correct"] + answer["incorrect"]))
    answers = answers[: len(answers)]

    flashcards, flashcards_answers = [], []

    for el in answers:
        obj = Flashcard.objects.get(id=el["flashcard_id"])
        flashcards.append(model_to_dict(obj))
        flashcards_answers.append(el)

    flashcards_info = []
    for i in range(len(flashcards)):
        correct = flashcards_answers[i]["correct"]
        incorrect = flashcards_answers[i]["incorrect"]

        flashcards_info.append(
            {
                "original": flashcards[i]["original_word"],
                "translated": flashcards[i]["translated_word"],
                "effectiveness": round(correct / (correct + incorrect) * 100, 2),
            }
        )

    context = {
        "user": {
            "username": request.user.username,
            "is_authenticated": request.user.is_authenticated,
            "email": request.user.email,
        },
        "answers": {"correct_answers": correct_answers, "incorrect_answers": incorrect_answers},
        "flashcards": flashcards_info,
        "statistics": json.dumps(data),
    }

    return render(request, "profile.html", context)


@login_required(login_url="/login")
def statistics_page(request):
    ranking = (
        Answer.objects.values("user__username", "user_id")
        .annotate(correct=Sum("correct_count"))
        .annotate(incorrect=Sum("incorrect_count"))
        .order_by("-correct")
    )
    ranking = list(ranking)

    ranking_words_added = (
        Flashcard.objects.values("author__username", "author__id")
        .annotate(flashcards_added=Count("author"))
        .order_by("-flashcards_added")
    )

    ranking_words_added = list(ranking_words_added)

    logged_user_position = None
    for i, el in enumerate(ranking):
        el["position"] = i + 1
        if el["user_id"] == request.user.id:
            logged_user_position = i + 1

    ranking_words_added.remove(
        {"author__username": None, "author__id": None, "flashcards_added": 0}
    )

    logged_user_position_words = None
    for i, el in enumerate(ranking_words_added):
        el["position"] = i + 1
        if el["author__id"] == request.user.id:
            logged_user_position_words = i + 1

    print(logged_user_position_words)

    context = {
        "ranking": json.dumps(ranking),
        "words_ranking": json.dumps(ranking_words_added),
        "position": logged_user_position if logged_user_position else 0,
        "words_position": logged_user_position_words if logged_user_position_words else 0,
    }
    return render(request, "statistics.html", context)
