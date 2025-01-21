import stripe
from django.conf import settings
import decimal

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(
    name: str, price: decimal.Decimal, description: str = "", url: str = None
) -> stripe.Product:
    """
    Create a product in Stripe

    name: name of the product
    price: price of the product in the currency specified in settings.STRIPE_CURRENCY_CODE, a decimal value 1.23 = £1.23
    description?: description of the product
    url?: url of the product

    returns: the product object created in Stripe
    """

    price_data = {
        "currency": settings.STRIPE_CURRENCY_CODE,
        "unit_amount": int(price * 100),
    }

    return stripe.Product.create(
        name=name, default_price_data=price_data, description=description, url=url
    )


def delete_product(product_id: str) -> None:
    """
    Delete a product in Stripe

    product_id: the id of the product to delete
    """

    stripe.Product.delete(product_id)


def update_product(
    product_id: str,
    name: str = None,
    price: decimal.Decimal = None,
    description: str = None,
    url: str = None,
    is_active=None,
) -> stripe.Product:
    """
    Update a product in Stripe

    product_id: the id of the product to update
    name?: name of the product
    price?: price of the product in the currency specified in settings.STRIPE_CURRENCY_CODE, a decimal value 1.23 = £1.23
    description?: description of the product
    url?: url of the product
    is_active?: whether the product is active

    returns: the product object updated in Stripe
    """

    price_id = None
    if price is not None:
        price_id = stripe.Price.create(
            product=product_id,
            currency=settings.STRIPE_CURRENCY_CODE,
            unit_amount=int(price * 100),
        ).id

    return stripe.Product.modify(
        product_id,
        name=name,
        description=description,
        url=url,
        active=is_active,
        default_price=price_id,
    )


def get_product(product_id: str) -> stripe.Product:
    """
    Get a product from Stripe

    product_id: the id of the product to get

    returns: the product object from Stripe
    """

    return stripe.Product.retrieve(product_id)


class CheckoutProduct:
    def __init__(self, product_id: str, quantity: int):
        self.product_id = product_id
        self.product = get_product(product_id)
        self.quantity = quantity


def create_checkout_session(products: list[CheckoutProduct], customer_email=None):
    """
    Create a checkout session in Stripe

    products: a list of product ids to purchase
    success_url: the url to redirect to on successful purchase
    cancel_url: the url to redirect to on cancelled purchase
    customer_email: the email of the customer

    returns: the checkout session object created in Stripe
    """

    line_items = [
        {"price": p.product.default_price, "quantity": p.quantity} for p in products
    ]

    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=settings.STRIPE_CHECKOUT_SUCCESS_URL,
        cancel_url=settings.STRIPE_CHECKOUT_CANCEL_URL,
        customer_email=customer_email,
        customer_creation="always",
        allow_promotion_codes=settings.STRIPE_CHECKOUT_ALLOW_PROMO_CODES,
    )
