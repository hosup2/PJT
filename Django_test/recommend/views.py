from rest_framework.views import APIView
from rest_framework.response import Response

from .logic import recommend_movies_for_user
from .ai_client import ai_rank_movies, parse_ai_json

from django.contrib.auth import get_user_model
User = get_user_model()


def get_test_user():
    return User.objects.first()



class AIRecommendView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else get_test_user()

        # 1️⃣ rule-based 추천 (fallback용)
        candidates = recommend_movies_for_user(user, limit=10)

        # 후보가 없으면 바로 반환
        if not candidates.exists():
            return Response({"recommendations": []})

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

        # 2️⃣ AI 호출
        try:
            ai_raw = ai_rank_movies(user_profile, movie_candidates)
            content = ai_raw["choices"][0]["message"]["content"]
            parsed = parse_ai_json(content)

            # ✅ 파싱 성공
            if parsed:
                return Response({
                    "recommendations": parsed,
                    "source": "ai",
                    "token_usage": ai_raw.get("usage"),
                })

        except Exception:
            pass

        # 3️⃣ Fallback (AI 실패 시)
        return Response({
            "recommendations": movie_candidates[:5],
            "source": "rule-based",
        })

