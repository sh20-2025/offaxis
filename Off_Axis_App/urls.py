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
    path("contact", views.contact, name="contact"),
    # path("password_change/", views.password_change, name="password_change"),
    # path("password_change/done/", views.PasswordChangeDoneView.as_view(),name="password_change_done",),
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
