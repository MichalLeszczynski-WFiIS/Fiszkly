from django.test import TestCase
from django.contrib.auth.models import User
from accounts.tasks import send_email_notifications


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

 