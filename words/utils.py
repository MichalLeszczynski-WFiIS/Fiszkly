import requests
import abc
from typing import List
from collections import namedtuple

WordSet = namedtuple("word_set", "original translated original_language")


class ITranslator(abc.ABC):
    def __init__(self, api_key):
        self.API_KEY = api_key
        self.url = "https://translation.googleapis.com/language/translate/v2"

    def translate(self, words: List[str]) -> List[WordSet]:
        """Returns words with their translations and original languages detected as WordSet."""

    def get_translations(self, words: List[str], target_language: str) -> List[WordSet]:
        """Returns words translated to specified language (pl or eng) as WordSet."""

    def detect(self, words: List[str]) -> List[WordSet]:
        """Returns languages detected for given word list."""


class Translator(ITranslator):
    def __init__(self, api_key: str):
        super().__init__(api_key)

    def translate(self, words: List[str]) -> List[WordSet]:
        detections = self.detect(words)
        en_words = [
            word.original for word in detections if word.original_language == "en"
        ]
        pl_words = [
            word.original for word in detections if word.original_language == "pl"
        ]
        return self.get_translations(en_words, "pl") + self.get_translations(
            pl_words, "en"
        )

    def get_translations(self, words: List[str], target_language: str) -> List[WordSet]:
        if not words:
            return []

        data = {"q": words, "target": target_language}
        params = {"key": self.API_KEY}

        response = requests.post(self.url, params=params, data=data)
        translated = response.json()["data"]["translations"]

        return [
            WordSet(
                word,
                translation["translatedText"],
                "pl" if target_language == "en" else "en",
            )
            for word, translation in zip(words, translated)
        ]

    def detect(self, words: List[str]) -> List[WordSet]:
        if not words:
            return []
        data = {"q": words}
        params = {"key": self.API_KEY}

        response = requests.post(f"{self.url}/detect", params=params, data=data)
        detected = response.json()["data"]["detections"]

        return [
            WordSet(word, "", "en" if detection[0]["language"] == "en" else "pl")
            for word, detection in zip(words, detected)
        ]


class MockTranslator(ITranslator):
    def __init__(self, api_key):
        super().__init__(api_key)

    def translate(self, words: List[str]) -> List[WordSet]:
        return [WordSet(word, f"<mock> {word}", "<mock>") for word in words]

    def get_translations(self, words: List[str], target_language: str) -> List[WordSet]:
        pass

    def detect(self, words: List[str]) -> List[WordSet]:
        pass
