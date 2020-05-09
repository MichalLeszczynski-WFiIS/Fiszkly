from django.shortcuts import render,HttpResponse, redirect
# from django.views.decorators.http import require_http_methods, require_POST
import json

def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {"user": user}
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
