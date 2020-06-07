import os
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from words.forms import WordsForm
from words.utils import Translator, MockTranslator, get_dictionary_entry, save_flashcard
from words.models import Flashcard, FlashcardGroup

key = os.environ.get("GCP_API_KEY")
translator = Translator(key) if key else MockTranslator("Mock")


@login_required(login_url="/login")
def browse_groups(request):
    flashcard_groups = FlashcardGroup.objects.all()
    for group in flashcard_groups:
        group.count = group.flashcards.count()

    user_count = Flashcard.objects.filter(author=request.user).count()
    all_count = Flashcard.objects.all().count()
    
    return render(request, "browse_groups.html", {"flashcard_groups": flashcard_groups, "user_count": user_count, "all_count": all_count})

@login_required(login_url="/login")
def browse_words(request, filter="all"):
    if filter == "all":
        words = Flashcard.objects.all()
    elif filter == "user":
        words = Flashcard.objects.filter(author=request.user)
    else:
        words = Flashcard.objects.filter(flashcardgroup__name=filter)

    return render(request, "browse_words.html", {"words": words, "filter": filter})


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
