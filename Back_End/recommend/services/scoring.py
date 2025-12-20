# services/scoring.py

def score_movie(movie, context):
    """
    movie: Movie instance
    context: {
        "genres": [...],
        "query": str
    }
    """
    score = 0.0

    # 1️⃣ 장르 매칭 점수 (가장 중요)
    if context["genres"]:
        movie_genres = {g.name for g in movie.genres.all()}
        matched = movie_genres & set(context["genres"])
        score += len(matched) * 3.0   # 가중치 큼

    # 2️⃣ 평점 점수 (정규화)
    if movie.tmdb_rating:
        score += (movie.tmdb_rating / 10) * 2.0

    # 3️⃣ 인기 보정 (너무 센 영향 방지)
    if hasattr(movie, "vote_count") and movie.vote_count:
        score += min(movie.vote_count / 10000, 1.5)

    # 4️⃣ 쿼리 키워드가 제목/설명에 있으면 가산
    q = context["query"].lower()
    if q in (movie.title or "").lower():
        score += 1.5
    if q in (movie.overview or "").lower():
        score += 1.0

    return score
