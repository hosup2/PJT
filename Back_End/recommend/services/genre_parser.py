# services/genre_parser.py

GENRE_KEYWORDS = {
    "공포": ["공포"],
    "무서운": ["공포"],
    "호러": ["공포"],

    "로맨스": ["로맨스"],
    "사랑": ["로맨스"],
    "연애": ["로맨스"],

    "코미디": ["코미디"],
    "웃긴": ["코미디"],
    "유머": ["코미디"],

    "액션": ["액션"],
    "박진감": ["액션"],

    "스릴러": ["스릴러"],
    "긴장감": ["스릴러"],

    "SF": ["SF"],
    "공상과학": ["SF"],

    "판타지": ["판타지"],

    "드라마": ["드라마"],

    "가족": ["가족"],

    "애니": ["애니메이션"],
    "애니메이션": ["애니메이션"],

    "범죄": ["범죄"],
    "수사": ["범죄"],

    "전쟁": ["전쟁"],

    "음악": ["음악"],

    "미스터리": ["미스터리"],

    "다큐": ["다큐멘터리"],
    "다큐멘터리": ["다큐멘터리"],

    "서부": ["서부"],

    "역사": ["역사"],

    "모험": ["모험"],
}

def extract_genres_from_text(text: str) -> list[str]:
    """
    사용자 입력에서 장르 키워드 추출
    """
    if not text:
        return []

    text = text.lower()
    genres = set()

    for keyword, mapped_genres in GENRE_KEYWORDS.items():
        if keyword in text:
            for g in mapped_genres:
                genres.add(g)

    return list(genres)
