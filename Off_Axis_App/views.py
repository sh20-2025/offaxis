from django.shortcuts import render, get_object_or_404
from .models import Artist


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
