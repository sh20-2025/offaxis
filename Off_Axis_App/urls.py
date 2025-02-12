from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

admin.site.site_header = "Off Axis Administration"
admin.site.index_title = "Admin Dashboard"
admin.site.site_title = "Off Axis Admin Portal"
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "-"
admin.site.login_url = "/admin/login/"
admin.site.logout_url = "/admin/logout"

urlpatterns = [
    path("artists/", views.artists_view, name="artists"),
    path("artist/<slug:slug>/", views.artist_view, name="artist"),
    path("register/", views.register, name="register"),
    path("gigs/", views.gigs, name="gigs"),
    path("gigs/<str:artist>/<int:id>/", views.gig, name="gig"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("login-redirect/", views.login_redirect_view, name="login_redirect"),
    path("admin/logout/", views.admin_logout_view),
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
    path("add_social_link/", views.add_social_link, name="add_social_link"),
    path("contact", views.contact, name="contact"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/completed/", views.checkout_completed, name="checkout_completed"),
    path("contact/", views.contact, name="contact"),
    path("festivals/", views.festivals, name="festivals"),
    path("festivals/<str:slug>/", views.festival, name="festival"),
    # have not implemented password change for artist and clients for now, will do so later for next sprint
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            email_template_name="registration/password_reset_email.html",
            html_email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html",
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
    path(
        "delete_social_link/<int:social_link_id>/",
        views.delete_social_link,
        name="delete_social_link",
    ),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("scan-tickets/", views.scan_tickets, name="scan_tickets"),
    path("scan-tickets/<int:id>", views.ticket_scanner, name="ticket_scanner"),
    path("scan-tickets-api/<str:code>", views.scan_ticket_api, name="scan_ticket_api"),
    path(
        "artist/<slug:slug>/add-social-link/",
        views.add_social_link,
        name="add_social_link",
    ),
    path(
        "artist/<slug:slug>/remove-social-link/<str:social_type>/",
        views.remove_social_link,
        name="remove_social_link",
    ),
]
