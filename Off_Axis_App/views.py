from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Artist, Gig, Ticket
from django.urls import reverse
from .forms import ClientForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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


def gigs(request):
    context = {}
    context["gigs"] = Gig.objects.all()

    return render(request, "Off_Axis/gigs.html", context)


def gig(request, artist, id):
    context = {}
    context["gig"] = Gig.objects.get(id=id)
    context["tickets_sold"] = Ticket.objects.filter(gig=context["gig"]).count()
    context["capacity_last_few"] = context["gig"].capacity * 0.9
    context["total_payable_amount"] = context["gig"].price + context["gig"].booking_fee

    return render(request, "Off_Axis/gig.html", context)


def login_redirect_view(request):
    if request.user.is_staff:
        return redirect("/admin/")
    elif hasattr(request.user, "artist"):
        return redirect(reverse("artist", args=[request.user.artist.slug]))
    else:
        return redirect("/")


@login_required
def approve_artist(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    if request.method == "POST":
        artist.is_approved = "approve" in request.POST
        artist.save()
    return redirect(reverse("artist", args=[artist.slug]))


@login_required
def upload_profile_picture(request):
    artist_slug = request.POST.get("artist_slug")
    artist = get_object_or_404(Artist, slug=artist_slug)

    if artist.profile_picture:
        artist.profile_picture.delete()

    if (
        "profile_picture" in request.FILES
    ):  # Ensure the name matches the name in the JavaScript
        artist.profile_picture = request.FILES["profile_picture"]
        artist.save()
        return JsonResponse({"picture_url": artist.profile_picture.url})

    return JsonResponse({"error": "No file uploaded"}, status=400)
