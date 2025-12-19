# services/logic.py

from .intent import is_recommend_intent
from .candidate import get_candidate_movies
from .prompt import build_recommend_prompt
from .ai_client import AIClient


def run_chatbot(user, message):
    """
    단일 진입점
    """
    if is_recommend_intent(message):
        return run_recommendation(user, message)
    else:
        return run_general_chat(message)


def run_general_chat(message):
    ai = AIClient()

    prompt = f"""
너는 영화 서비스 MIA의 친절한 챗봇이다.
영화 추천, 영화 정보, 서비스 안내를 자연스럽게 대답해라.

사용자 질문:
{message}
"""

    answer = ai.chat(prompt)

    return {
        "answer": answer,
        "movies": [],
    }


def run_recommendation(user, message):
    """
    🔥 온보딩/취향 없이 동작하는 추천
    """

    # 1️⃣ 1차: 메시지 기반 후보
    candidates = get_candidate_movies(
        user=user,
        query=message,
        limit=10
    )

    # 2️⃣ 2차 fallback (아무것도 없을 때)
    if not candidates.exists():
        candidates = get_candidate_movies(
            user=user,
            query=None,
            limit=10
        )

    if not candidates.exists():
        return {
            "answer": "아직 추천할 영화 데이터가 부족해요 😢",
            "movies": [],
        }

    # 3️⃣ 후보 정리
    movie_candidates = [
        {
            "id": m.id,
            "title": m.title,
            "genres": [g.name for g in m.genres.all()],
        }
        for m in candidates
    ]

    # 4️⃣ 프롬프트 (유저 취향 제거)
    prompt = build_recommend_prompt(
        movie_candidates=movie_candidates,
        user_message=message,
    )


    ai = AIClient()

    ranked = ai.rank_movies(prompt)
    # movie_candidates를 dict로 매핑
    movie_map = {m["id"]: m for m in movie_candidates}

    movies = []
    for m in ranked:
        movie_id = m.get("id")
        if movie_id in movie_map:
            movies.append({
                "movie_id": movie_id,
                "title": movie_map[movie_id]["title"],
                "reason": m.get("reason", ""),
            })


    return {
        "answer": "이런 영화들이 잘 어울릴 것 같아요 🎬",
        "movies": movies,
    }
