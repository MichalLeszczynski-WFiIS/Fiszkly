import os
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from words.forms import WordsForm
from words.utils import Translator, MockTranslator
from words.models import Flashcard

key = os.environ.get("GCP_API_KEY")
translator = Translator(key) if key else MockTranslator("Mock")


@login_required(login_url="/login")
def browse_words(request):
    user_words = Flashcard.objects.filter(author=request.user)
    return render(request, "browse_words.html", {"user_words": user_words})


@login_required(login_url="/login")
def upload_words(request):
    if request.method == "POST":
        if request.FILES.get("words_file", False):
            words = [
                word.decode("ascii") for word in request.FILES["words_file"].read().splitlines()
            ]
            translated_words = translator.translate(
                words, source_language="en", target_language="pl"
            )
        else:
            form = WordsForm(request.POST)
            if form.is_valid():
                words = form.cleaned_data["field"].split()
                translated_words = translator.translate(
                    words, source_language="en", target_language="pl"
                )

        request.session["translated_words"] = translated_words
        return redirect("/words/verify-words/")
    else:
        form = WordsForm()
        return render(request, "upload_words.html", {"form": form})


@login_required(login_url="/login")
def verify_words(request):
    if request.method == "POST":
        # confirm translations
        confirmed_words = request.POST.getlist("confirmed_words")
        translated_words = request.session["translated_words"]
        confirmed_translated_words = [
            word for word in translated_words if word["original"] in confirmed_words
        ]

        # get dictionary entries & user
        for word in confirmed_translated_words:
            word["author"] = request.user
            word["dictionary_entry"] = get_dictionary_entry(word["original"])

        # submit to database
        for word in confirmed_translated_words:
            save_flashcard(word)

        # return
        request.session.pop("translated_words", None)
        messages.success(request, "New words added successfully.")
        return redirect("/words/")
    else:
        # display translated words
        translated_words = request.session["translated_words"]
        return render(request, "verify_words.html", {"translated_words": translated_words})


def get_dictionary_entry(word):
    language_code = "en"
    url = f"https://api.dictionaryapi.dev/api/v1/entries/{language_code}/{word}"

    response = requests.get(url, timeout=31)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def save_flashcard(word):
    flashcard = Flashcard()

    flashcard.original_word = word["original"]
    flashcard.translated_word = word["translation"]
    flashcard.original_language = word["sl"]
    flashcard.translated_language = word["tl"]
    flashcard.dictionary_entry = word["dictionary_entry"]
    flashcard.author = word["author"]

    flashcard.save()
