import requests
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def fetch_movie_credits(tmdb_movie_id: int, language: str = "ko-KR") -> dict:
    """
    TMDB movie credits API 호출
    반환 형태: {"cast": [...], "crew": [...]}
    """
    api_key = getattr(settings, "TMDB_API_KEY", "")
    if not api_key:
        raise ValueError("TMDB_API_KEY is missing in settings")

    url = f"{TMDB_BASE_URL}/movie/{tmdb_movie_id}/credits"
    params = {"api_key": api_key, "language": language}

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()
