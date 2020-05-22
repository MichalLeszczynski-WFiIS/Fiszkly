import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from words.words_utils import Translator, MockTranslator
from words.forms import WordsForm

key = os.environ.get("GCP_API_KEY")
translator = Translator(key) if key else MockTranslator("Mock")


@login_required
def upload(request):
    if request.method == "POST" and request.FILES["words_file"]:
        words = [word.decode("ascii") for word in request.FILES["words_file"].readlines()]
        translated_words = translator.translate(words)
        return render(request, "upload.html", {"translated_words": translated_words})
    return render(request, "upload.html")


@login_required
def insert(request):
    if request.method == "POST":
        form = WordsForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data["field"].split()
            translated_words = translator.translate(words)
            print(words)
            return render(
                request, "input.html", {"form": form, "translated_words": translated_words}
            )
    else:
        form = WordsForm()
        return render(request, "input.html", {"form": form})
