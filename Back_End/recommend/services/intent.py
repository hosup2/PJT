# services/intent.py

RECOMMEND_KEYWORDS = [
    "추천", "골라", "뭐 볼까", "뭐보지",
    "비슷한 영화", "취향"
]

def is_recommend_intent(message: str) -> bool:
    if not message:
        return False
    return any(k in message for k in RECOMMEND_KEYWORDS)
