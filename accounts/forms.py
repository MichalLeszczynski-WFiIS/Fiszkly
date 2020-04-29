from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        required=True,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.fields.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.fields.TextInput(attrs={"placeholder": "Email"}),
        }
