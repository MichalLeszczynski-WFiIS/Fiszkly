from django.test import TestCase
from django.contrib.auth.models import User
from accounts.tasks import send_email_notifications
from django.contrib.auth.forms import UserCreationForm

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
        self.register_data = {"username": "testuser", "password1": "Siema_123", "password2": "Siema_123", "email": "test@gmail.com", "Create_user": ['Register']}
        self.credentials = {"username": "testuser", "password": "Siema_123"}
        
    def test_register(self):
        response = self.client.post("/register/", self.register_data, follow=True)
        self.assertEquals(response.status_code, 200)

        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)


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
