from django.shortcuts import render


def learning(request):
    return render(request, "learning_landing.html", {})
