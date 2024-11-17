from django import forms
from .models import Client, User


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    billing_info = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = Client
        fields = [
            "username",
            "email",
            "password",
            "billing_info",
            "phone_number",
        ]

        widgets = {
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
            "password": forms.PasswordInput(),
            "billing_info": forms.TextInput(),
            "phone_number": forms.TextInput(),
        }

    def save(self, commit=True):
        client = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        client.user = user
        client.phone_number = self.cleaned_data["phone_number"]
        client.billing_info = self.cleaned_data["billing_info"]

        if commit:
            client.save()
