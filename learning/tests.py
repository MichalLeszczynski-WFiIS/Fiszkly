import json
from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from words.models import Flashcard
from learning.models import Answer
from fiszkly.tests_common import LoggedInTestTemplate


class LoginSecurityTest(TestCase):
    def test_access_to_get_answer_without_login(self):
        response = self.client.post("/learning/get_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/get_answer/", status_code=301)

    def test_access_to_save_answer_without_login(self):
        response = self.client.post("/learning/save_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/save_answer/", status_code=301)


class LearningViewTest(LoggedInTestTemplate):
    def test_learning_all(self):
        response = self.client.post("/learning/learn/all", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.context["category"], "all")
        self.assertIsNotNone(response.context["flashcard"])

    def test_learning_user(self):
        response = self.client.post("/learning/learn/user", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["flashcard_groups"])

    def test_learning_group(self):
        response = self.client.post("/learning/learn/test", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["flashcard_groups"])

    def test_learning_not_existing_group(self):
        response = self.client.post("/learning/learn/test123blabla", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context["messages"])


class GetAnswerViewTest(LoggedInTestTemplate):
    def setUp(self):
        super().setUp()
        self.flashcard_id = 1
        self.current_date = datetime.date(datetime.now())

    def test_get_right_answer(self):
        data = {"flashcard_id": self.flashcard_id}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/get_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEquals(responseData["answer"], flashcard.translated_word)


class SaveAnswerViewTest(LoggedInTestTemplate):
    def setUp(self):
        super().setUp()
        self.flashcard_id = 1
        self.current_date = datetime.date(datetime.now())

    def test_save_answer_correct(self):
        data = {"flashcard_id": self.flashcard_id, "is_correct": "true", "category": "all"}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/save_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, b'{"next_url": "/learning/learn/all"}')

    def test_save_answer_false(self):
        data = {"flashcard_id": self.flashcard_id, "is_correct": "false", "category": "all"}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/save_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, b'{"next_url": "/learning/learn/all"}')
