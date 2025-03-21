import os
import django
import stripe
from django.utils.dateparse import parse_datetime
from django.core.files.images import ImageFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Off_Axis_Django.settings")
django.setup()

# fmt: off
from Off_Axis_App.models import (Artist, Client, User, Gig, Venue, SocialLink, GenreTag, Address, Festival, Credit, CMS)  # noqa: E402
from django.conf import settings  # noqa: E402
# fmt: on

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def populate():
    Artist.objects.all().delete()
    Client.objects.all().delete()
    User.objects.all().delete()
    # User.objects.get(username="admin").delete()
    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser(
            "admin", "sh20.team.offaxis@gmail.com", "BespokePassword"
        )
        Client.objects.create(user=admin_user, phone_number="+447123456789")
        admin_artist = add_artist("admin", "I am the admin", True)

    admin_user = User.objects.get(username="admin")
    admin_artist = Artist.objects.get(user=admin_user)

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

    # more specific artists
    aurora_engine = add_artist(
        "Aurora Engine",
        "Originally from the north east of England, "
        "Aurora Engine (aka Deborah Shaw) is a ground-breaking"
        " Edinburgh-based singer-songwriter, composer and producer. "
        "She was Single of the Week on BBC Radio Scotland flagship show "
        "The Afternoon Show and interviewed by Janice Forsyth, Artist of the "
        "Week in Scotland On Sunday featured by The Skinny for her sold out "
        "run at Edinburgh Festival Fringe (Terre for Made In Scotland) and "
        "secured airplay via BBC Radio Newcastle, Amazing Radio and more.",
        True,
        "./static/images/AuroraEngine.png",
    )

    becca_james = add_artist(
        "Becca James",
        "Becca James is a singer-songwriter from Glasgow, Scotland.",
        True,
        "./static/images/BeccaJames.png",
    )

    harry_miles_watson = add_artist(
        "Harry Miles Watson",
        "Harry Miles Watson is a singer-songwriter from Glasgow, Scotland.",
        True,
        "./static/images/HarryMilesWatson.png",
    )

    ria_timkin = add_artist(
        "Ria Timkin",
        "Ria Timkin is a singer-songwriter from Glasgow, Scotland.",
        True,
        "./static/images/RiaTimkin.png",
    )

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
        aurora_engine,
        v2,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by aurora_engine",
        True,
        "./static/images/AuroraEngine.png",
    )

    add_gig(
        becca_james,
        v1,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by Becca James",
        True,
        "./static/images/BeccaJames.png",
    )

    add_gig(
        harry_miles_watson,
        v1,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by Harry Miles Watson",
        True,
        "./static/images/HarryMilesWatson.png",
    )

    add_gig(
        ria_timkin,
        v2,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by Ria Timkin",
        True,
        "./static/images/RiaTimkin.png",
    )

    add_gig(
        a1,
        v1,
        "2022-12-12 12:00:00",
        10.00,
        100,
        "A gig by someone",
    )
    add_gig(
        a1,
        v1,
        "2022-12-12 12:00:00",
        12.00,
        50,
        "A gig by someone",
    )
    add_gig(
        a3,
        v1,
        "2022-12-12 12:00:00",
        6.00,
        20,
        "A gig by someone",
    )
    add_gig(
        a2,
        v2,
        "2022-12-12 12:00:00",
        8.00,
        35,
        "A gig by someone",
    )
    add_gig(
        a4,
        v2,
        "2022-12-12 12:00:00",
        9.00,
        15,
        "A gig by someone",
    )
    add_gig(
        a5,
        v1,
        "2022-12-12 12:00:00",
        14.00,
        40,
        "A gig by someone",
    )

    add_gig(
        admin_artist,
        v1,
        "2022-12-12 12:00:00",
        14.00,
        40,
        "test gig",
    )

    CMS.objects.all().delete()
    cms = CMS.objects.create()
    gigs = Gig.objects.all()[:4]
    cms.just_announced_gigs.add(*gigs)
    cms.featured_gigs.add(*gigs)
    cms.artist_of_the_week = a1
    cms.save()

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

    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser(
            "admin", "sh20.team.offaxis@gmail.com", "BespokePassword"
        )
        Client.objects.create(user=admin_user, phone_number="+447123456789")
        admin_artist = Artist.objects.create(
            user=admin_user, bio="I am the admin", is_approved=False
        )
        admin_artist.save()

        add_gig(
            admin_artist,
            v1,
            "2022-12-12 12:00:00",
            14.00,
            40,
            "A gig by admin",
        )
        add_gig(
            admin_artist,
            v2,
            "2022-12-12 12:00:00",
            18.00,
            100,
            "A gig by admin 2",
        )


def add_artist(
    name, bio, is_approved, image_path="./static/images/gig-placeholder.png"
):
    u = User.objects.get_or_create(username=name)[0]

    with open(image_path, "rb") as f:
        a = Artist.objects.get_or_create(
            user=u,
            bio=bio,
            is_approved=is_approved,
            profile_picture=ImageFile(f),
            credit=Credit.objects.create(balance=2.00),
        )[0]

        return a


def add_client(name, phone_number):
    u = User.objects.get_or_create(username=name)[0]
    c = Client.objects.get_or_create(user=u, phone_number=phone_number)[0]
    return c


def add_venue(name, description, venue_picture):
    a = Address.objects.create(
        line_1="123 Argyle St",
        line_2="",
        city="Glasgow",
        state_or_province="Glasgow",
        country="United Kingdom",
        post_code="G1 7DX",
    )
    v = Venue.objects.get_or_create(
        name=name, description=description, venue_picture=venue_picture, address=a
    )[0]
    return v


def add_gig(
    artist,
    venue,
    date,
    price,
    capacity,
    description,
    is_approved=True,
    gig_picture_path="./static/images/gig-placeholder.png",
):
    with open(gig_picture_path, "rb") as f:
        g = Gig.objects.get_or_create(
            artist=artist,
            venue=venue,
            date=parse_datetime(date),
            price=price,
            capacity=capacity,
            description=description,
            gig_picture=ImageFile(f),
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
