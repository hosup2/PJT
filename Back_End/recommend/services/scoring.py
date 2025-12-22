# services/scoring.py

def score_movie(movie, context):
    """
    context:
      - genres
      - query
      - feedback_map   ⭐ 추가
    """
    score = 0.0

    score += feedback_adjustment(movie, context)
    
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
