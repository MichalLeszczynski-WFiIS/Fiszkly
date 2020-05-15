from django.urls import path
from learning import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "check_user_skills/<slug:id>", views.check_user_skills, name="check_user_skills"
    ),
    path("save_answer/", views.save_answer),
    path("get_answer/", views.get_answer),
]
