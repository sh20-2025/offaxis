from django import forms
from .models import Client, User, ContactInformation


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ("first_name", "last_name", "email", "message_content")
