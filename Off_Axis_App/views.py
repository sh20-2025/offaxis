from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist, Gig, Ticket, GenreTag, ContactInformation
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ClientForm, ContactInformationForm
from django.core.cache import cache
from django.utils.timezone import now
import math
from urllib.parse import urlencode
from django.contrib.auth import login


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
    genres = GenreTag.objects.all()
    context["artist"] = artist
    context["genres"] = genres
    return render(request, "Off_Axis/artist.html", context)


def register(request):
    client_form = ClientForm()
    is_artist = request.POST.get("isArtist") == "true"

    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            try:
                client = client_form.save()
                login(request, client.user)

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


@login_required
def update_text(request):
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        new_text = request.POST.get("new_text")

        artist_slug = request.POST.get("artist_slug")
        artist = get_object_or_404(Artist, slug=artist_slug)

        if section_id == "bio-text":
            artist.bio = new_text
            artist.save()
        else:
            return JsonResponse({"error": "Invalid section ID"}, status=400)

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_genre(request):
    if request.method == "POST":
        genre_tag = request.POST.get("genre")
        artist_slug = request.POST.get("artist_slug")
        artist = get_object_or_404(Artist, slug=artist_slug)

        genre, created = GenreTag.objects.get_or_create(tag=genre_tag)
        artist.genre_tags.add(genre)
        artist.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


def password_change(request):
    return render(request, "registration/password_change_form.html")


def contact(request):
    cooldown_period = 60
    cache_key = f"contact_form_{request.user.id if request.user.is_authenticated else request.META['REMOTE_ADDR']}"
    contact_message_type = [
        {"value": key, "label": label} for key, label in ContactInformation.MESSAGE_TYPE
    ]

    last_submission = cache.get(cache_key)
    if last_submission:
        time_remaining = cooldown_period - (now() - last_submission).total_seconds()
        if time_remaining > 0:
            return render(
                request,
                "Off_Axis/contact.html",
                {
                    "form": ContactInformationForm(),
                    "cooldown": math.ceil(time_remaining),
                    "contact_message_type": contact_message_type,
                },
            )

    if request.method == "POST":
        form = ContactInformationForm(request.POST)

        if form.is_valid():
            form.save()
            cache.set(cache_key, now(), timeout=cooldown_period)

            base_url = reverse("contact")
            query_string = urlencode({"contact_page_submission_value": "success"})
            return redirect(f"{base_url}?{query_string}")

    else:
        form = ContactInformationForm()

    return render(
        request,
        "Off_Axis/contact.html",
        {"form": form, "contact_message_type": contact_message_type},
    )
