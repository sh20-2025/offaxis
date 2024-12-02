from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist, Gig, Ticket, Cart, CartItem
from django.urls import reverse
from .forms import ClientForm
from django.http.response import HttpResponseBadRequest, HttpResponseNotAllowed
from django.http import QueryDict
from .helpers.cart import get_or_create_cart
from .helpers.stripe import CheckoutProduct, create_checkout_session
from django.conf import settings


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


def cart(request):
    """
    On POST request add a gig to the cart.

    The user can add a maximum of `settings.MAX_CART_ITEMS` items to the cart.

    The user can add a maximum of `min(gig.tickets_available(), settings.MAX_CART_QUANTITY)` tickets to the cart for one gig.

    The request body should be:
    {
        "gig_id": <string> (required),
        "quantity": <int> (required, >= 0) (optional if action is "remove"),
        "action": "add" | "update" | "remove" (required)
    }
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

        action = query_dict.get("action")

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

        if quantity > settings.MAX_CART_QUANTITY:
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

        existing_cart_item = CartItem.objects.filter(cart=cart, gig=gig).first()
        if (action == "update" or action == "remove") and not existing_cart_item:
            context["error"] = "Item not in cart"
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
