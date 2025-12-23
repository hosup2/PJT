# services/scoring.py
from django.db.models import Avg


def score_movie(movie, context):
    score = 0.0

    # 1️⃣ 장르 매칭 (기본)
    genres = context.get("genres", [])
    if genres:
        matched = movie.genres.filter(name__in=genres).count()
        score += matched * 6

    
    # 3️⃣ 우리 서비스 평점
    avg_rating = movie.ratings.aggregate(
        Avg("rating")
    )["rating__avg"]
    if avg_rating:
        score += avg_rating * 4

    # 4️⃣ 리뷰 수 (신뢰도)
    review_count = movie.ratings.count()
    score += min(review_count, 10) * 1.5

    # 5️⃣ tmdb_rating (보조)
    if movie.tmdb_rating:
        score += min(movie.tmdb_rating, 8.5) * 1.2

    # 6️⃣ 유저 피드백 확장 (핵심)
    score += feedback_adjustment(movie, context)

    return score


def score_movie_seeded(movie, seed, context):
    score = 0.0

    overlap = movie.genres.filter(
        id__in=seed.genres.values_list("id", flat=True)
    ).count()
    score += overlap * 7

    if movie.release_date and seed.release_date:
        diff = abs(movie.release_date.year - seed.release_date.year)
        score += max(0, 6 - diff)

    score += feedback_adjustment(movie, context)

    if movie.tmdb_rating:
        score += min(movie.tmdb_rating, 8.5)

    return score


from recommend.models import MovieFeedback

def get_user_feedback_map(user):
    """
    return:
      {
        movie_id: "like" | "dislike"
      }
    """
    qs = MovieFeedback.objects.filter(user=user)
    return {fb.movie_id: fb.feedback for fb in qs}

def genre_similarity(movie, target):
    """
    장르 겹침 비율 (0~1)
    """
    m = set(movie.genres.values_list("id", flat=True))
    t = set(target.genres.values_list("id", flat=True))
    if not m or not t:
        return 0.0
    return len(m & t) / len(t)

def feedback_adjustment(movie, context):
    """
    좋아요 / 싫어요를 영화 단위 → 유사 영화까지 확장
    """
    user = context.get("user")
    if not user:
        return 0.0

    score = 0.0

    feedbacks = MovieFeedback.objects.filter(user=user)

    for fb in feedbacks:
        target = fb.movie

        sim = genre_similarity(movie, target)

        if sim == 0:
            continue

        if fb.feedback == "like":
            score += sim * 2.0      # 👍 유사할수록 가산
        elif fb.feedback == "dislike":
            score -= sim * 3.5      # 👎 유사할수록 감점

    return score
