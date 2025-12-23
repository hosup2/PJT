```vue
<template>
  <div class="hero-container">
    <div class="ambient-glow white"></div>
    <div class="ambient-glow purple"></div>

    <div class="hero-inner">
      
      <header class="hero-header">
        <h1 class="main-title">
          <span class="gradient-text">Discover</span><br />
          New Worlds.
        </h1>
        <p class="sub-title">MIA가 엄선한 영화, 컬렉션, 그리고 이야기.</p>
      </header>

      <div class="bento-grid">

        <div 
          @click="goToFullExplore"
          class="bento-card large upcoming-card group"
        >
          <div class="card-glow"></div>
          
          <div class="card-content">
            <div class="card-header-row">
              <div class="header-left">
                <div class="badge-pill blue">
                  <span class="pulse-dot">
                    <span class="ping"></span>
                    <span class="dot"></span>
                  </span>
                  UPCOMING
                </div>
                <h2 class="card-title">공개 예정작</h2>
                <p class="card-desc">
                  {{ movieGroups.length > 0 ? movieGroups[0].date : '곧 공개될' }} 
                  새로운 영화 <span class="highlight">{{ totalMovieCount }}편</span>을 만나보세요.
                </p>
              </div>
              
              <div class="icon-circle">
                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>

            <div class="double-carousel">
              
              <div class="carousel-track animate-marquee-left">
                <div class="carousel-set">
                  <div 
                    v-for="(movie, idx) in previewMovies" 
                    :key="`org-l-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="carousel-item group/poster"
                  >
                    <div class="poster-box">
                      <div class="poster-overlay"></div>
                      <img :src="movie.poster_path" :alt="movie.title" />
                    </div>
                    <p class="poster-title">{{ movie.title }}</p>
                    <p class="poster-year">{{ movie.year }}</p>
                  </div>
                </div>
                <div class="carousel-set" aria-hidden="true">
                  <div 
                    v-for="(movie, idx) in previewMovies" 
                    :key="`clone-l-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="carousel-item group/poster"
                  >
                    <div class="poster-box">
                      <div class="poster-overlay"></div>
                      <img :src="movie.poster_path" :alt="movie.title" />
                    </div>
                    <p class="poster-title">{{ movie.title }}</p>
                    <p class="poster-year">{{ movie.year }}</p>
                  </div>
                </div>
              </div>

              <div class="carousel-track animate-marquee-left mt-6">
                <div class="carousel-set">
                  <div 
                    v-for="(movie, idx) in reversePreviewMovies" 
                    :key="`org-r-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="carousel-item group/poster"
                  >
                    <div class="poster-box">
                      <div class="poster-overlay"></div>
                      <img :src="movie.poster_path" :alt="movie.title" />
                    </div>
                    <p class="poster-title">{{ movie.title }}</p>
                    <p class="poster-year">{{ movie.year }}</p>
                  </div>
                </div>
                <div class="carousel-set" aria-hidden="true">
                  <div 
                    v-for="(movie, idx) in reversePreviewMovies" 
                    :key="`clone-r-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="carousel-item group/poster"
                  >
                    <div class="poster-box">
                      <div class="poster-overlay"></div>
                      <img :src="movie.poster_path" :alt="movie.title" />
                    </div>
                    <p class="poster-title">{{ movie.title }}</p>
                    <p class="poster-year">{{ movie.year }}</p>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div class="right-column">
          
          <div class="bento-card curation-card">
            <div class="curation-grid">
              <div
                v-for="item in lifeMovies.slice(0,3)"
                :key="item.user.id"
                class="mini-movie-card cursor-pointer"
                @click="onMovieClick(item.movie.id)"
              >
                <div class="mini-poster">
                  <img :src="`https://image.tmdb.org/t/p/w342${item.movie.poster_path}`" />
                </div>
                <div class="mini-info">
                  <p
                    class="mini-user hover:underline cursor-pointer"
                    @click.stop="goToUserProfile(item.user.id)"
                  >
                    {{ item.user.username }}
                  </p>

                  <p class="mini-title">{{ item.movie.title }}</p>
                  <p v-if="item.review" class="mini-rating">★ {{ item.review.rating }}/5</p>
                </div>
              </div>

              <div class="curation-text-box">
                <div class="badge-pill purple">CURATION</div>
                <h2 class="card-title-sm">
                  내 친구들의<br />
                  <span class="text-purple">인생 영화</span>
                </h2>
              </div>
            </div>
          </div>

          <router-link to="/community" class="bento-card community-card group">
            <div class="card-glow green"></div>
            
            <div class="card-content-row">
              <div class="text-content">
                <div class="badge-pill green">COMMUNITY</div>
                <h2 class="card-title">영화 수다</h2>
                <p class="card-desc-sm">
                  영화를 보고 난 뒤의 여운,<br/>
                  이곳에서 함께 나누세요.
                </p>
              </div>

              <div class="mock-chat-ui">
                <div class="chat-bubble">
                  <div class="chat-header">
                    <span class="tag-hot">HOT</span>
                    <span class="chat-title">"라라랜드 - 과연 명작인가?"</span>
                  </div>
                  <div class="chat-lines">
                    <div class="line long"></div>
                    <div class="line short"></div>
                  </div>
                  <div class="chat-footer">
                    <span>참여하기 &rarr;</span>
                  </div>
                </div>
              </div>
              
              <div class="icon-arrow-green">
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </router-link>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject, Ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
  release_date: string;
  year?: number;
  is_liked?: boolean;
}

interface Props {
  currentUserId?: number;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  (e: 'movie-click', movieId: number): void;
  (e: 'open-auth'): void;
}>();

const router = useRouter();
const movies = ref<Movie[]>([]);
const error = ref<string | null>(null);

const isLoggedIn = inject<Ref<boolean>>('isLoggedIn', ref(false));
const currentUser = inject<Ref<any>>('currentUser', ref(null));

// Life Movies Interface & Ref
interface LifeMovie {
  user: {
    id: number;
    username: string;
  };
  movie: {
    id: number;
    title: string;
    poster_path: string;
  };
  review?: {
    rating: number;
    comment: string;
  };
}
const lifeMovies = ref<LifeMovie[]>([]);

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/movies/');
    const results = response.data.results || response.data;
    
    movies.value = results.map((movie: any) => ({
      ...movie,
      year: new Date(movie.release_date).getFullYear(),
      poster_path: movie.poster_path 
        ? (movie.poster_path.startsWith('http') ? movie.poster_path : `https://image.tmdb.org/t/p/w500${movie.poster_path}`)
        : 'https://via.placeholder.com/500x750?text=No+Image',
      is_liked: movie.is_liked || false 
    }));
    
    // 2️⃣ 🔥 인증회원 인생영화
    const lifeRes = await axios.get(
      'http://127.0.0.1:8000/movies/curation/life-movies/'
    );
    lifeMovies.value = lifeRes.data;
  } catch (err) {
    console.error('Failed to fetch movies:', err);
    error.value = '영화 목록을 불러오는 데 실패했습니다.';
  }
});

const movieGroups = computed(() => {
  if (!movies.value.length) return [];

  const groups: { [key: string]: Movie[] } = movies.value.reduce((acc, movie) => {
    const date = movie.release_date;
    if (!acc[date]) acc[date] = [];
    acc[date].push(movie);
    return acc;
  }, {} as { [key: string]: Movie[] });

  return Object.entries(groups)
    .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime())
    .map(([date, movieList]) => ({
      date: new Date(date).toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'long' }),
      platforms: [{
        count: movieList.length,
        movies: movieList,
      }],
    }));
});

const totalMovieCount = computed(() => {
  return movies.value.length;
});

const previewMovies = computed(() => {
  return movies.value.slice(0, 25); 
});

// 🔥 Reverse order for second carousel
const reversePreviewMovies = computed(() => {
  return [...previewMovies.value].reverse();
});

const onMovieClick = (movieId: number) => {
  router.push({ 
    name: 'MovieDetail', 
    params: { id: movieId.toString() } 
  });
  emit('movie-click', movieId);
};

const goToFullExplore = () => {
  router.push({ name: 'ExploreFull' });
};

const goToUserProfile = (userId: number) => {
  router.push({
    name: 'UserProfile',
    params: { userId: userId.toString() },
  });
};
</script>

<style scoped>
/* 🎨 MIA Cinema Hero Style */
.hero-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  position: relative;
  overflow: hidden;
  /* 👇 네비게이션 바와 겹치지 않도록 상단 여백 추가 */
  padding-top: 5rem; 
  padding-bottom: 4rem;
}

/* Background Ambient Glows */
.ambient-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
  pointer-events: none;
}

.ambient-glow.white {
  top: -10%;
  left: -10%;
  background: rgba(30, 18, 80, 0.557);
}

.ambient-glow.purple {
  bottom: -10%;
  right: -10%;
  background: rgba(147, 51, 234, 0.15);
}

.hero-inner {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 3rem 0;
}

/* Header */
.hero-header {
  margin-bottom: 4rem;
}

.main-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 1rem 0;
  letter-spacing: -0.02em;
}

.gradient-text {
  /* 연한 블루 -> 보라 */
  background: linear-gradient(to right, #93c5fd 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.sub-title {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 300;
}

/* Bento Grid */
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
}

/* General Card Style */
.bento-card {
  position: relative;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.bento-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.card-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom right, rgba(59, 130, 246, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.bento-card:hover .card-glow {
  opacity: 1;
}

.card-glow.green {
  background: linear-gradient(to right, rgba(16, 185, 129, 0.1), transparent);
}

/* === CARD 1: Upcoming (Large) === */
.upcoming-card {
  grid-column: span 6;
  padding: 2.5rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
}

.card-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
}

.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 0.75rem;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.badge-pill.blue {
  background: rgba(59, 130, 246, 0.15);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #60a5fa;
}

.badge-pill.purple {
  background: rgba(147, 51, 234, 0.15);
  border: 1px solid rgba(147, 51, 234, 0.3);
  color: #c084fc;
}

.badge-pill.green {
  background: rgba(16, 185, 129, 0.15);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #34d399;
}

.pulse-dot {
  position: relative;
  display: flex;
  width: 8px;
  height: 8px;
}

.pulse-dot .ping {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #60a5fa;
  opacity: 0.75;
  animation: ping 1.5s cubic-bezier(0, 0, 0.2, 1) infinite;
}

.pulse-dot .dot {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: #3b82f6;
}

@keyframes ping {
  75%, 100% { transform: scale(2); opacity: 0; }
}

.card-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
}

.card-desc {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
}

.card-desc .highlight {
  color: white;
  font-weight: 600;
}

.icon-circle {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s ease;
}

.upcoming-card:hover .icon-circle {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(4px);
}

/* Double Carousel */
.double-carousel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  overflow: hidden;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
  margin-top: 1rem;
}

.carousel-wrapper {
  position: relative;
  width: 100%;
  overflow: hidden;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

.carousel-track {
  display: flex;
  width: max-content;
  gap: 1.5rem;
}

.carousel-set {
  display: flex;
  gap: 1.5rem;
}

.carousel-item {
  width: 140px;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.carousel-item:hover {
  transform: scale(1.05);
}

.poster-box {
  aspect-ratio: 2/3;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
  margin-bottom: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.poster-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.2);
  transition: background 0.3s ease;
}

.carousel-item:hover .poster-overlay {
  background: transparent;
}

.poster-title {
  font-size: 0.75rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
  transition: color 0.2s;
}

.carousel-item:hover .poster-title {
  color: white;
}

.poster-year {
  font-size: 0.6875rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

/* Marquee Animation */
@keyframes marquee-left {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 60s linear infinite;
}

.animate-marquee-left {
  animation: marquee-left 60s linear infinite;
}

.upcoming-card:hover .animate-marquee,
.upcoming-card:hover .animate-marquee-left {
  animation-play-state: paused;
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}


/* === Right Column === */
.right-column {
  grid-column: span 6;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Card 2: Curation */
.curation-card {
  padding: 2rem;
  flex: 1;
}

.curation-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.mini-movie-card {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.mini-poster {
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.mini-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mini-user {
  font-size: 0.6875rem;
  color: #c084fc;
  font-weight: 700;
  margin-bottom: 0.125rem;
}

.mini-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.125rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.mini-rating {
  font-size: 0.6875rem;
  color: #fbbf24;
}

.curation-text-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding-left: 1rem;
}

.card-title-sm {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.2;
  color: white;
}

.text-purple {
  color: #c084fc;
}

/* Card 3: Community */
.community-card {
  padding: 2rem;
  text-decoration: none;
  display: block;
}

.card-content-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.text-content {
  flex: 1;
}

.card-desc-sm {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
}

.mock-chat-ui {
  flex: 1;
  display: none; /* Hidden on very small screens if needed, but handled by flex */
}

@media (min-width: 768px) {
  .mock-chat-ui {
    display: block;
  }
}

.chat-bubble {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1rem;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.tag-hot {
  background: #ef4444;
  color: white;
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
}

.chat-title {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.chat-lines {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-bottom: 0.75rem;
}

.line {
  height: 6px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 100px;
}

.line.long { width: 80%; }
.line.short { width: 50%; }

.chat-footer {
  text-align: right;
  font-size: 0.75rem;
  color: #34d399;
  font-weight: 600;
}

.icon-arrow-green {
  color: #34d399;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  font-weight: 700;
  gap: 0.25rem;
}

.community-card:hover .icon-arrow-green svg {
  transform: translateX(4px);
  transition: transform 0.2s;
}

/* Responsive */
@media (max-width: 1024px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
  
  .upcoming-card, .right-column {
    grid-column: span 1;
  }
  
  .main-title {
    font-size: 3rem;
  }
}

@media (max-width: 768px) {
  .hero-inner {
    padding: 2rem 1.5rem 0;
  }
  
  .card-header-row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .icon-circle {
    display: none;
  }
  
  .card-content-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .mock-chat-ui {
    width: 100%;
  }
}
</style>
```

밑에 줄도 같은 방향(왼쪽으로)으로 가도록 `animate-marquee-right`를 `animate-marquee-left`로 변경했습니다!