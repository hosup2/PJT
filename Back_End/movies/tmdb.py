import requests
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_credits(tmdb_id, language="ko-KR"):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"
    params = {
        "api_key": settings.TMDB_API_KEY,
        "language": language,
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()

