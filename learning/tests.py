from django.test import TestCase
from django.contrib.auth.models import User
from .models import Flashcard, Answer
import json

# Create your tests here.


class LoginSecurityTest(TestCase):
    def test_access_to_check_user_skills_without_login(self):
        response = self.client.get("/learning/check_user_skills/1", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/check_user_skills/1")

    def test_access_to_get_answer_without_login(self):
        response = self.client.post("/learning/get_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/get_answer/", status_code=301)

    def test_access_to_save_answer_without_login(self):
        response = self.client.post("/learning/save_answer", follow=True)
        self.assertRedirects(response, "/login/?next=/learning/save_answer/", status_code=301)

    def test_show_user_when_no_authenticated(self):
        response = self.client.get("/learning/", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context["user"])


class AvailabilityTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        logged_in = self.client.login(**self.credentials)

    def test_access_to_check_user_skills_with_login(self):
        response = self.client.post("/learning/check_user_skills/1", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_show_user_when_authenticated(self):
        response = self.client.get("/learning/", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"])


class LearningTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        self.user = User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        self.flashcard_id = 1
        logged_in = self.client.login(**self.credentials)

    def test_create_new_answer_if_not_exists(self):
        data = {"is_correct": "true", "flashcard_id": self.flashcard_id}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/save_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Answer.objects.filter(user_id=self.user.id, flashcard=flashcard).exists())

    def save_user_answer(self, answer):
        Answer.objects.create(
            correct_count=0,
            incorrect_count=0,
            flashcard=Flashcard.objects.get(id=1),
            user=self.user,
        )
        data = {"is_correct": answer, "flashcard_id": self.flashcard_id}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        if answer == "true":
            answer_count_before = Answer.objects.get(
                user_id=self.user.id, flashcard=flashcard
            ).correct_count
        elif answer == "false":
            answer_count_before = Answer.objects.get(
                user_id=self.user.id, flashcard=flashcard
            ).incorrect_count
        response = self.client.post("/learning/save_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        if answer == "true":
            answer_count_after = Answer.objects.get(
                user_id=self.user.id, flashcard=flashcard
            ).correct_count
        elif answer == "false":
            answer_count_after = Answer.objects.get(
                user_id=self.user.id, flashcard=flashcard
            ).incorrect_count
        self.assertEquals(answer_count_before + 1, answer_count_after)

    def test_get_right_answer(self):
        data = {"flashcard_id": self.flashcard_id}
        flashcard = Flashcard.objects.get(id=self.flashcard_id)
        response = self.client.post("/learning/get_answer/", data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        responseData = json.loads(response.content)
        self.assertEquals(responseData["answer"], flashcard.translated)

    def test_save_correct_answer(self):
        self.save_user_answer("true")

    def test_save_incorrect_answer(self):
        self.save_user_answer("false")
