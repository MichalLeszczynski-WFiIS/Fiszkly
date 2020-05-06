from django.shortcuts import render
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
