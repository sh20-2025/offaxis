from Off_Axis_App.models import Gig, Ticket, User, Client
import stripe
import qrcode
from django.core.files.base import ContentFile
from io import BytesIO
from Off_Axis_App.helpers.emails import send_ticket_email


def handle_checkout_session_completed(event):
    checkout_session = event.data.object
    line_items = stripe.checkout.Session.list_line_items(checkout_session.id).data
    breakdown = stripe.checkout.Session.retrieve(
        checkout_session.id, expand=["total_details.breakdown"]
    ).total_details.breakdown

    email = (
        checkout_session.customer_email
        if checkout_session.customer_email
        else checkout_session.customer_details.email
    )
    name = (
        checkout_session.customer_details.name
        if checkout_session.customer_details
        else None
    )
    postcode = (
        checkout_session.customer_details.address.postal_code
        if checkout_session.customer_details
        else None
    )
    country = (
        checkout_session.customer_details.address.country
        if checkout_session.customer_details
        else None
    )

    # print(checkout_session)
    # print(line_items)

    print("Checkout session completed", checkout_session.id, "for", email)

    user = User.objects.filter(email=email).first()
    if user is None:
        print("Could not find user for email", email)
    else:
        user = Client.objects.filter(user=user).first()
        if user is None:
            print("Could not find client for user", user.email)

    for item in line_items:
        gig = Gig.objects.filter(stripe_product_id=item.price.product).first()
        if gig is None:
            print("Could not find gig for product", item.price.product, email)
            continue

        for _ in range(item.quantity):
            ticket = Ticket.objects.create(
                gig=gig,
                user=user,
                checkout_email=email,
                checkout_name=name,
                checkout_postcode=postcode,
                checkout_country=country,
                purchase_price=int(
                    item.price.unit_amount_decimal
                    if item.price.unit_amount_decimal
                    else gig.price
                )
                / 100,
                discount_used=",".join(
                    [d.discount.coupon.name for d in breakdown.discounts]
                ),
            )

            qr_img = qrcode.make(ticket.qr_code_data)
            img_io = BytesIO()
            qr_img.save(img_io, format="JPEG")

            ticket.qr_code.save(
                f"{ticket.qr_code_data}.jpg", ContentFile(img_io.getvalue())
            )
            ticket.save()

            print("Created ticket", ticket.id, "for", email, "for gig", gig.id)

            send_ticket_email(ticket)
            print("Sent ticket email to", email)
