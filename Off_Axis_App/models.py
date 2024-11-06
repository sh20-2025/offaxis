from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Client will always be made when a user is made.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    billing_info = models.CharField(
        max_length=100, blank=True
    )  # This will need to change to link to a billing model.
    phone_number = models.CharField(max_length=100, blank=True)

    def __str__(self):

        return self.user.username


# Artist will be made if a user decides then will have to be approved by an admin.
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    is_approved = models.BooleanField(default=False)
    profile_picture_url = models.URLField(blank=True)

    social_links = models.ManyToManyField("SocialLink", blank=True)
    genre_tags = models.ManyToManyField("GenreTag", blank=True)
    gigs = models.TextField(
        max_length=500, blank=True
    )  # models.ManyToManyField('Gig', blank=True) eventually.

    slug = models.SlugField(unique=True, default="default-slug")

    def save(self, *args, **kwargs):
        # Generate slug from username
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):

        return self.user.username


# social link attribute.
class SocialLink(models.Model):
    type = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.type


# genre tag attribute.
class GenreTag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag
