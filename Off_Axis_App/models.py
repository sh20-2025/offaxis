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


class ContactInformation(models.Model):
    # Arbitrary max lengths, can be changed
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message_content = models.TextField(max_length=2000)

    MESSAGE_TYPE = [
        ("general_question", "General Question"),
        ("cant_find_tickets", "I can't find my tickets"),
        ("ticket_query", "Ticket Query"),
        ("press_enquiry", "Press Enquiry"),
    ]
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) {self.message_type}"


class Gig(models.Model):
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    venue = models.ForeignKey("Venue", on_delete=models.CASCADE)
    supporting_artists = models.ManyToManyField(
        "Artist", blank=True, related_name="supporting_artists"
    )
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    booking_fee = models.DecimalField(max_digits=19, decimal_places=2, default=1.25)
    capacity = models.IntegerField()
    description = models.TextField(max_length=500)
    gig_photo_url = models.TextField(max_length=2048)


class Venue(models.Model):
    name = models.TextField(max_length=500)
    address = models.OneToOneField("Address", on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    venue_photo_url = models.TextField(max_length=2048)


class Ticket(models.Model):
    gig = models.ForeignKey("Gig", on_delete=models.CASCADE)
    user = models.ForeignKey("Client", on_delete=models.CASCADE)
    discount_used = models.TextField(max_length=256, blank=True)
    is_used = models.BooleanField(default=False)


class Address(models.Model):
    line_1 = models.TextField(max_length=256)
    line_2 = models.TextField(max_length=256)
    country = models.TextField(max_length=256)
    city = models.TextField(max_length=256)
    state_or_province = models.TextField(max_length=256)
    post_code = models.TextField(max_length=64)


class Festival(models.Model):
    name = models.TextField(max_length=256)
    description = models.TextField(max_length=1024)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    artists = models.ManyToManyField("Artist", blank=True)
    youtube_video_url = models.URLField(blank=True)
    slug = models.SlugField(unique=True, default="")
    is_active = models.BooleanField(default=True)
    festival_photo_url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        # Generate slug from username
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
