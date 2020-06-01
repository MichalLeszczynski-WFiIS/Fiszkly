import requests
import abc
from typing import List
from collections import namedtuple
from words.models import Flashcard

WordSet = namedtuple("word_set", "original translated original_language")


class ITranslator(abc.ABC):
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.url = "https://translation.googleapis.com/language/translate/v2"

    def translate(self, words, source_language, target_language):
        """Returns a dictionary with translated words."""


class Translator(ITranslator):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def translate(self, words, source_language, target_language):
        if not words:
            return []
        words = list(set(words))

        data = {"q": words, "source": source_language, "target": target_language}
        params = {"key": self.API_KEY}

        response = requests.post(self.url, params=params, data=data)
        translated = response.json()["data"]["translations"]

        return [
            {
                "original": word,
                "translation": translation["translatedText"],
                "sl": source_language,
                "tl": target_language,
            }
            for word, translation in zip(words, translated)
        ]


class MockTranslator(ITranslator):
    def __init__(self, api_key):
        super().__init__(api_key)

    def translate(self, words, source_language, target_language):
        if not words:
            return []
        words = list(set(words))

        return [
            {"original": word, "translation": f"t_{word}", "sl": "en", "tl": "pl"} for word in words
        ]


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
