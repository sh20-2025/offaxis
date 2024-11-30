from ..models import Cart, Client, Artist


def get_or_create_cart(u=None, cart_id=None):
    """
    Gets or creates a cart for a user or cart_id.

    If a user is provided, the cart will either be created or retrieved from the user's cart attribute.
    If the cart_id is provided, the cart will either be retrieved from the database or created.

    If the user and cart_id is provided and the user has no cart, the cart will be taken from the cart_id and assigned to the user.

    If neither a user or cart_id is provided, a new cart will be created.

    If the provided cart_id belongs to a user that is not the provided user (or the user is none), the cart_id will be ignored.

    Returns the cart object.
    """

    cart = None

    if cart_id is not None:
        if Cart.objects.filter(id=cart_id).exists():
            cart = Cart.objects.get(id=cart_id)

            cart_owner = None
            if Client.objects.filter(cart=cart).exists():
                cart_owner = Client.objects.get(cart=cart)
            elif Artist.objects.filter(cart=cart).exists():
                cart_owner = Artist.objects.get(cart=cart)

            # cart is owned by a different user so can't access
            if cart_owner is not None and (u is None or cart_owner.user.id != u.id):
                cart = None

        else:
            cart = Cart.objects.create()

    if u is not None:
        if hasattr(u, "artist"):
            u = u.artist
        elif hasattr(u, "client"):
            u = u.client
        else:
            raise ValueError("Cart for user not implemented")

        if u.cart is not None:
            cart = u.cart
        else:
            if cart is None:
                cart = Cart.objects.create()

            u.cart = cart
            u.save()

    elif cart is None:
        cart = Cart.objects.create()

    return cart
