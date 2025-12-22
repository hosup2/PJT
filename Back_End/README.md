## Back_End Test

## 12.22 
- 커뮤니티(게시판) 기능 추가
  - `community` 앱 생성
  - 게시글(`Post`) 및 댓글(`Comment`) 모델 정의
  - 게시글, 댓글 CRUD API 엔드포인트 구현
    - `GET, POST /community/posts/`
    - `GET, PUT, DELETE /community/posts/<int:pk>/`
    - `GET, POST /community/posts/<int:post_pk>/comments/`
    - `GET, PUT, DELETE /community/posts/<int:post_pk>/comments/<int:pk>/`
  - 작성자만 수정/삭제 가능하도록 권한 설정

## 12.22
- 챗봇 이전대화 기억, 사용자 피드백 수용, scoring구체화

## 12.20
- 챗봇 시스템 개선 ( 장르 텍스트 매칭해서 해당 장르에 candidate하기)

## 12.19
- 챗봇 시스템 구현 + 세션 구현 (TEST 통과 가끔 session id생성 전 session을 불러오려해서 오류 발생)

## 12.18
- 챗봇 시스템 구현 (Test 전)

## 12.15 
- 영화 정보 받아오는 과정에서 장르정보 누락 수정
- 영화 디테일을 tmdb api를 불러와서 반환

## 12.13
- 영화 리뷰, 평점 기능
- 유저간 팔로우 기능
- tmdb api에 데이터 요청기능

## 12.11
- Movie / FeaturedMovie 데이터
- TMDB Top_Rated 데이터 200개 수집 기능
- 자동으로 20위 내 영화 FeaturedMovie 등록

## 12.09
- Movie - Model, Serializer 수정, 
- 영화목록 조회, 영화 디테일 조회 기능 구현  
- 페이지네이션 적용
- 영화 검색 기능 구현

## 12.07
- API 테스트용 seed_data 생성
- GMS를 이용해 gpt-4o-mini로 영화 추천 logic 구현 (성공)
- users 정보 CRUD 구현 (성공)
- JWT token 인증

## 12.06
- user관련 api 구현

    -> 선호 장르 조회,저장 / 좋아하는 영화 추가,삭제/ 이미 시청한 영화 저장 /

- Test용 추천로직 구현

    -> 해당 유저의 선호 장르 기반 추천

## 12.05
- TMDB_API 연결 및 ERD기반 db설계