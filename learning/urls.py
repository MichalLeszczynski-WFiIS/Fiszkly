from django.urls import path
from learning import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/<slug:id>", views.test, name="test"),
    path("save_answer/", views.save_answer),
    path("get_answer/", views.get_answer),
]
