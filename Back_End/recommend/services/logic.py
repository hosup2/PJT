# services/logic.py

from .intent import is_recommend_intent
from .prompt import build_recommend_prompt
from .ai_client import AIClient
from .summary import summarize_messages
from .genre_parser import extract_genres_from_text
from movies.models import Movie
from django.utils import timezone
from .intent import route_intent, wants_exclude_previous
from .candidate import (
    get_candidate_movies,
    extract_seed_title,
    find_seed_movie,
    get_candidates_by_seed
)
from .scoring import score_movie, score_movie_seeded, get_user_feedback_map, get_user_genre_preference_map
from .semantic import semantic_topk

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


def run_chatbot(message: str, session):
    ai = AIClient()
    intent = route_intent(message)

    # 1) SIMILAR (A 같은 영화)
    if intent == "SIMILAR":
        seed_title = extract_seed_title(message)
        seed = find_seed_movie(seed_title)
        if seed:
            candidates = get_candidates_by_seed(seed)
            if wants_exclude_previous(message):
                candidates = exclude_previous(session, candidates)

            candidates = candidates[:300]
            ranked = sorted(
                candidates,
                key=lambda m: score_movie_seeded(m, seed),
                reverse=True
            )[:5]

            save_recommend_history(session, ranked)

            return {
                "answer": f"'{seed.title}'와 비슷한 느낌으로 골라봤어요 🎬",
                "movies": [{"movie_id": m.id, "title": m.title, "reason": "유사도 기반 추천"} for m in ranked],
            }

        # seed 못 찾으면 취향 기반으로 폴백
        # (아래 PREFERENCE로 흐르게 처리)

    # 2) UPCOMING (개봉예정)
    if intent == "UPCOMING":
        from django.utils.timezone import now
        today = now().date()

        # ✅ 1. 개봉 예정 영화만 후보로
        candidates_qs = Movie.objects.filter(
            release_date__gte=today
        )

        if wants_exclude_previous(message):
            candidates_qs = exclude_previous(session, candidates_qs)

        candidates = list(candidates_qs[:300])
        if not candidates:
            return {
                "answer": "아직 추천할 만한 개봉 예정 작품이 없어요 🥲",
                "movies": [],
            }

        # ✅ 2. 의미 기반 TopK 압축
        candidate_ids = [m.id for m in candidates]
        top_ids = semantic_topk(
            message,
            top_k=60,
            candidate_ids=candidate_ids
        )
        semantic_scores = {
            mid: (60 - rank) / 60  # 0~1 점수
            for rank, mid in enumerate(top_ids)
        }


        filtered = [m for m in candidates if m.id in set(top_ids)] if top_ids else candidates

        # ✅ 3. UPCOMING 전용 점수 계산 (개인화)
        genre_pref_map = get_user_genre_preference_map(session.user)


        context = {
            "genres": extract_genres_from_text(message),
            "query": message,
            "semantic_scores": semantic_scores,
            "genre_pref_map": genre_pref_map,
        }


        scored = [
            {
                "movie": m,
                "score": score_upcoming_movie(m, context)
            }
            for m in filtered
        ]

        scored.sort(key=lambda x: x["score"], reverse=True)
        top_movies = scored[:2]

        save_recommend_history(session, [item["movie"] for item in top_movies])

        return {
            "answer": "말씀해주신 취향을 바탕으로 개봉 예정 작품을 골라봤어요 🎟️",
            "movies": [
                {
                    "movie_id": item["movie"].id,
                    "title": item["movie"].title,
                    "reason": f"기대 점수 {item['score']:.1f}",
                }
                for item in top_movies
            ],
        }

    if intent == "PREFERENCE":
        candidates_qs = get_candidate_movies(session.user, message, limit=None)

        if wants_exclude_previous(message):
            candidates_qs = exclude_previous(session, candidates_qs)

        candidates = list(candidates_qs[:300])  # 일단 300개까지
        if not candidates:
            fallback = Movie.objects.order_by("-tmdb_rating")[:5]
            save_recommend_history(session, list(fallback))
            return {
                "answer": "조건에 맞는 영화가 없어서 인기작으로 추천할게요 🎬",
                "movies": [{"movie_id": m.id, "title": m.title, "reason": "인기/평점 기반"} for m in fallback],
            }

        # ✅ 1) 의미 기반으로 후보 300개 중 topK를 먼저 뽑아 “유사한 것만 남김”
        candidate_ids = [m.id for m in candidates]
        top_ids = semantic_topk(message, top_k=60, candidate_ids=candidate_ids)  # 60개로 압축
        top_id_set = set(top_ids) if top_ids else set(candidate_ids)

        filtered = [m for m in candidates if m.id in top_id_set]
        if not filtered:
            filtered = candidates  # 안전장치

        # ✅ 2) 그 다음 기존 score_movie로 최종 정렬 (너의 로직 살림)
        feedback_map = get_user_feedback_map(session.user)
        context = {
            "genres": extract_genres_from_text(message),
            "query": message,
            "feedback_map": feedback_map,
            "context_user": session.user,
        }

        scored = [{"movie": m, "score": score_movie(m, context)} for m in filtered]
        scored.sort(key=lambda x: x["score"], reverse=True)
        top_movies = scored[:5]

        save_recommend_history(session, [item["movie"] for item in top_movies])

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



    # 4) CHITCHAT (일반 대화)
    messages = build_chat_context(session, message)
    reply = safe_chat(ai, messages)
    return {"answer": reply, "movies": []}


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

def build_chat_context(session, user_message, limit=10):
    messages = [{
        "role": "system",
        "content": (
            "너는 영화 추천 챗봇 MIA다.\n"
            f"[대화 요약]\n{session.summary or ''}\n"
            "한국어로 답변해."
        )
    }]

    recent = session.messages.order_by("-created_at")[:limit]
    for m in reversed(recent):
        messages.append({"role": m.role, "content": m.content})

    messages.append({"role": "user", "content": user_message})
    return messages


def safe_chat(ai_client, messages):
    try:
        return ai_client.chat(messages)
    except Exception:
        return "지금은 잠시 응답이 불안정해요. 같은 질문을 한 번만 더 보내줄래요?"


def save_recommend_history(session, movies):
    session.last_recommended_movie_ids = [m.id for m in movies]
    session.save(update_fields=["last_recommended_movie_ids"])

def exclude_previous(session, queryset):
    ids = session.last_recommended_movie_ids or []
    if ids:
        return queryset.exclude(id__in=ids)
    return queryset

def score_upcoming_movie(movie, context):
    score = 0.0

    # 1️⃣ 장르 점수
    user_genres = context.get("genres", [])
    if user_genres:
        movie_genres = {g.name for g in movie.genres.all()}
        matched = len(set(user_genres) & movie_genres)
        score += (matched / len(user_genres)) * 40

    # 2️⃣ 의미 점수 (semantic_topk 기반)
    semantic_scores = context.get("semantic_scores", {})
    score += semantic_scores.get(movie.id, 0) * 35

    # 3️⃣ 사용자 취향 보정
    genre_pref_map = context.get("genre_pref_map", {})

    for g in movie.genres.all():
        score += genre_pref_map.get(g.id, 0) * 15


    # 4️⃣ 개봉일 보정
    if movie.release_date:
        days = (movie.release_date - timezone.now().date()).days
        if days < 30:
            score += 10
        elif days < 90:
            score += 5

    return score

