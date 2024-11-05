from django.test import TestCase
from django.contrib import admin
from Off_Axis_App.models import Artist, Client, SocialLink, GenreTag

# Register your models here.
admin.site.register(Artist)
admin.site.register(Client)
admin.site.register(SocialLink)
admin.site.register(GenreTag)
