from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Artist,
    Gig,
    Ticket,
    GenreTag,
    SocialLink,
    Cart,
    CartItem,
    ContactInformation,
    Festival,
)
from .forms import ClientForm, ContactInformationForm, GigForm
from django.http.response import (
    HttpResponseBadRequest,
    HttpResponseNotAllowed,
    HttpResponseForbidden,
)
from django.http import QueryDict
from .helpers.cart import get_or_create_cart
from .helpers.stripe import CheckoutProduct, create_checkout_session
from .helpers.stripe_webhook import handle_checkout_session_completed
from django.urls import reverse
from django.core.cache import cache
from django.utils.timezone import now
import math
from urllib.parse import urlencode, urlparse
from django.contrib.auth import login
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from .api.spotify_utils import get_artist_top_track
from django.views.decorators.http import require_POST
import re


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
    artist = get_object_or_404(Artist, slug=slug)

    gig_form = GigForm()

    if request.method == "POST":
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.artist = artist
            gig.save()
            return redirect(reverse("artist", args=[artist.slug]))

    # Get Spotify top track if artist has Spotify link
    top_track = None
    spotify_link = artist.social_links.filter(type="Spotify").first()
    if spotify_link:
        top_track = get_artist_top_track(spotify_link.url)

    genres = GenreTag.objects.all()
    select_options = []
    for each in genres:
        select_options.append({"label": each.tag, "value": each.tag})

    context = {
        "artist": artist,
        "options": select_options,
        "top_track": top_track,
        "gig_form": gig_form,
    }
    return render(request, "Off_Axis/artist.html", context)


def register(request):
    client_form = ClientForm()
    is_artist = request.POST.get("isArtist") == "Artist"

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
                    {"error": "Username already exists", "clientForm": client_form},
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
    context["tickets_sold"] = context["gig"].tickets_sold()
    context["capacity_last_few"] = context["gig"].capacity * 0.9

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


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


@user_passes_test(lambda u: u.is_staff)
def admin_logout_view(request):
    logout(request)
    return redirect("/admin/login/?next=/admin/")


def cart(request):
    """
    On POST request add a gig to the cart.

    The user can add a maximum of `settings.MAX_CART_ITEMS` items to the cart.

    The user can add a maximum of `min(gig.tickets_available(), settings.MAX_CART_QUANTITY)` tickets to the cart for one gig.

    The request body should be:
    ```
    {
        "gig_id": <string> (required),
        "quantity": <int> (required, >= 0 and <= settings.MAX_CART_QUANTITY) (optional if action is "remove"),
        "action": "add" | "update" | "remove" (required)
    }
    ```
    """

    def response():
        url = reverse("cart")
        if context["error"]:
            url += f"?error={context['error']}"

        res = redirect(url)
        res.set_cookie("cart_id", str(cart.id))
        return res

    # find or create cart
    cart = get_or_create_cart(
        request.user if request.user.is_authenticated else None,
        request.COOKIES.get("cart_id"),
    )
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        "error": request.GET.get("error") or "",
        "cart": cart,
        "cart_items": cart_items,
        "cart_total_price": sum([item.total_price for item in cart_items]),
    }

    if request.method == "POST":
        query_dict = QueryDict(request.body)

        # get gig
        gig_id = int(query_dict.get("gig_id"))

        if not Gig.objects.filter(id=gig_id).exists():
            context["error"] = "Gig does not exist"
            return response()

        gig = Gig.objects.get(id=gig_id)

        existing_cart_item = CartItem.objects.filter(cart=cart, gig=gig).first()
        action = query_dict.get("action")

        if (action == "update" or action == "remove") and not existing_cart_item:
            context["error"] = "Item not in cart"
            return response()

        # get quantity
        if query_dict.get("quantity") is None and action != "remove":
            context["error"] = "Quantity required"
            return response()

        quantity = int(query_dict.get("quantity") or 0)
        if quantity < 0:
            context["error"] = "Quantity must be greater than or equal to 0"
            return response()

        if quantity > gig.tickets_available():
            context["error"] = (
                f"Only {gig.tickets_available()} tickets available for '{
                    gig.name()}'"
            )
            return response()

        if (
            quantity + (existing_cart_item.quantity if existing_cart_item else 0)
            > settings.MAX_CART_QUANTITY
        ):
            context["error"] = (
                f"Maximum of {settings.MAX_CART_QUANTITY} tickets can be added to cart for '{
                    gig.name()}'"
            )
            return response()

        # get action
        if action not in ["add", "update", "remove"]:
            context["error"] = "Invalid action"
            return response()

        # validate action with params
        if action == "add" and quantity == 0:
            context["error"] = "Quantity must be greater than 0 to add item to cart"
            return response()

        if action == "add" and cart_items.count() >= settings.MAX_CART_ITEMS:
            context["error"] = (
                f"Maximum of {settings.MAX_CART_ITEMS} items can be added to cart"
            )
            return response()

        # perform action
        if action == "add":
            if existing_cart_item:
                existing_cart_item.quantity += quantity
            else:
                CartItem.objects.create(
                    cart=cart,
                    gig=gig,
                    quantity=quantity,
                    total_price=gig.full_price() * quantity,
                )
        elif action == "remove" or (action == "update" and quantity == 0):
            existing_cart_item.delete()
            existing_cart_item = None
        elif action == "update":
            existing_cart_item.quantity = quantity

        if existing_cart_item:
            existing_cart_item.total_price = (
                gig.full_price() * existing_cart_item.quantity
            )
            existing_cart_item.save()

        return response()

    return render(request, "Off_Axis/cart.html", context)


def checkout(request):
    cart = get_or_create_cart(
        request.user if request.user.is_authenticated else None,
        request.COOKIES.get("cart_id"),
    )
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect(reverse("cart") + "?error=Cart is empty")

    products = [
        CheckoutProduct(item.gig.stripe_product_id, item.quantity)
        for item in cart_items
    ]
    session = create_checkout_session(
        products, request.user.email if request.user.is_authenticated else None
    )

    return redirect(session.url)


def checkout_completed(request):
    context = {
        "status": request.GET.get("status") or "success",
    }

    # clear cart only if checkout was successful
    if context["status"] == "success":
        cart = get_or_create_cart(
            request.user if request.user.is_authenticated else None,
            request.COOKIES.get("cart_id"),
        )
        CartItem.objects.filter(cart=cart).delete()

    return render(request, "Off_Axis/checkout/completed.html", context)


def password_change(request):
    return render(request, "registration/password_change_form.html")


def contact(request):
    cooldown_period = 60
    cache_key = f"contact_form_{
        request.user.id if request.user.is_authenticated else request.META['REMOTE_ADDR']}"
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


def festivals(request):
    context = {
        "festivals": Festival.objects.filter(is_active=True),
    }

    return render(request, "Off_Axis/festivals.html", context)


def festival(request, slug):
    f = Festival.objects.get(slug=slug)
    context = {
        "festival": f,
        "artists": f.artists.all(),
    }

    return render(request, "Off_Axis/festival.html", context)


def social_link_validation(social_link, type):
    # validating social_link against type shown
    link_regex = {
        "YouTube": r"https://www\.youtube\.com/channel/[a-zA-Z0-9_-]+",
        "Spotify": r"https://open\.spotify\.com/artist/[a-zA-Z0-9]+",
        "Instagram": r"https://www\.instagram\.com/[a-zA-Z0-9_]+",
        "SoundCloud": r"https://soundcloud\.com/[a-zA-Z0-9_-]+",
        "WhatsApp": r"https://wa\.me/[0-9]+",
    }

    if not re.match(link_regex[type], social_link):
        return False
    return True


def add_social_link_on_artist(request):
    if request.method == "POST":
        artist_slug = request.POST.get("artist_slug")
        social_type = request.POST.get("type")
        social_url = request.POST.get("url")

        artist = get_object_or_404(Artist, slug=artist_slug)

        if not social_link_validation(social_url, social_type):
            return JsonResponse({"error": "Invalid URL"}, status=400)

        social_link = SocialLink.objects.create(
            artist=artist, type=social_type, url=social_url
        )
        social_link.save()
        artist.social_links.add(social_link)
        artist.save()

        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def add_social_link(request, slug):
    artist = get_object_or_404(Artist, slug=slug)

    if request.user != artist.user:
        return HttpResponseForbidden(
            "You are not allowed to edit this artist's social links."
        )

    social_platforms = ["YouTube", "Spotify", "Instagram", "SoundCloud", "WhatsApp"]
    allowed_domains = {
        "spotify.com",
        "youtube.com",
        "soundcloud.com",
        "whatsapp.com",
        "instagram.com",
    }

    social_links_data = [
        {"type": platform, "link": artist.social_links.filter(type=platform).first()}
        for platform in social_platforms
    ]

    if request.method == "POST":
        social_type = request.POST.get("type")
        social_url = request.POST.get("url")

        if not social_type or not social_url:
            return redirect("add_social_link", slug=artist.slug)

        social_url = social_url.strip().lower()

        if not social_url.startswith(("http://", "https://")):
            social_url = "https://" + social_url

        parsed_url = urlparse(social_url)
        domain = parsed_url.netloc.replace("www.", "")

        if domain not in allowed_domains:
            return render(
                request,
                "Off_Axis/add_social_link.html",
                {
                    "artist": artist,
                    "social_links_data": social_links_data,
                    "allowed_domains": allowed_domains,
                    "error_message": f"Invalid URL! Only {', '.join(allowed_domains)} are allowed.",
                },
            )

        existing_link = artist.social_links.filter(type=social_type).first()
        if existing_link:
            return redirect("add_social_link", slug=artist.slug)

        social_link = SocialLink.objects.create(type=social_type, url=social_url)
        artist.social_links.add(social_link)

        return redirect("add_social_link", slug=artist.slug)


@require_POST
def delete_social_link(request, social_link_id):
    social_link = get_object_or_404(SocialLink, id=social_link_id)
    social_link.delete()
    return JsonResponse({"success": True})


@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    payload = request.body

    try:
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest(status=400)

    # Handle the event
    if not event:
        return HttpResponseBadRequest(status=400)

    if event["type"] == "checkout.session.completed":
        handle_checkout_session_completed(event)

    return HttpResponse(status=200)


def scan_tickets(request):
    if not request.user.is_authenticated or not request.user.artist:
        return HttpResponseForbidden()

    context = {
        # "gigs": Gig.objects.filter(artist=request.user.artist)
        "gigs": Gig.objects.all()
    }

    return render(request, "Off_Axis/scan_tickets.html", context)


def ticket_scanner(request, id):
    if not request.user.is_authenticated or not request.user.artist:
        return HttpResponseForbidden()

    # gig = Gig.objects.filter(artist=request.user.artist, id=id).first()
    gig = Gig.objects.filter(id=id).first()
    if not gig:
        return HttpResponseForbidden()

    context = {"gig": gig}

    return render(request, "Off_Axis/ticket_scanner.html", context)


@csrf_exempt
def scan_ticket_api(request, code):
    if not request.user.is_authenticated or not request.user.artist:
        return HttpResponseForbidden()

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    ticket = Ticket.objects.filter(qr_code_data=code).first()
    if not ticket:
        return HttpResponseBadRequest()

    ticket.is_used = True
    ticket.save()

    print("Ticket scanned for code ", code)

    return HttpResponse(status=200)
