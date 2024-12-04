import os
import django
import stripe
from django.utils.dateparse import parse_datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Off_Axis_Django.settings")
django.setup()

# fmt: off
from Off_Axis_App.models import (Artist, Client, User, Gig, Venue, SocialLink, GenreTag, Address, Festival,)  # noqa: E402
from django.conf import settings  # noqa: E402
# fmt: on

stripe.api_key = settings.STRIPE_SECRET_KEY


def populate():
    Artist.objects.all().delete()

    add_genre_tag("Rock")
    add_genre_tag("Pop")
    add_genre_tag("Rap")
    add_genre_tag("Country")
    add_genre_tag("Jazz")
    add_genre_tag("Soul")
    add_genre_tag("Blues")
    add_genre_tag("Folk")
    add_genre_tag("Indie")
    add_genre_tag("Punk")

    a1 = add_artist("Ed Armeson", "I am a musician", True)
    a2 = add_artist("Precious Ink", "I am a musician", True)
    a3 = add_artist("Sub Violet", "I am a musician", True)
    a4 = add_artist("Deltamaniac", "I am a musician", True)
    a5 = add_artist("The Demographic", "I am a musician", True)
    add_artist("The Sun Day", "I am a musician", False)
    add_artist("Dear Heather", "I am a musician", False)

    add_client("John Doe", "555-555-5555")
    add_client("Jane Doe", "555-555-5555")
    add_client("Bob Smith", "555-555-5555")
    add_client("Sally Smith", "555-555-5555")

    v1 = add_venue(
        "The Blue Note",
        "A venue in Columbia, MO",
        "https://www.glasgowworld.com/jpim-static/image/2024/03/12/9/06/GettyImages-464461345.jpg.jpg?crop=3:2,smart&trim=&width=1200&auto=webp&quality=75",
    )
    v2 = add_venue(
        "The Hydro",
        "A venue in Glasgow, Scotland",
        "https://www.glasgowworld.com/jpim-static/image/2024/03/12/9/06/GettyImages-464461345.jpg.jpg?crop=3:2,smart&trim=&width=1200&auto=webp&quality=75",
    )

    gigs = Gig.objects.all()
    for gig in gigs:
        if gig.stripe_product_id is not None:
            try:
                stripe.Product.modify(gig.stripe_product_id, active=False)
            except Exception as e:
                print("Failed to archive product", gig.stripe_product_id)
                print(e)
                pass

    Gig.objects.all().delete()

    add_gig(
        a1,
        v1,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )
    add_gig(
        a1,
        v1,
        "2022-12-12 12:00:00",
        12.00,
        50,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )
    add_gig(
        a3,
        v1,
        "2022-12-12 12:00:00",
        6.00,
        20,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )
    add_gig(
        a2,
        v2,
        "2022-12-12 12:00:00",
        8.00,
        35,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )
    add_gig(
        a4,
        v2,
        "2022-12-12 12:00:00",
        9.00,
        15,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )
    add_gig(
        a5,
        v1,
        "2022-12-12 12:00:00",
        14.00,
        40,
        "A gig by someone",
        "/static/images/gig-placeholder.png",
    )

    Festival.objects.all().delete()

    add_festival(
        "Sound Of Belfast",
        "Sound of Belfast is an annual festival celebrating new music talent and creativity from across Northern Ireland.",
        "2024-11-25",
        "2024-11-01",
        [a1, a2, a3],
        "/static/images/festival-placeholder.png",
        "https://www.youtube.com/embed/wtOvDo1Mrh8?si=wFSIWqES72Fi3Fi0",
    )
    add_festival(
        "Output",
        "Output festival is Ireland’s biggest one-day music conference, taking place on Tuesday 12 November 2024 to coincide with",
        "2024-11-10",
        "2024-11-20",
        [a1, a3, a4],
        "/static/images/festival-placeholder.png",
        "https://www.youtube.com/embed/wtOvDo1Mrh8?si=wFSIWqES72Fi3Fi0",
    )
    add_festival(
        "Unconvention",
        "ounded in 2008, Un-Convention is a series of music conferences, showcases and events",
        "2024-10-05",
        "2024-10-16",
        [a2, a4, a5],
        "/static/images/festival-placeholder.png",
        "https://www.youtube.com/embed/wtOvDo1Mrh8?si=wFSIWqES72Fi3Fi0",
    )


def add_artist(name, bio, is_approved):
    u = User.objects.get_or_create(username=name)[0]
    a = Artist.objects.get_or_create(
        user=u,
        bio=bio,
        is_approved=is_approved,
        profile_picture_url="/static/images/gig-placeholder.png",
    )[0]
    return a


def add_client(name, phone_number):
    u = User.objects.get_or_create(username=name)[0]
    c = Client.objects.get_or_create(user=u, phone_number=phone_number)[0]
    return c


def add_venue(name, description, venue_photo_url):
    a = Address.objects.create(
        line_1="123 Argyle St",
        line_2="",
        city="Glasgow",
        state_or_province="Glasgow",
        country="United Kingdom",
        post_code="G1 7DX",
    )
    v = Venue.objects.get_or_create(
        name=name, description=description, venue_photo_url=venue_photo_url, address=a
    )[0]
    return v


def add_gig(
    artist, venue, date, price, capacity, description, gig_photo_url, is_approved=True
):
    g = Gig.objects.get_or_create(
        artist=artist,
        venue=venue,
        date=parse_datetime(date),
        price=price,
        capacity=capacity,
        description=description,
        gig_photo_url=gig_photo_url,
        is_approved=is_approved,
    )[0]

    if is_approved:
        g.approve()

    return g


def add_genre_tag(tag):
    return GenreTag.objects.get_or_create(tag=tag)[0]


def add_festival(
    name,
    description,
    start_date,
    end_date,
    artists,
    festival_photo_url,
    youtube_video_url,
):
    f = Festival.objects.get_or_create(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        festival_photo_url=festival_photo_url,
        youtube_video_url=youtube_video_url,
    )[0]
    f.artists.add(*artists)
    return f


# Start execution here!
if __name__ == "__main__":
    print("Populating database...")
    populate()
