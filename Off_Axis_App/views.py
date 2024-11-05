from django.shortcuts import render
from Off_Axis_App.models import Artist


# Create your views here.
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
    context["artists"] = artist
    return render(request, "Off_Axis/artist.html", context)
