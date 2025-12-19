## FrontEnd

## 12.18 
- .env 파일생성 후 tmdb_api_key 저장해서 서버 구동
- 평점과 댓글 기능 수정
- 사용자 프로필 디자인 수정
- 사용자 기본 프로필 수정.


## 12.09
- 새로운 사용자 온보딩 페이지 구현
  - 영화 취향 분석을 위한 온보딩 플로우 추가
  - `onboarding` 디렉토리 내에 `GenreSelection.vue`, `MovieSelection.vue`, `OnboardingProgress.vue`, `PreferenceComplete.vue`, `PreferenceOnboarding.vue` 컴포넌트 신규 생성
  - `App.vue` 수정하여 온보딩 기능 통합

## 12.07

- 네비게이션 바 로고 레이아웃 조정 
- Herosection.vue 풀스크린 캐러셀 구현 
  - 무한 루프 슬라이드 기능 (5초 자동 재생)
  - 좌우 네비게이션 버튼 (호버 시 표시)
  - 하단 인디케이터 (현재 슬라이드 표시)
  - 영화 정보 표시 (제목, 설명, 평점, 장르, 재생 시간)
  - 재생하기/상세정보 버튼 포함


## 12.05
- 사용자 프로필 조회 및 편집을 위한 
UserProfile.vue, ProfileEditModal.vue 컴포넌트 구조 생성
- 영화 상세 정보 표시를 위한
MovieDetail.vue 컴포넌트 구조 생성
- 별점 표시 및 평가를 위한 
StarRating.vue 컴포넌트 추가     
- 댓글 및 평점 목록 관련    
CommentSection.vue,
RatingsList.vue,
RatingDistributionChart.vue      
컴포넌트 추가
- 메인 네비게이션 바 (Navigation.vue) 구현        
- 메인 페이지 Hero 섹션 (Herosection.vue) 구현       
- 영화 목록을 그리드 형태로 표시하는 MovieGrid.vue 구현
- 사용자 인증 모달 AuthModal.vue 추가 (이후 LoginModal.vue로 교체되어 스타일 및 기능 개선)
- 전역 스타일 및 CSS 초기화 (styles/globals.css, index.css)  
- 개발용 Mock Data
## 12.03
- 사용하지않는 tsx 파일 삭제
- Title 수정

## 12.02 
- 기존 React 프로젝트를 Vue 3 기반으로 전환
- 프로젝트 구조 재정리: App.vue, components/ 등 Vue 표준 구조 적용
- 기본 Mockup 페이지 구성 완료
- 프로젝트 서비스명 확정: MIA (Movie Intelligence Assistant)


