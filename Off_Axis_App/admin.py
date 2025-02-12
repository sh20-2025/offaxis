from django.contrib import admin
from .models import Artist, Client, SocialLink, GenreTag, ContactInformation
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
                )
            },
        ),
    )
    list_display = ("user", "is_approved", "slug")
    search_fields = ("user__username", "slug")
    list_filter = ("is_approved",)

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.user.username)
        super().save_model(request, obj, form, change)


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


admin.site.register(Client)
admin.site.register(SocialLink)
admin.site.register(GenreTag)
