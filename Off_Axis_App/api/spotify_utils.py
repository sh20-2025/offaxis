from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import re


def get_spotify_client():
    """Initialize and return a Spotify client."""
    auth_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
    return Spotify(auth_manager=auth_manager)


def extract_spotify_artist_id(spotify_url):
    """Extract artist ID from Spotify URL."""
    # Handle different Spotify URL formats
    pattern = r"artist\/([a-zA-Z0-9]+)"
    match = re.search(pattern, spotify_url)
    return match.group(1) if match else None


def get_artist_top_track(spotify_url):
    """Get the top track for an artist using their Spotify URL."""
    try:
        spotify = get_spotify_client()
        artist_id = extract_spotify_artist_id(spotify_url)

        if not artist_id:
            return None

        # Get top tracks (market parameter is required)
        top_tracks = spotify.artist_top_tracks(artist_id, country="GB")

        if not top_tracks["tracks"]:
            return None

        top_track = top_tracks["tracks"][0]

        return {
            "name": top_track["name"],
            "preview_url": top_track["preview_url"],
            "external_url": top_track["external_urls"]["spotify"],
            "album_name": top_track["album"]["name"],
            "album_image": (
                top_track["album"]["images"][0]["url"]
                if top_track["album"]["images"]
                else None
            ),
        }
    except Exception as e:
        print(f"Error fetching top track: {e}")
        return None
