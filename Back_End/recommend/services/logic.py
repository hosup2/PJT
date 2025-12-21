# services/logic.py

from .intent import is_recommend_intent
from .candidate import get_candidate_movies
from .prompt import build_recommend_prompt
from .ai_client import AIClient
from .summary import summarize_messages
from .scoring import score_movie
from .genre_parser import extract_genres_from_text
from movies.models import Movie


SUMMARY_TRIGGER_COUNT = 8
RECENT_MESSAGE_COUNT = 4

def update_session_summary(session):
    messages = session.messages.order_by("-created_at")[:SUMMARY_TRIGGER_COUNT]

    if messages.count() < SUMMARY_TRIGGER_COUNT:
        return

    new_summary = summarize_messages(
        reversed(messages),
        prev_summary=session.summary
    )

    session.summary = new_summary
    session.save()


def build_chat_messages(session):
    messages = [
        {
            "role": "system",
            "content": (
                "너는 영화 서비스 MIA의 친절한 챗봇이다. "
                "이전 대화를 기억하고 자연스럽게 이어서 대답해라."
            )
        }
    ]

    if session.summary:
        messages.append({
            "role": "system",
            "content": f"지금까지의 대화 요약:\n{session.summary}"
        })

    recent_messages = session.messages.order_by("-created_at")[:RECENT_MESSAGE_COUNT]

    for msg in reversed(recent_messages):
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    return messages


def run_chatbot(user, message, session):
    if is_recommend_intent(message):
        return run_recommendation(user, message, session)
    else:
        return run_general_chat(message, session)


def run_general_chat(message, session):
    ai = AIClient()

    messages = build_chat_messages(session)
    messages.append({
        "role": "user",
        "content": message
    })

    answer = ai.chat(messages)

    return {
        "answer": answer,
        "movies": [],
    }



def run_recommendation(user, message, session):
    genres = extract_genres_from_text(message)

    candidates = get_candidate_movies(
        user=user,
        query=message,
        limit=50
    )

    if not candidates.exists():
        fallback = Movie.objects.order_by("-tmdb_rating")[:5]

        return {
            "answer": "비슷한 인기 영화들을 추천해드릴게요 😊",
            "movies": [
                {
                    "movie_id": m.id,
                    "title": m.title,
                }
                for m in fallback
            ],
        }


    context = {
        "genres": genres,
        "query": message,
    }

    scored = []
    for movie in candidates:
        scored.append({
            "movie": movie,
            "score": score_movie(movie, context),
        })

    # 🔥 점수 기준 정렬
    scored.sort(key=lambda x: x["score"], reverse=True)

    top_movies = scored[:5]

    return {
        "answer": "이런 영화들이 잘 어울릴 것 같아요 🎬",
        "movies": [
            {
                "movie_id": item["movie"].id,
                "title": item["movie"].title,
                "reason": f"추천 점수 {item['score']:.1f}",
            }
            for item in top_movies
        ],
    }

