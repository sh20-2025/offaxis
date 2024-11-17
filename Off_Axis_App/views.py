from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist
from .forms import UserForm


# Create your views here.


def components(request):
    return render(
        request,
        "components/index.html",
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
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserForm()

    return render(request, "Off_Axis/register.html", {"form": form})
