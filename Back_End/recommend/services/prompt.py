# services/prompt.py

def build_recommend_prompt(movie_candidates, user_message):
    movie_text = "\n".join([
        f"{m['id']}. {m['title']} ({', '.join(m['genres'])})"
        for m in movie_candidates
    ])

    return f"""
너는 영화 추천 전문가 AI다.

사용자 요청:
"{user_message}"

아래 영화 후보 중에서
사용자 요청에 가장 잘 맞는 영화 5개를 골라라.

후보 영화 목록:
{movie_text}

아래 형식의 JSON 배열만 반환해라.
설명이나 다른 텍스트는 절대 포함하지 마라.

출력 예시:
[
  {{ "id": 1, "reason": "이유" }},
  {{ "id": 3, "reason": "이유" }}
]
"""
