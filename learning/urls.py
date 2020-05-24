from django.urls import path

from learning import views

app_name = "learning"

urlpatterns = [
    path("", views.index, name="index"),
    path("save_answer/", views.save_answer),
    path("get_answer/", views.get_answer),
    path("check_user_skills/<slug:id>", views.check_user_skills, name="check_user_skills"),
]
