from django.shortcuts import render, get_object_or_404, redirect
from .models import Artist, Gig, Ticket
from .forms import UserForm


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
    if artist.is_approved:
        context["artist"] = artist
        return render(request, "Off_Axis/artist.html", context)
    else:
        return render(request, "Off_Axis/artist_not_approved.html", context)


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request, "Off_Axis/register.html")


def gigs(request):
    context = {}
    context["gigs"] = Gig.objects.all()

    return render(request, "Off_Axis/gigs.html", context)


def gig(request, artist, id):
    context = {}
    context["gig"] = Gig.objects.get(id=id)
    context["tickets_sold"] = Ticket.objects.filter(gig=context["gig"]).count()
    context["capacity_last_few"] = context["gig"].capacity * 0.9
    context["total_payable_amount"] = context["gig"].price + context["gig"].booking_fee

    return render(request, "Off_Axis/gig.html", context)
