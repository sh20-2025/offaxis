from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist, Gig, Ticket
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Artist
from .forms import ClientForm


def components(request):
    return render(
        request,
        "components/components_show_room.html",
        {
            "test_options": [
                {"label": "United States", "value": "US"},
                {"label": "Canada", "value": "CA"},
                {"label": "Mexico", "value": "MX"},
            ]
        },
    )


def index(request):
    return render(request, "Off_Axis/index.html")


def artists_view(request):
    context = {}
    artists = Artist.objects.all()
    context["artists"] = artists
    return render(request, "Off_Axis/artists.html", context)


def artist_view(request, slug):
    context = {}
    artist = Artist.objects.get(slug=slug)

    context["artist"] = artist
    return render(request, "Off_Axis/artist.html", context)


def register(request):
    client_form = ClientForm()
    is_artist = request.POST.get("isArtist") == "true"

    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            try:
                client = client_form.save()

                if is_artist:
                    artist = Artist(user=client.user)
                    artist.save()
                    return redirect(reverse("artist", args=[artist.slug]))

                return redirect("/")

            except IntegrityError:
                return render(
                    request,
                    "registration/register.html",
                    {"error": "Username already exists"},
                )

    return render(
        request,
        "registration/register.html",
        {"clientForm": client_form},
    )

# def login_redirect_view(request):
#     if request.user.is_staff:
#         return redirect("/admin/")
#     elif hasattr(request.user, "artist"):
#         return redirect(reverse("artist", args=[request.user.artist.slug]))
#     else:
#         return redirect("/")

# @login_required
# def logout_redirect_view(request):
#     logout(request)
#     return redirect("/")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('index')
        else:
            return render(request, 'login.html',{'error':'Invalid credentials.'})
    else:
        return render(request, 'login.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@user_passes_test(lambda u: u.is_staff)
def admin_logout_view(request):
    logout(request)
    return redirect('/admin/login/?next=/admin/')
# @login_required
# def admin_logout_redirect_view(request):
#     logout(request) # redirects to regular login page rather than admin 
#     return redirect('/admin/login/')