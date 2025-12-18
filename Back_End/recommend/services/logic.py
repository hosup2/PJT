from .candidate import get_candidate_movies
from .prompt import build_rank_prompt
from .ai_client import AIClient


def run_ai_recommendation(user):
    candidates = get_candidate_movies(user, limit=10)

    if not candidates.exists():
        return {"source": "none", "recommendations": []}

    movie_candidates = [
        {
            "id": m.id,
            "title": m.title,
            "genres": [g.name for g in m.genres.all()],
        }
        for m in candidates
    ]

    user_profile = {
        "genres": list(
            user.userpreference.favorite_genres.values_list("name", flat=True)
        ) if hasattr(user, "userpreference") else [],
        "recent_genres": [],
    }

    prompt = build_rank_prompt(user_profile, movie_candidates)
    ai = AIClient()

    try:
        ranked = ai.rank_movies(prompt)
        return {"source": "ai", "recommendations": ranked}
    except Exception:
        return {
            "source": "rule-based",
            "recommendations": movie_candidates[:5]
        }
