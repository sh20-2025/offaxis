from django.contrib import admin
from Off_Axis_App.models import Artist, Client, SocialLink, GenreTag, ContactInformation

# from .models import Artist

# Register your models here.
admin.site.register(Artist)
admin.site.register(Client)
admin.site.register(SocialLink)
admin.site.register(GenreTag)


# This was the only way I could get the admin to display, don't know why it wouldn't work otherwise
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
