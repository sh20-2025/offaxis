from django.urls import path
from . import views

urlpatterns = [
    path("artists/", views.artists_view, name="artists"),
    path("artist/<slug:slug>/", views.artist_view, name="artist"),
    path("register/", views.register, name="register"),
    path("", views.index, name="index"),
    path("components", views.components, name="components"),
    path("contact", views.contact, name="contact"),
]
