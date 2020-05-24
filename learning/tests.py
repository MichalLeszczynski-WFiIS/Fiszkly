from django.test import TestCase
from django.contrib.auth.models import User

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


class AvailabilityTest(TestCase):
    def setUp(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        User.objects.create_user(
            username=self.credentials.get("username"), password=self.credentials.get("password")
        )
        logged_in = self.client.login(**self.credentials)

    def test_access_to_check_user_skills_with_login(self):
        response = self.client.get("/learning/check_user_skills/1", follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context["user"].is_authenticated)
