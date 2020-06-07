from django.urls import path
from words import views

app_name = "words"

urlpatterns = [
    path("", views.browse_groups, name="browse_groups"),
    path("browse-words/<slug:category>", views.browse_words, name="browse_words"),
    path("upload-words/", views.upload_words, name="upload_words"),
    path("verify-words/", views.verify_words, name="verify_words"),
]
