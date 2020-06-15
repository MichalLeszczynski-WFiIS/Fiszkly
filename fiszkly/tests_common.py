from django.test import TestCase
from django.contrib.auth.models import User
from words.models import Flashcard
from learning.models import Answer
from words.utils import get_dictionary_entry


class UserCreatedTestTemplate(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"),
            password=self.credentials.get("password"),
        )


class LoggedInTestTemplate(UserCreatedTestTemplate):
    def setUp(self):
        super().setUp()
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)


class HaveFlashcardTestTemplate(LoggedInTestTemplate):
    def setUp(self):
        super().setUp()
        Flashcard.objects.create(
            original_word="encouragement",
            translated_word="zachęta",
            original_language="en",
            translated_language="pl",
            dictionary_entry=get_dictionary_entry("encouragement"),
        )


class HaveAnswerTestTemplate(HaveFlashcardTestTemplate):
    def setUp(self):
        super().setUp()
        Answer.objects.create(
            incorrect_count=6,
            correct_count=8,
            flashcard=Flashcard.objects.get(id="1"),
            user=User.objects.get(username="testuser"),
        )
