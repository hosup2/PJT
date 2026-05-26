# MIA

> AI 기반 영화 추천 플랫폼 — TMDB 영화 데이터를 기반으로 AI 챗봇·시맨틱 검색·실시간 채팅을 한곳에서 제공합니다.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.16-ff1709)](https://www.django-rest-framework.org/)
[![Vue](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vuedotjs)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite)](https://vitejs.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)](https://www.sqlite.org/)
[![Channels](https://img.shields.io/badge/Django_Channels-4.3-092E20)](https://channels.readthedocs.io/)

---

## 목차

- [프로젝트 소개](#프로젝트-소개)
- [핵심 기능](#핵심-기능)
- [시스템 아키텍처](#시스템-아키텍처)
- [AI 추천 흐름](#ai-추천-흐름)
- [기술 스택](#기술-스택)
- [디렉토리 구조](#디렉토리-구조)
- [Quick Start](#quick-start)
- [환경변수](#환경변수)
- [API 개요](#api-개요)
- [팀원](#팀원)

---

## 프로젝트 소개

영화를 고를 때 "오늘 뭐 볼까?"라는 고민을 해결하기 어렵습니다. 장르별 목록, 평점 순위만으로는 취향에 꼭 맞는 영화를 찾기 어렵기 때문입니다.

**MIA (Movie Intelligence Assistant)** 는 이 문제를 해결합니다.

- **AI 챗봇**: GMS 프록시(GPT-4.1-mini)로 구동되는 챗봇이 자연어 대화를 통해 맞춤 영화를 추천합니다.
- **시맨틱 검색**: `sentence-transformers` 임베딩으로 의미 유사도 기반 영화를 검색합니다.
- **TMDB 연동**: 최신 영화 정보(포스터·평점·출연진·감독)를 TMDB API에서 실시간으로 가져옵니다.
- **소셜 기능**: 팔로우·리뷰·커뮤니티·영화별 실시간 채팅으로 취향을 공유합니다.

---

## 핵심 기능

| 기능 | 설명 |
| --- | --- |
| **AI 챗봇 추천** | GMS(GPT-4.1-mini) 기반 대화형 추천 — 이전 대화 기억, 장르·감정 의도 파악, 스코어링 |
| **시맨틱 검색** | `sentence-transformers` 768차원 임베딩으로 의미 유사도 기반 영화 후보 추출 |
| **TMDB 연동** | Top Rated 200편 자동 수집, 상세 정보(출연진·감독·트레일러) TMDB API 실시간 조회 |
| **영화 평점·리뷰** | 별점 + 댓글 동시 제출, 스포일러 태그, 리뷰 좋아요 |
| **소셜 팔로우** | 유저 간 팔로우/언팔로우, 팔로워·팔로잉 목록 조회 |
| **커뮤니티** | 영화 연계 게시글·댓글 CRUD, 작성자 권한 보호 |
| **실시간 채팅** | Django Channels(WebSocket) 기반 영화별 채팅방 |
| **온보딩** | 가입 시 선호 장르·영화 선택으로 초기 취향 프로필 구성 |
| **인증·계정** | JWT Access(60분)/Refresh(1일), 프로필 이미지 설정, 인생작 영화 등록 |

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     Client (Browser)                    │
│              Vue 3 + TypeScript + Vite                  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP REST / WebSocket
┌────────────────────────▼────────────────────────────────┐
│              Django 4.2 + Django REST Framework         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ movies/  │ │ users/   │ │recommend/│ │community/ │  │
│  │ TMDB 연동│ │ 팔로우   │ │AI 챗봇   │ │게시판     │  │
│  │ 평점·리뷰│ │ 즐겨찾기 │ │시맨틱검색│ │WebSocket  │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
│                    Daphne (ASGI)                         │
└──────────┬──────────────────────┬───────────────────────┘
           │                      │
┌──────────▼──────────┐  ┌────────▼────────────────────┐
│     SQLite 3        │  │    GMS API (gpt-4.1-mini)   │
│   (메인 DB)         │  │  + TMDB API + sentence-     │
└─────────────────────┘  │    transformers              │
                         └─────────────────────────────┘
```

---

## AI 추천 흐름

```
사용자 채팅 입력
       │
       ▼
 [intent.py] 의도 파악 (장르·감정·키워드)
       │
       ▼
 [genre_parser.py] 텍스트 → 장르 ID 매핑
       │
       ├─────────────────────────┐
       ▼                         ▼
[candidate.py]            [semantic.py]
 장르 기반 후보 추출        임베딩 유사도 후보 추출
       │                         │
       └──────────┬──────────────┘
                  ▼
           [scoring.py]
         후보 통합 스코어링
                  │
                  ▼
           [ai_client.py]
      GMS(gpt-4.1-mini) 최종 순위·설명 생성
                  │
                  ▼
            추천 결과 반환
```

---

## 기술 스택

| 계층 | 기술 | 버전 | 용도 |
| --- | --- | --- | --- |
| **Frontend** | Vue 3 + TypeScript | Vue 3 / TS 5 | 웹 UI |
| **빌드 도구** | Vite | 6 | 번들링·HMR |
| **UI** | Tailwind CSS + lucide-vue-next | — | 스타일·아이콘 |
| **라우팅** | vue-router | 4 | SPA 라우팅 |
| **Backend API** | Django + DRF | 4.2 + 3.16 | REST API 서버 |
| **실시간** | Django Channels + Daphne | 4.3 + 4.2 | WebSocket 채팅 |
| **인증** | djangorestframework-simplejwt | 5.5 | JWT 인증 |
| **데이터베이스** | SQLite 3 | — | 메인 DB |
| **AI LLM** | GMS 프록시 (gpt-4.1-mini) | — | 챗봇·추천 순위 생성 |
| **임베딩 모델** | sentence-transformers | 5.2 | 768차원 시맨틱 검색 |
| **외부 API** | TMDB API | — | 영화 데이터 소스 |

---

## 디렉토리 구조

```
PJT/
├── Back_End/                        # Django 4.2 + DRF
│   ├── config/                      # Django 설정·URL 라우팅·ASGI
│   ├── movies/                      # 영화 CRUD, 평점·리뷰, 히어로 배너
│   │   └── tmdb.py                  # TMDB API 연동
│   ├── users/                       # 유저 프로파일, 팔로우, 즐겨찾기, 시청이력
│   ├── recommend/                   # AI 추천 챗봇·시맨틱 검색
│   │   └── services/
│   │       ├── ai_client.py         # GMS API 클라이언트
│   │       ├── candidate.py         # 장르 기반 후보 추출
│   │       ├── semantic.py          # 임베딩 유사도 검색
│   │       ├── scoring.py           # 후보 통합 스코어링
│   │       ├── intent.py            # 사용자 의도 파악
│   │       ├── genre_parser.py      # 텍스트 → 장르 매핑
│   │       └── prompt.py            # 프롬프트 템플릿
│   ├── community/                   # 게시글·댓글·실시간 채팅(WebSocket)
│   ├── requirements.txt
│   └── manage.py
└── Front_End/                       # Vue 3 + TypeScript + Vite
    ├── src/
    │   ├── components/              # 페이지·UI 컴포넌트
    │   │   ├── HomeView.vue         # 메인 홈 (히어로 배너·인기 영화)
    │   │   ├── MovieDetail.vue      # 영화 상세·평점·리뷰
    │   │   ├── ExploreView.vue      # 둘러보기 (예정작·인생작·커뮤니티)
    │   │   ├── UserProfile.vue      # 유저 프로파일
    │   │   └── community/           # 커뮤니티 게시판 컴포넌트
    │   │       └── chat/            # 실시간 채팅 컴포넌트
    │   └── router/                  # vue-router 설정
    ├── package.json
    └── vite.config.ts
```

---

## Quick Start

### 사전 요구사항

- Python 3.10+
- Node.js 18+

### 1. 환경변수 설정

```bash
# Back_End/.env 파일 생성
TMDB_API_KEY=your_tmdb_api_key
GMS_API_URL=your_gms_proxy_url
GMS_API_KEY=your_gms_api_key
SECRET_KEY=your_django_secret_key
```

### 2. 백엔드 실행

```bash
cd Back_End
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# → http://localhost:8000
```

### 3. 영화 데이터 수집 (최초 1회)

```bash
# TMDB Top Rated 200편 수집
python manage.py seed_movies

# 추천용 임베딩 생성
python manage.py build_embeddings
```

### 4. 프론트엔드 실행

```bash
cd Front_End
npm install
npm run dev
# → http://localhost:5173
```

---

## 환경변수

`Back_End/.env` 파일에 설정합니다. **`.env` 파일은 절대 커밋하지 않습니다.**

| 변수 | 필수 | 설명 |
| --- | --- | --- |
| `TMDB_API_KEY` | **필수** | TMDB API 키 — 영화 데이터 조회용 |
| `GMS_API_URL` | **필수** | GMS 프록시 엔드포인트 URL |
| `GMS_API_KEY` | **필수** | GMS API 키 (gpt-4.1-mini 호출용) |
| `SECRET_KEY` | 필수 | Django 시크릿 키 (운영 환경에서 반드시 교체) |

---

## API 개요

기본 URL: `http://localhost:8000`

| 도메인 | 주요 엔드포인트 | 인증 |
| --- | --- | --- |
| **인증** | `POST /api/token/`, `POST /api/token/refresh/` | — |
| **영화** | `GET /movies/`, `GET /movies/{id}/`, `GET /movies/search/` | — |
| **평점·리뷰** | `POST /movies/{id}/ratings/`, `GET /movies/{id}/ratings/` | 일부 필요 |
| **추천 챗봇** | `POST /recommend/chat/` | 필요 |
| **사용자** | `GET/PATCH /users/me/`, `/users/follow/`, `/users/favorites/` | 필요 |
| **커뮤니티** | `GET/POST /community/posts/`, `/community/posts/{id}/comments/` | 일부 필요 |
| **실시간 채팅** | `ws://localhost:8000/ws/chat/{movie_id}/` | WebSocket |

---

## 팀원

| 이름 | 역할 | GitHub |
| --- | --- | --- |
| 김동현 | 백엔드 / AI | [@hosup2](https://github.com/hosup2) |
| 김지원 | 프론트엔드 / 디자인 | [@jiwonii6](https://github.com/jiwonii6) |

---

<p align="center">
  <sub>SSAFY 14기 1학기 프로젝트 — MIA Team</sub>
</p>
