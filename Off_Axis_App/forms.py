from django import forms
from .models import Client, User, Artist, SocialLink, GenreTag
from django.utils.text import slugify


class ClientForm(forms.ModelForm):
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


class ArtistForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    bio = forms.CharField(max_length=500)
    profile_picture_url = forms.URLField()
    social_type = forms.CharField(max_length=100)
    social_links = forms.CharField(max_length=100)
    genre_tags = forms.CharField(max_length=100)
    gigs = forms.CharField(max_length=500)

    class Meta:
        model = Artist
        fields = [
            "username",
            "email",
            "password",
            "bio",
            "profile_picture_url",
            "social_type",
            "social_links",
            "genre_tags",
            "gigs",
        ]

    def save(self, commit=True):
        artist = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        artist.user = user
        artist.bio = self.cleaned_data["bio"]
        artist.profile_picture_url = self.cleaned_data["profile_picture_url"]
        artist.gigs = self.cleaned_data["gigs"]
        artist.slug = slugify(self.cleaned_data["username"])

        if commit:
            artist.save()
            social_link = SocialLink.objects.create(
                type=self.cleaned_data["social_type"],
                url=self.cleaned_data["social_links"],
            )
            genre_tag = GenreTag.objects.create(tag=self.cleaned_data["genre_tags"])
            artist.social_links.set([social_link])
            artist.genre_tags.set([genre_tag])
            artist.save()
