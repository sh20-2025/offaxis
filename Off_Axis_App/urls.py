from django.urls import path, include
from django.contrib import admin
# from django.contrib.auth import auth_views
from . import views

admin.site.site_header = "Off Axis Administration"
admin.site.index_title = "Admin Dashboard"
admin.site.site_title = "Off Axis Admin Portal"
admin.site.site_url = "/"
admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "-"
admin.site.login_url = '/admin/login/'
admin.site.logout_url = '/admin/logout'

urlpatterns = [
    path("artists/", views.artists_view, name="artists"),
    path("artist/<slug:slug>/", views.artist_view, name="artist"),
    path("register/", views.register, name="register"),
    path("gigs/", views.gigs, name="gigs"),
    path("gigs/<str:artist>/<int:id>/", views.gig, name="gig"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("login-redirect/", views.login_redirect_view, name="login_redirect"),
    # path("logout-redirect/", views.logout_redirect_view, name="logout_redirect"),
    # path("admin/login/", include("django.contrib.auth.urls")),
    path("admin/logout/", views.admin_logout_view, name="admin_logout"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("", views.index, name="index"),
    path("components", views.components, name="components"),
]
