from django.test import TestCase
from accounts.tasks import send_email_notifications
from fiszkly.tests_common import (
    UserCreatedTestTemplate,
    LoggedInTestTemplate,
    HaveAnswerTestTemplate,
)


class LogInTest(UserCreatedTestTemplate):
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


class LogOutTest(LoggedInTestTemplate):
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


class CeleryTest(LoggedInTestTemplate):
    def test_send_email_message(self):
        message = send_email_notifications()
        self.assertIn("testuser", message)
        self.assertIn("fiszkly.pl", message)


class ProfileTest(HaveAnswerTestTemplate):
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
