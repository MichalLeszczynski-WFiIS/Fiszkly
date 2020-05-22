from django.shortcuts import render
from words.words_utils import Translator
from django.contrib.auth.decorators import login_required

translator = Translator()

@login_required
def upload(request):
    if request.method == "POST" and request.FILES["words_file"]:
        words = [word.decode('ascii') for word in request.FILES["words_file"].readlines()]
        print(words)
        translated_words = translator.translate(words)
        return render(request, "upload.html", {
            "translated_words": translated_words
        })
    return render(request, "upload.html") 