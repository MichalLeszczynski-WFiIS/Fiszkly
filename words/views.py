import os
import requests

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from words.forms import WordsForm
from words.utils import (
    Translator,
    MockTranslator,
    get_dictionary_entry,
    save_flashcard,
    save_categorized_flashcard,
)
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

    return render(
        request,
        "browse_groups.html",
        {"flashcard_groups": flashcard_groups, "user_count": user_count, "all_count": all_count},
    )


@login_required(login_url="/login")
def browse_words(request, category="all"):
    if category == "all":
        words = Flashcard.objects.all()
    elif category == "user":
        words = Flashcard.objects.filter(author=request.user)
    else:
        words = Flashcard.objects.filter(flashcardgroup__name=category)

    return render(request, "browse_words.html", {"words": words, "category": category})


@login_required(login_url="/login")
def upload_words(request):
    if request.method == "POST":
        if request.FILES.get("words_file", False):
            words = [
                word.decode("ascii") for word in request.FILES["words_file"].read().splitlines()
            ]
            source_language = request.POST.get("language")
        else:
            form = WordsForm(request.POST)
            if form.is_valid():
                words = form.cleaned_data["field"].split()
                source_language = form.cleaned_data["language"]
                print(f"\n\n{source_language}\n\n")

        target_language = "en" if source_language == "pl" else "pl"
        translated_words = translator.translate(
            words, source_language=source_language, target_language=target_language
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

        # add to categories
        if request.POST.get("category", 0):
            category = FlashcardGroup(name=request.POST["category"])
            category.save()
            categorized = True
        else:
            categorized = False

        # submit to database
        for word in confirmed_translated_words:
            if categorized:
                save_categorized_flashcard(word, category)
            else:
                save_flashcard(word)

        # return
        request.session.pop("translated_words", None)
        messages.success(request, "New words added successfully.")
        return redirect("/words/")
    else:
        # display translated words
        translated_words = request.session["translated_words"]
        return render(request, "verify_words.html", {"translated_words": translated_words})
