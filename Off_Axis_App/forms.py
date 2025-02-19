from django import forms
from .models import Client, User, ContactInformation, Artist, SocialLink, Gig
from django.contrib.auth.password_validation import validate_password
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
        email = cleaned_data.get("email")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email already exists")

        if password:
            try:
                validate_password(password)
            except forms.ValidationError as e:
                self.add_error("password", e)

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

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


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model = SocialLink
        fields = ["type", "url"]

    def clean_url(self):
        url = self.cleaned_data.get("url")
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url


class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = [
            "artist",
            "venue",
            "supporting_artists",
            "date",
            "price",
            "booking_fee",
            "capacity",
            "description",
            "gig_photo_url",
            "is_approved",
        ]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "venue": forms.TextInput(attrs={"placeholder": "Enter venue name"}),
            "supporting_artists": forms.SelectMultiple(attrs={"size": 5}),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Enter description"}
            ),
            "gig_photo_url": forms.URLInput(attrs={"placeholder": "Enter a valid URL"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        gig = super().save(commit=False)
        if not gig.description:
            gig.description = "No description provided."
        if commit:
            gig.save()
        return gig
