from django.shortcuts import render


def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {'user': user}
    return render(request, "index.html", context)
