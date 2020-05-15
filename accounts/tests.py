from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password"),
        )

    def test_login(self):
        response = self.client.post("/login/", self.credentials, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)
