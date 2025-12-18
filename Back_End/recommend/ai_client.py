import requests
from django.conf import settings
import json
import re

def ai_rank_movies(user_profile, movie_candidates):

    movie_text = "\n".join([
        f"{m['id']}. {m['title']} ({', '.join(m['genres'])})"
        for m in movie_candidates
    ])

    prompt = f"""
사용자 선호 장르: {', '.join(user_profile['genres'])}
최근 시청 장르: {', '.join(user_profile['recent_genres'])}

후보 영화 목록:
{movie_text}

위 사용자에게 가장 잘 맞는 영화 5개를
중요도 순으로 JSON 배열만 반환하세요.

출력 예시:
[
  {{ "movie_id": 1, "reason": "이유" }}
]
"""

    payload = {
        "model": settings.GMS_MODEL,  # gpt-4o-mini
        "messages": [
            {"role": "system", "content": "너는 영화 추천 전문가 AI다."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    response = requests.post(
        settings.GMS_API_URL,
        headers={
            "Authorization": f"Bearer {settings.GMS_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=10,
    )

    response.raise_for_status()
    return response.json()




def parse_ai_json(content: str):
    """
    AI가 ```json ... ``` 형태로 응답한 문자열을
    실제 Python list/dict로 변환
    """
    try:
        cleaned = re.sub(r"```json|```", "", content).strip()
        return json.loads(cleaned)
    except Exception as e:
        return None
