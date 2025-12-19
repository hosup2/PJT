# services/candidate.py

from movies.models import Movie
from django.db.models import Q

def get_candidate_movies(user, query, limit=10):
    qs = Movie.objects.all()

    # 🔍 자연어 query 기반 필터
    if query:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        )

    # ⭐ 온보딩 있으면 보너스로 장르 반영
    if hasattr(user, "userpreference"):
        genres = user.userpreference.favorite_genres.all()
        if genres.exists():
            qs = qs.filter(genres__in=genres)

    return qs.distinct()[:limit]
