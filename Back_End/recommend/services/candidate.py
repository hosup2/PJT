from movies.models import Movie


def get_candidate_movies(user, query, limit=10):
    qs = Movie.objects.all()

    # 1️⃣ 쿼리에서 장르 키워드 추출 (초기엔 단순 매칭)
    if "우주" in query or "SF" in query:
        qs = qs.filter(genres__name__icontains="Science Fiction")

    # 2️⃣ 유저 선호 반영
    liked_genres = user.favorite_genres.all()
    if liked_genres.exists():
        qs = qs.filter(genres__in=liked_genres)

    return qs.distinct().order_by('-tmdb_rating')[:limit]
