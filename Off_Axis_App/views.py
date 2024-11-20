from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Artist
from .forms import ClientForm, ArtistForm


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
    if artist.is_approved:
        context["artist"] = artist
        return render(request, "Off_Axis/artist.html", context)
    else:
        return render(request, "Off_Axis/artist_not_approved.html", context)


def register(request):
    artist_form = ArtistForm()
    client_form = ClientForm()

    if request.method == "POST":
        if "is_artist" in request.POST:
            if request.POST.get("is_artist") == "true":
                form = ArtistForm(request.POST)
            else:
                form = ClientForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/")
        else:
            form = ClientForm(request.POST)

    return render(
        request,
        "registration/register.html",
        {"artist_form": artist_form, "client_form": client_form},
    )


def login_redirect_view(request):
    if request.user.is_staff:
        return redirect("/admin/")
    elif hasattr(request.user, "artist"):
        return redirect(reverse("artist", args=[request.user.artist.slug]))
    else:
        return redirect("/")
