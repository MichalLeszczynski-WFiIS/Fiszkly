from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm
from django.shortcuts import redirect

from django.contrib import messages

# Create your views here.

def home(request):
	return render(request, 'dashboard.html')

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for user ' + user)
            return redirect('/login')
        else:
            messages.info(request, 'Wrong data has been passed.')



    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../learning')
        else:
            messages.info(request, 'Username or password is incorect.')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')