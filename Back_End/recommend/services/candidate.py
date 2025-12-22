# services/candidate.py

from movies.models import Movie
from .genre_parser import extract_genres_from_text

def extract_seed_title(text: str) -> str | None:
    for k in ["같은", "비슷한", "처럼", "느낌", "유사한"]:
        if k in text:
            left = text.split(k, 1)[0]
            left = left.replace("영화", "").replace("추천", "").strip()
            return left if left else None
    return None


def get_candidate_movies(user, query, limit=50):
    qs = Movie.objects.all()

    genres = extract_genres_from_text(query)
    print("🎯 extracted genres:", genres)  # ✅ 디버깅

    if genres:
        qs = qs.filter(genres__name__in=genres)

    qs = qs.order_by("-tmdb_rating").distinct()

    print("🎬 candidate count:", qs.count())  # ✅ 디버깅
    return qs

def find_seed_movie(seed_title: str):
    if not seed_title:
        return None
    return (
        Movie.objects
        .filter(title__icontains=seed_title)
        .order_by("-tmdb_rating")
        .first()
    )

def get_candidates_by_seed(seed: Movie, limit=300):
    genre_ids = seed.genres.values_list("id", flat=True)

    qs = (
        Movie.objects
        .filter(genres__in=genre_ids)
        .exclude(id=seed.id)
        .distinct()
    )

    # 연도 근접(옵션)
    if seed.release_date:
        y = seed.release_date.year
        qs = qs.filter(release_date__year__gte=y-8, release_date__year__lte=y+8)

    return qs
