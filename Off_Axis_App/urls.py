from django.urls import path, include
from . import views

urlpatterns = [
    path("artists/", views.artists_view, name="artists"),
    path("artist/<slug:slug>/", views.artist_view, name="artist"),
    path("register/", views.register, name="register"),
    path("gigs/", views.gigs, name="gigs"),
    path("gigs/<str:artist>/<int:id>/", views.gig, name="gig"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login-redirect/", views.login_redirect_view, name="login_redirect"),
    path("", views.index, name="index"),
    path("components", views.components, name="components"),
    path("cart/", views.cart, name="cart"),
]
