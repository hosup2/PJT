# services/intent.py

RECOMMEND_KEYWORDS = [
    "추천", "골라", "뭐 볼까", "뭐보지",
    "비슷한 영화", "취향"
]

def is_recommend_intent(message: str) -> bool:
    if not message:
        return False
    return any(k in message for k in RECOMMEND_KEYWORDS)


SIMILAR_KEYWORDS = ["같은", "비슷한", "처럼", "느낌", "유사한"]
UPCOMING_KEYWORDS = ["개봉", "예정", "upcoming", "개봉예정", "곧 나오는", "나올"]

def route_intent(message: str) -> str:
    """
    CHITCHAT | SIMILAR | UPCOMING | PREFERENCE
    """
    if is_recommend_intent(message):
        if any(k in message for k in SIMILAR_KEYWORDS):
            return "SIMILAR"
        if any(k in message for k in UPCOMING_KEYWORDS):
            return "UPCOMING"
        return "PREFERENCE"
    return "CHITCHAT"

EXCLUDE_PREV_KEYWORDS = ["말고", "다른", "제외", "빼고"]

def wants_exclude_previous(message: str) -> bool:
    return any(k in message for k in EXCLUDE_PREV_KEYWORDS)
