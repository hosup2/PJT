# services/candidate.py

from movies.models import Movie
from .genre_parser import extract_genres_from_text

def get_candidate_movies(user, query, limit=50):
    qs = Movie.objects.all()

    genres = extract_genres_from_text(query)
    print("🎯 extracted genres:", genres)  # ✅ 디버깅

    if genres:
        qs = qs.filter(genres__name__in=genres)

    qs = qs.order_by("-tmdb_rating").distinct()

    print("🎬 candidate count:", qs.count())  # ✅ 디버깅
    return qs[:limit]
