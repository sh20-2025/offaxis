from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Artist
from .forms import ClientForm


# Create your views here.


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


def login_redirect_view(request):
    if request.user.is_staff:
        return redirect("/admin/")
    elif hasattr(request.user, "artist"):
        return redirect(reverse("artist", args=[request.user.artist.slug]))
    else:
        return redirect("/")
