from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import CreateUserForm

from learning.models import Answer, Flashcard
from django.db.models import Sum, Q
from django.forms.models import model_to_dict

# Create your views here.


def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for user {}".format(user))
            return redirect("/login")

    context = {"form": form}
    return render(request, "register.html", context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username or password is incorect.")

    context = {}
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login")
def profilePage(request):
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

    answers = Answer.objects.filter(Q(user=request.user.id) & (~Q(correct_count = 0) | ~Q(incorrect_count = 0)))
    
    # for p in Answer.objects.raw('SELECT * FROM learning_answer l WHERE user=%s AND (correct_count != 0 OR incorrect_count != 0)', [request.user]):
    #     print(p)
    # for p in Answer.objects.raw(''' SELECT * FROM learning_answer 
    #                                 JOIN learning_flashcard using (flashcard_id, id)
    #                                 WHERE user_id = %s AND (correct_count != 0 OR incorrect_count != 0)''', [request.user.id]):
    #     print(model_to_dict(p))
    # a = Answer.objects.raw('SELECT * FROM learning_answer l WHERE user=%s AND (correct_count != 0 OR incorrect_count != 0)', [request.user])
    # a = Answer.objects.raw('SELECT * FROM learning_answer')
    # print(a)

    answers = list(answers)
    answers.sort(key=lambda answer: answer.correct_count / (answer.correct_count + answer.incorrect_count))
    if len(answers) > 3:
        answers = answers[:3]
    
    flashcards, flashcards_answers = [], []

    for el in answers:
        obj = Flashcard.objects.get(id=el.flashcard.id)
        flashcards.append(model_to_dict(obj))
        flashcards_answers.append(model_to_dict(el))
    
    flashcards_info = []
    for i in range(len(flashcards)):
        correct = flashcards_answers[i]['correct_count']
        incorrect = flashcards_answers[i]['incorrect_count']
        
        flashcards_info.append({
            'original': flashcards[i]['original'],
            'translated': flashcards[i]['translated'],
            'effectiveness': correct / (correct + incorrect) * 100

        })
        
    context = {
        'user': {
            'username': request.user.username,
            'email': request.user.email, 
        },
        'answers': {
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers
        },
        'flashcards': flashcards_info,
    }


    return render(request, "profile.html", context)
