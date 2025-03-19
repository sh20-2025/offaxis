from Off_Axis_App.models import Ticket
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import os


def send_ticket_email(ticket: Ticket):
    context = {
        "ticket": ticket,
        "artist": ticket.gig.artist,
        "gig": ticket.gig,
        "qr_code_src": f"{os.getenv("TRUSTED_ORIGIN")}{ticket.qr_code.url}",
    }

    # First, render the plain text content.
    text_content = render_to_string(
        "emails/ticket.html",
        context=context,
    )

    # Secondly, render the HTML content.
    html_content = render_to_string("emails/ticket.html", context=context)

    # Then, create a multipart email instance.
    msg = EmailMultiAlternatives(
        f"You're going to see {ticket.gig.artist.user.username} in {
            ticket.gig.venue.address.city}!",
        text_content,
        settings.EMAIL_HOST_USER,
        [ticket.checkout_email],
        headers={"Reply-To": settings.EMAIL_HOST_USER},
    )

    # Lastly, attach the HTML content to the email instance and send.
    msg.attach_alternative(html_content, "text/html")
    msg.send()
