from django.contrib import admin
from .models import (
    Artist,
    Client,
    SocialLink,
    GenreTag,
    ContactInformation,
    Credit,
    CreditTransaction,
)
from .forms import ArtistForm
from django.utils.text import slugify


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    form = ArtistForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "cart",
                    "bio",
                    "is_approved",
                    "profile_picture",
                    "social_links",
                    "genre_tags",
                    "slug",
                    "credit",
                )
            },
        ),
    )
    list_display = ("user", "is_approved", "slug")
    search_fields = ("user__username", "slug")
    list_filter = ("is_approved",)
    list_display = ("user", "is_approved", "slug")
    search_fields = ("user__username", "slug")
    list_filter = ("is_approved",)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.user.username)
        super().save_model(request, obj, form, change)


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ("get_artist_username", "balance")
    search_fields = ("artist__user__username",)

    def get_artist_username(self, obj):
        return obj.artist.user.username

    get_artist_username.short_description = "Artist"


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "message_type",
        "message_content",
    )
    list_filter = ("message_type",)
    search_fields = ("first_name", "last_name", "email", "message_type")


@admin.register(CreditTransaction)
class CreditTransactionAdmin(admin.ModelAdmin):
    list_display = ("from_artist", "to_artist", "amount", "status", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("from_artist__user__username", "to_artist__user__username")


admin.site.register(Client)
admin.site.register(SocialLink)
admin.site.register(GenreTag)
