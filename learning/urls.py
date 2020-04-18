from django.urls import path
from learning import views

urlpatterns = [
    path("", views.learning, name="learning")
]