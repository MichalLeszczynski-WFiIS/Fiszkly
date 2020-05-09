from django.shortcuts import render,HttpResponse, redirect
# from django.views.decorators.http import require_http_methods, require_POST
import json
from .models import Question, Answers
from .forms import QuestionForm
import random 
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
        question = Question.objects.get(id=id)
        right_answer_id = random.randint(1,3)
        question.right_answer_id = right_answer_id
        question.save()
        print(question.question)
        print("Right answer id - {}".format(right_answer_id))
        word = {
            'id':question.id,
            'content':question.question
        }
        other_aswers_ids = []
        if right_answer_id == 1:
            other_aswers_ids.extend([2, 3])
        elif right_answer_id == 2:
            other_aswers_ids.extend([1, 3])
        else:
            other_aswers_ids.extend([1, 2])
        answers = {
            right_answer_id: question.answer,
            other_aswers_ids[0]:'awful',
            other_aswers_ids[1]:'terrible'
        }
        info = []
        answer_count = Answers.objects.all().filter(user_id = request.user.id, question_id = question.id).count()
        if answer_count > 0:
            info = Answers.objects.get(user_id = request.user.id, question_id = question.id)
        context = {
            'word': word,
            'answers':answers,
            'answer_info': info
        }
        return render(request, "learning.html", context)
    else:
        return redirect("/")

def save_answer(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user)
            questions_count = Question.objects.all().count()
            next_question_position = random.randint(0, questions_count - 1) 
            next_word_id = Question.objects.all()[next_question_position].id    
            print(next_word_id)
            answer_id = request.POST['answer_id']
            word_id = request.POST['word_id']
            print(word_id)
            question = Question.objects.get(id=word_id)
            print(question.right_answer_id)
            if str(answer_id) == str(Question.objects.get(id=word_id).right_answer_id):#equal to right answer in the future
                data = json.dumps({"next_word_id": str(next_word_id), "is_correct": True})
                answers = Answers.objects.filter(user_id = request.user.id, question_id = question)
                if len(answers) == 0:
                    a = Answers(user_id = request.user, question_id = question, correct_answers = 0, incorrect_answers = 0)
                    a.save()
                answer = Answers.objects.get(user_id = request.user.id, question_id = question)
                answer.correct_answers = answer.correct_answers + 1
                answer.save()
                print(data)
                return HttpResponse(data)
            else:
                data = json.dumps({"next_word_id": str(next_word_id), "is_correct": False})
                answers = Answers.objects.filter(user_id = request.user.id, question_id = question)
                if len(answers) == 0:
                    a = Answers(user_id = request.user, question_id = question, correct_answers = 0, incorrect_answers = 0)
                    a.save()
                answer = Answers.objects.get(user_id = request.user.id, question_id = question)
                answer.incorrect_answers = answer.incorrect_answers + 1
                answer.save()
                print(data)
                return HttpResponse(data)
    else:
        return HttpResponse(status=401)



