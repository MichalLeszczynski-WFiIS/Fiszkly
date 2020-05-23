from django.urls import path
from words import views

app_name = "words"

urlpatterns = [
    path("upload/", views.upload, name="upload"),
]
