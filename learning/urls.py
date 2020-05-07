from django.urls import path
from learning import views

urlpatterns = [path("", views.index, name="index"),
               path("test/<int:id>", views.learning, name="test"),
               path("save_answer/", views.save_answer)]
