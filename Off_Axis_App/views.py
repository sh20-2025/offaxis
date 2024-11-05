from django.shortcuts import render, get_object_or_404
from .models import Artist

# Create your views here.


def components(request):
    return render(
        request,
        "components/index.html",
        {
            "test_options": [
                {"label": "United States", "value": "US"},
                {"label": "Canada", "value": "CA"},
                {"label": "Mexico", "value": "MX"},
            ]
        },
    )
    
def artist_profile(request, slug):
    artist_profile_page = get_object_or_404(Artist, slug=slug)
    if (artist_profile_page.is_approved == True):
        return render(request, 'artist_profile.html', {'artist_profile': artist_profile_page})
    else:
        return render(request, 'artist_not_approved.html', {'artist_profile': artist_profile_page})
