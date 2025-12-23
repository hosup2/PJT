# services/candidate.py

from movies.models import Movie
from .genre_parser import extract_genres_from_text
import re

STOP_WORDS = [
    "영화", "추천", "느낌", "같은", "비슷한", "유사한",
    "처럼", "의", "랑", "과", "와"
]

SIMILAR_TRIGGERS = ["같은", "비슷한", "유사한", "느낌"]

def extract_seed_title(text: str) -> str | None:
    if not text:
        return None

    # 트리거 키워드가 없으면 SIMILAR 아님
    if not any(k in text for k in SIMILAR_TRIGGERS):
        return None

    # 트리거 앞부분 우선 사용
    for k in SIMILAR_TRIGGERS:
        if k in text:
            candidate = text.split(k, 1)[0]
            break
    else:
        return None

    # 불필요 단어 제거
    for w in STOP_WORDS:
        candidate = candidate.replace(w, "")

    candidate = candidate.strip()

    # 너무 짧으면 seed 아님
    if len(candidate) < 2:
        return None

    # 장르 단어면 seed 취급 안 함
    from .genre_parser import extract_genres_from_text
    if extract_genres_from_text(candidate):
        return None

    return candidate



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
