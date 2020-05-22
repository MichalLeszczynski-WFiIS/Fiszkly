from django.shortcuts import render
from words.words_utils import Translator, MockTranslator
from django.contrib.auth.decorators import login_required

import os

key = os.environ.get("GCP_API_KEY")
if key:
    translator = Translator(key)
else:
    translator = MockTranslator("Mock")
    


@login_required
def upload(request):
    if request.method == "POST" and request.FILES["words_file"]:
        words = [word.decode("ascii") for word in request.FILES["words_file"].readlines()]
        translated_words = translator.translate(words)
        return render(request, "upload.html", {"translated_words": translated_words})
    return render(request, "upload.html")
