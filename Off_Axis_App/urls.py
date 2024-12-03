from django.urls import path, include
from django.contrib.auth import views as auth_views
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
    path("approve_artist/<slug:slug>/", views.approve_artist, name="approve_artist"),
    path(
        "upload_profile_picture/",
        views.upload_profile_picture,
        name="upload_profile_picture",
    ),
    path("update_text/", views.update_text, name="update_text"),
    path("add_genre/", views.add_genre, name="add_genre"),
    path("contact", views.contact, name="contact"),
    # have not implemented password change for artist and clients for now, will do so later for next sprint
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirmation.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_successful.html"
        ),
        name="password_reset_complete",
    ),
]
