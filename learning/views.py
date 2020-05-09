from django.shortcuts import render,HttpResponse, redirect
# from django.views.decorators.http import require_http_methods, require_POST
import json
from .models import Question, Answers
from .forms import QuestionForm

def index(request):
    user = None
    questions = None
    if request.user.is_authenticated:
        user = request.user
        questions = Question.objects.all()
    
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            u_id = request.user.id
            q_id = questions[0].id
            is_answer_correct = form.cleaned_data['is_correct'] == 't'
            answers = Answers.objects.filter(user_id = u_id, question_id = q_id)
            if len(answers) == 0:
                a = Answers(user_id = request.user, question_id = questions[0], correct_answers = 0, incorrect_answers = 0)
                a.save()
            answer = Answers.objects.get(user_id = u_id, question_id = q_id)
            if is_answer_correct:
                answer.correct_answers = answer.correct_answers + 1
            else:    
                answer.incorrect_answers = answer.incorrect_answers + 1
            answer.save()
    
    info = Answers.objects.get(user_id = request.user.id, question_id = questions[0].id)
    context = {"user": user, "question": questions[0], "form": form, "answer_info": info}
    return render(request, "index.html", context)
    

def learning(request, id):
    #answer should be random or somethings but we need one right answer
    if request.user.is_authenticated:
        word = {
            'id':1,
            'content':'miły'
        }
        answers = {
            '1':'nice',
            '2':'awful',
            '3':'terrible'
        }
        context = {
            'word': word,
            'answers':answers
        }
        return render(request, "learning.html", context)
    else:
        return redirect("/")

def save_answer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user)
            next_word_id = 2 #here we get id from source           
            id = request.POST['id']
            if id == '1':#equal to right answer in the future
                data = json.dumps({"next_word_id": next_word_id, "is_correct": True})
                print(data)
                return HttpResponse(data)
            else:
                data = json.dumps({"next_word_id": next_word_id, "is_correct": False})
                print(data)
                return HttpResponse(data)
    else:
        return HttpResponse(status=401)



