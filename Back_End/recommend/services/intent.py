# services/intent.py

RECOMMEND_KEYWORDS = [
    # 직접 요청
    "추천", "골라", "찾아", "알려줘",
    "뭐 볼까", "뭐볼까", "뭐 보지", "뭐보지",
    "볼만한", "볼만한거",

    # 취향 기반
    "취향", "내 스타일", "내취향",
    "비슷한 영화", "같은 영화",

    # 완곡한 표현
    "보고 싶은", "보고싶은",
    "재밌는", "좋은 영화",
]


def is_recommend_intent(message: str) -> bool:
    if not message:
        return False
    return any(k in message for k in RECOMMEND_KEYWORDS)


SIMILAR_KEYWORDS = [
    "같은", "비슷한", "유사한",
    "처럼", "느낌",
    "비슷한 영화",
    "○○ 같은",
    "○○ 느낌",
]

UPCOMING_KEYWORDS = [
    "개봉", "개봉예정",
    "예정", "곧", "곧 나오는",
    "나올", "출시",
    "upcoming", "신작",
    "이번달", "다음달",
]


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

EXCLUDE_PREV_KEYWORDS = [
    "말고", "다른", "제외", "빼고",
    "말고 추천", "다른거",
    "이미 봤어",
    "봤어", "본거",
]


def wants_exclude_previous(message: str) -> bool:
    return any(k in message for k in EXCLUDE_PREV_KEYWORDS)
