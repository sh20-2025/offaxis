from django import forms
from .models import Client, User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")
