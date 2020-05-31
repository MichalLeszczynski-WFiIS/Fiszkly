import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from words.forms import WordsForm
from words.utils import Translator, MockTranslator

key = os.environ.get("GCP_API_KEY")
translator = Translator(key) if key else MockTranslator("Mock")


@login_required(login_url="/login")
def upload(request):
    if request.method == "POST":
        if request.FILES.get("words_file", False):
            words = [word.decode("ascii") for word in request.FILES["words_file"].readlines()]
            translated_words = translator.translate(words)
            form = WordsForm()
        else:
            form = WordsForm(request.POST)
            if form.is_valid():
                words = form.cleaned_data["field"].split()
                translated_words = translator.translate(words)
        return render(request, "upload.html", {"form": form, "translated_words": translated_words})
    else:
        form = WordsForm()
        return render(request, "upload.html", {"form": form})
