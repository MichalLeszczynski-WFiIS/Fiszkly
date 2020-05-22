import requests
import os
from collections import namedtuple

word_set = namedtuple('word_set', 'original translated original_language')

class Translator:
    def __init__(self):
        self.API_KEY = os.environ.get("GCP_API_KEY")
        self.url = "https://translation.googleapis.com/language/translate/v2"

    def translate(self, words):

        data = {'q': words, 'target': 'pl'}
        params = {'key': self.API_KEY}
        
        response = requests.post(self.url, params=params, data=data)
        translated = response.json()["data"]["translations"]


        for word, translation in zip(words, translated): 
            print(f"{word} \t<-->\t {translation['translatedText']}")

        return [word_set(word, translation['translatedText'], "pl") for word, translation in zip(words, translated)]
