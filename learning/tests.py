import json
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from words.models import Flashcard
from learning.models import Answer


class LoginSecurityTest(TestCase):
    def test_access_to_get_answer_without_login(self):
        response = self.client.post("/learning/get_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/get_answer/", status_code=301)

    def test_access_to_save_answer_without_login(self):
        response = self.client.post("/learning/save_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/save_answer/", status_code=301)

class LearningTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        self.user = User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        self.flashcard_id = 1
        logged_in = self.client.login(**self.credentials)
        self.current_date = datetime.date(datetime.now())

    def test_get_right_answer(self):
        data = {"flashcard_id": self.flashcard_id}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/get_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEquals(responseData["answer"], flashcard.translated_word)
