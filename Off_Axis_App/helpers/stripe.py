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
