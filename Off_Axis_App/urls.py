from django.urls import path, include
from django.contrib import admin
from . import views

# admin.site.site_header = "Off Axis"
# admin.site.index_title = "Admin Dashboard"
# admin.site.site_url = "/"
# admin.site.enable_nav_sidebar = True
# admin.site.empty_value_display = "-"

urlpatterns = [
    path("artists/", views.artists_view, name="artists"),
    path("artist/<slug:slug>/", views.artist_view, name="artist"),
    path("register/", views.register, name="register"),
    path("", views.index, name="index"),
    path("components", views.components, name="components"),
]
