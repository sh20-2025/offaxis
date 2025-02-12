from django import forms
from .models import Client, User, ContactInformation, Artist, SocialLink, GenreTag
from django.utils.text import slugify


class ClientForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

        model = Client
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def save(self, commit=True):
        client = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        client.user = user

        if commit:
            client.save()

        return client


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ("first_name", "last_name", "email", "message_content", "message_type")


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = "__all__"
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter artist bio"}),
            "profile_picture_url": forms.URLInput(
                attrs={"placeholder": "Enter a valid URL"}
            ),
            "social_links": forms.SelectMultiple(attrs={"size": 5}),
            "genre_tags": forms.SelectMultiple(attrs={"size": 5}),
            "slug": forms.TextInput(attrs={"readonly": "readonly"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if not slug:
            slug = slugify(self.instance.user.username)
        return slug
