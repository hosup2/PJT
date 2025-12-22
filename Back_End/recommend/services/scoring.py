# services/scoring.py

def score_movie(movie, context):
    """
    context:
      - genres
      - query
      - feedback_map   ⭐ 추가
    """
    score = 0.0

    # 1️⃣ 장르 매칭
    if context["genres"]:
        movie_genres = {g.name for g in movie.genres.all()}
        matched = movie_genres & set(context["genres"])
        score += len(matched) * 3.0

    # 2️⃣ 평점
    if movie.tmdb_rating:
        score += (movie.tmdb_rating / 10) * 2.0

    # 3️⃣ 인기 보정
    if hasattr(movie, "vote_count") and movie.vote_count:
        score += min(movie.vote_count / 10000, 1.5)

    # 4️⃣ 쿼리 키워드
    q = context["query"].lower()
    if q in (movie.title or "").lower():
        score += 1.5
    if q in (movie.overview or "").lower():
        score += 1.0

    # ==========================
    # 🔥 5️⃣ 사용자 피드백 반영
    # ==========================
    feedback_map = context.get("feedback_map", {})
    fb = feedback_map.get(movie.id)

    if fb == "like":
        score += 3.0        # 👍 강력 가중치
    elif fb == "dislike":
        score -= 5.0        # 👎 강력 패널티

    return score


def score_movie_seeded(movie, seed) -> float:
    score = 0.0

    m_genres = set(movie.genres.values_list("id", flat=True))
    s_genres = set(seed.genres.values_list("id", flat=True))
    score += len(m_genres & s_genres) * 3.0

    if movie.release_date and seed.release_date:
        diff = abs(movie.release_date.year - seed.release_date.year)
        score += max(0.0, 3.0 - diff * 0.3)

    if movie.runtime and seed.runtime:
        diff = abs(movie.runtime - seed.runtime)
        score += max(0.0, 2.0 - diff / 60)

    score += (movie.tmdb_rating or 0) * 0.6
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
