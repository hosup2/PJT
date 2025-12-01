import requests
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_URL = "https://api.themoviedb.org/3"

def get_upcoming_movies(page=1):
    url = f"{BASE_URL}/movie/upcoming"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "ko-KR",
        "page": page
    }
    response = requests.get(url, params=params)
    return response.json()
