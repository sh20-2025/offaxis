from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist
from .forms import UserForm, ArtistForm


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
    client_form = UserForm()

    if request.method == "POST":
        if "is_artist" in request.POST:
            if request.POST.get("is_artist") == "true":
                form = ArtistForm(request.POST)
            else:
                form = UserForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect("/")
        else:
            form = UserForm(request.POST)

    return render(
        request,
        "Off_Axis/register.html",
        {"artist_form": artist_form, "client_form": client_form},
    )
