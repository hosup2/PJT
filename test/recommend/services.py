from .models import UserFavoriteMovie, UserWatchedMovie, UserPreference, RecommendationResult

def calculate_user_preferences(user):
    """
    1. 유저가 좋아한 영화 가져오기
    2. TMDB에서 장르/감독/배우 정보 가져오기
    3. 빈도수 기반으로 선호도 계산
    4. UserPreference에 저장
    """
    # (나중에 채울 로직 — 기본 틀만)
    pass


def generate_recommendation(user):
    """
    1. UserPreference 기반으로 추천 계산
    2. 이미 본 영화(UserWatchedMovie)는 제외
    3. 결과 RecommendationResult로 저장
    """
    # (나중에 채울 로직)
    pass
