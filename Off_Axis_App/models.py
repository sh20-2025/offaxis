import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .helpers.stripe import create_product


# Client will always be made when a user is made.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cart = models.OneToOneField("Cart", null=True, on_delete=models.CASCADE)
    billing_info = models.CharField(
        max_length=100, blank=True
    )  # This will need to change to link to a billing model.
    phone_number = models.CharField(max_length=100, blank=True)

    def __str__(self):

        return self.user.username


# Artist will be made if a user decides then will have to be approved by an admin.
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="artist")
    cart = models.OneToOneField("Cart", null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    is_approved = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to="artists/", null=True, blank=True)
    social_links = models.ManyToManyField("SocialLink", blank=True)
    genre_tags = models.ManyToManyField("GenreTag", blank=True)
    slug = models.SlugField(unique=True, default="default-slug")
    credit = models.OneToOneField(
        "Credit", on_delete=models.CASCADE, related_name="artist_credit", null=True
    )

    def get_all_transactions(self):
        return CreditTransaction.objects.filter(to_artist=self)

    def get_pending_transactions(self):
        return CreditTransaction.objects.filter(to_artist=self, status="pending")

    def get_accepted_transactions(self):
        return CreditTransaction.objects.filter(to_artist=self, status="accepted")

    def credit_balance(self):
        return self.credit.balance

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)
        if not self.credit:
            self.credit = Credit.objects.create()
            super().save(update_fields=["credit"])

    def __str__(self):
        return self.user.username


# social link attribute.
class SocialLink(models.Model):
    SPOTIFY = "Spotify"
    YOUTUBE = "YouTube"
    SOUNDCLOUD = "SoundCloud"
    INSTAGRAM = "Instagram"
    WHATSAPP = "WhatsApp"

    SOCIAL_CHOICES = [
        (SPOTIFY, "Spotify"),
        (YOUTUBE, "YouTube"),
        (SOUNDCLOUD, "SoundCloud"),
        (INSTAGRAM, "Instagram"),
        (WHATSAPP, "WhatsApp"),
    ]

    type = models.CharField(max_length=100, choices=SOCIAL_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.type}: {self.url}"


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
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="gigs")
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
    is_approved = models.BooleanField(default=False)
    stripe_product_id = models.TextField(max_length=256, null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    def tickets(self):
        return Ticket.objects.filter(gig=self.id)

    def tickets_sold(self):
        return self.tickets().count()

    def tickets_available(self):
        return max(0, self.capacity - self.tickets_sold())

    def full_price(self):
        return self.price + self.booking_fee

    def name(self, upper_artist_name=True, with_city=False, with_date=False):
        name = self.artist.user.username

        if upper_artist_name:
            name = name.upper()

        if with_city:
            name = f"{self.artist.user.username} - {self.venue.address.city}"

        if with_date:
            name = f"{name} - {self.date.strftime('%d/%m/%Y')}"

        return name

    def approve(self):
        self.is_approved = True

        if not self.stripe_product_id:
            product = create_product(
                name=self.name(with_city=True, with_date=True),
                price=self.full_price(),
                description=self.description,
            )
            self.stripe_product_id = product.id

        self.save()


class Venue(models.Model):
    name = models.TextField(max_length=500)
    address = models.OneToOneField("Address", on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    venue_photo_url = models.TextField(max_length=2048)


class Ticket(models.Model):
    gig = models.ForeignKey("Gig", on_delete=models.CASCADE)
    user = models.ForeignKey("Client", on_delete=models.CASCADE, null=True)
    checkout_email = models.EmailField()
    checkout_name = models.TextField(max_length=256)
    checkout_postcode = models.TextField(max_length=256)
    checkout_country = models.TextField(max_length=256)
    purchase_price = models.DecimalField(max_digits=19, decimal_places=2)
    discount_used = models.TextField(max_length=256, blank=True)
    is_used = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to="ticket-qr-codes/", blank=True)
    qr_code_data = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Address(models.Model):
    line_1 = models.TextField(max_length=256)
    line_2 = models.TextField(max_length=256)
    country = models.TextField(max_length=256)
    city = models.TextField(max_length=256)
    state_or_province = models.TextField(max_length=256)
    post_code = models.TextField(max_length=64)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    gig = models.ForeignKey("Gig", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=19, decimal_places=2)


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


class Credit(models.Model):
    balance = models.IntegerField(default=2)

    def __str__(self):
        return f"Credit - Balance: {self.balance}"


class CreditTransaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    from_artist = models.ForeignKey(
        "Artist", on_delete=models.CASCADE, related_name="sent_transactions", null=True
    )
    to_artist = models.ForeignKey(
        "Artist",
        on_delete=models.CASCADE,
        related_name="received_transactions",
        null=True,
    )
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    timestamp = models.DateTimeField(auto_now_add=True)
    gig = models.ForeignKey("Gig", on_delete=models.Case, null=True)

    def __str__(self):
        return f"{self.from_artist.user.username} supported {self.to_artist.user.username} with {self.amount} credits; Status: {self.status}"


class CMS(models.Model):
    just_announced_gigs = models.ManyToManyField(
        "Gig", blank=True, related_name="just_announced_in_cms"
    )
    featured_gigs = models.ManyToManyField(
        "Gig", blank=True, related_name="featured_in_cms"
    )
    artist_of_the_week = models.ForeignKey(
        "Artist", on_delete=models.CASCADE, null=True
    )
