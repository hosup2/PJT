from movies.models import Movie
from users.models import UserPreference, WatchedMovie

def recommend_movies_for_user(user, limit=20):
    """
    1. 사용자의 선호 장르 조회
    2. 해당 장르의 영화 필터링
    3. 시청한 영화 제외
    """

    prefs = UserPreference.objects.filter(user=user).first()

    # 선호 장르 없으면 빈 QuerySet 반환
    if not prefs:
        return Movie.objects.none()

    favorite_genres = prefs.favorite_genres.all()

    qs = (
        Movie.objects
        .filter(genres__in=favorite_genres)
        .exclude(
            id__in=WatchedMovie.objects.filter(user=user)
            .values_list("movie_id", flat=True)
        )
        .distinct()
    )

    return qs[:limit]
