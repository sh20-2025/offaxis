from Off_Axis_App.models import Gig, Ticket, User, Client
import stripe


def handle_checkout_session_completed(event):
    checkout_session = event.data.object
    line_items = stripe.checkout.Session.list_line_items(checkout_session.id).data

    email = (
        checkout_session.customer_email
        if checkout_session.customer_email
        else checkout_session.customer_details.email
    )

    print(checkout_session)
    print(line_items)

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
            ticket = Ticket.objects.create(gig=gig, user=user, checkout_email=email)
            print("Created ticket", ticket.id, "for", email, "for gig", gig.id)
