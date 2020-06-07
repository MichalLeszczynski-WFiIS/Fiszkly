from django.test import TestCase
from django.contrib.auth.models import User
from accounts.tasks import send_email_notifications
from django.contrib.auth.forms import UserCreationForm
from words.models import Flashcard
from learning.models import Answer


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )

    def test_login(self):
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_bad_password(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "credential"}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login_with_bad_username(self):
        response = self.client.post(
            "/login/", {"username": "bad", "password": "credential"}, follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class LogOutTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_logout(self):
        response = self.client.post("/logout/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(not response.context["user"].is_authenticated)


class RegisterTest(TestCase):
    def setUp(self):
        self.register_data = {
            "username": "testuser",
            "password1": "Siema_123",
            "password2": "Siema_123",
            "email": "test@gmail.com",
            "Create_user": ["Register"],
        }
        self.credentials = {"username": "testuser", "password": "Siema_123"}

    def test_register_requested(self):
        response = self.client.post("/register/", self.register_data, follow=True)
        self.assertEquals(response.status_code, 200)

        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)

    def test_register_initial(self):
        response = self.client.post("/register/", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("register.html")


class CeleryTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_send_email_message(self):
        message = send_email_notifications()
        self.assertIn("testuser", message)
        self.assertIn("fiszkly.pl", message)


class ProfileTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)

        Flashcard.objects.create(
            original_word="encouragement",
            translated_word="zachęta",
            original_language="en",
            translated_language="pl",
            dictionary_entry=r"[example_dictionary_entry]",
        )
        Answer.objects.create(
            incorrect_count=6,
            correct_count=8,
            flashcard=Flashcard.objects.get(id="1"),
            user=User.objects.get(username="testuser"),
        )

    def test_profile_view(self):
        response = self.client.post("/profile/", {}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed("profile.html")
        self.assertEquals(
            response.context["statistics"],
            '{"dates": ["None"], "correct": [8], "incorrect": [6], "all": [14], "percentage": [57.14285714285714]}',
        )
        self.assertEquals(response.context["answers"]["correct_answers"], 8)
        self.assertEquals(response.context["answers"]["incorrect_answers"], 6)
