def build_rank_prompt(user_profile, movie_candidates):
    movie_text = "\n".join([
        f"{m['id']}. {m['title']} ({', '.join(m['genres'])})"
        for m in movie_candidates
    ])

    return f"""
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
