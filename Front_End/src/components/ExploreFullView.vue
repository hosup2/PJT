<template>
  <div class="explore-container">
    <header class="explore-header">
      <div class="header-inner">
        <button @click="goBack" class="btn-back-minimal">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
          </svg>
          <span>뒤로가기</span>
        </button>
        <h1 class="page-title">개봉 예정작</h1>
      </div>
    </header>

    <div class="timeline-wrapper">
      <div class="timeline-line"></div>
      
      <div class="groups-container">
        <div v-for="(group, index) in movieGroups" :key="index" class="timeline-group">
          
          <div class="timeline-node">
            <div class="node-dot"></div>
          </div>
          
          <div class="group-content">
            <div class="date-label">
              <span class="month">{{ group.date }}</span>
            </div>
            
            <div class="platforms-list">
              <div v-for="(platform, pIndex) in group.platforms" :key="pIndex" class="platform-section">
                
                <div class="platform-header">
                  <span class="count-badge">{{ platform.count }}편</span>
                  <span class="status-text">공개 예정</span>
                </div>
                
                <div class="carousel-container">
                  
                  <button 
                    v-if="platform.movies.length > 5"
                    @click="prevPage(group)"
                    :disabled="group.currentPage === 0"
                    class="nav-btn prev"
                  >
                    <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                  </button>

                  <div class="movies-row-wrapper">
                    <div class="movies-row">
                      <div 
                        v-for="movie in platform.movies.slice(group.currentPage * 5, (group.currentPage * 5) + 5)"
                        :key="movie.id"
                        @click="onMovieClick(movie.id)"
                        class="movie-item"
                      >
                        <div class="poster-frame">
                          <img 
                            :src="movie.poster_path" 
                            :alt="movie.title"
                          />
                          <div class="poster-overlay"></div>
                        </div>
                        
                        <div class="movie-info">
                          <h3 class="movie-title">{{ movie.title }}</h3>
                          
                          <div class="meta-row">
                            <span class="year-text">{{ movie.year }}</span>
                            
                            <button 
                              v-if="isLoggedIn"
                              @click.stop="handleAddToLikes(movie)"
                              :class="['btn-like-mini', { active: movie.is_liked }]"
                              :title="movie.is_liked ? '좋아요 취소' : '좋아요 추가'"
                            >
                              <svg 
                                xmlns="http://www.w3.org/2000/svg" 
                                viewBox="0 0 24 24"
                                stroke-width="2"
                                class="icon-heart"
                              >
                                <path 
                                  stroke-linecap="round" 
                                  stroke-linejoin="round" 
                                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                                />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <button
                    v-if="platform.movies.length > 5"
                    @click="nextPage(group)"
                    :disabled="group.currentPage >= Math.ceil(platform.movies.length / 5) - 1"
                    class="nav-btn next"
                  >
                    <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
                  </button>
                  
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button @click="scrollToTop" class="fab-top">
        <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, inject, Ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// --- 인터페이스 ---
interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
  release_date: string;
  year?: number;
  is_liked?: boolean;
}

interface MovieGroup {
  yearMonth: string;
  date: string;
  currentPage: number;
  platforms: {
    count: number;
    movies: Movie[];
  }[];
}

const emit = defineEmits<{
  (e: 'movie-click', movieId: number): void;
  (e: 'open-auth'): void;
}>();

// --- 변수 및 주입 ---
const router = useRouter();
const allMovies = ref<Movie[]>([]);
const movieGroups = ref<MovieGroup[]>([]);
const error = ref<string | null>(null);

const isLoggedIn = inject<Ref<boolean>>('isLoggedIn', ref(false));
const currentUser = inject<Ref<any>>('currentUser', ref(null));


// --- 함수 ---

// 1. 데이터 가져오기
onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/movies/');
    const results = response.data.results || response.data;
    
    allMovies.value = results.map((movie: any) => ({
      ...movie,
      year: new Date(movie.release_date).getFullYear(),
      poster_path: movie.poster_path 
        ? (movie.poster_path.startsWith('http') ? movie.poster_path : `https://image.tmdb.org/t/p/w500${movie.poster_path}`)
        : 'https://via.placeholder.com/500x750?text=No+Image',
      is_liked: movie.is_liked || false 
    }));
  } catch (err) {
    console.error('Failed to fetch movies:', err);
    error.value = '영화 목록을 불러오는 데 실패했습니다.';
  }
});

// 2. 그룹화 로직
watch(allMovies, (newMovies) => {
  if (!newMovies.length) {
    movieGroups.value = [];
    return;
  }

  const groups: { [key: string]: Movie[] } = newMovies.reduce((acc, movie) => {
    const yearMonth = movie.release_date.substring(0, 7); // "YYYY-MM"
    if (!acc[yearMonth]) acc[yearMonth] = [];
    acc[yearMonth].push(movie);
    return acc;
  }, {} as { [key: string]: Movie[] });

  movieGroups.value = Object.entries(groups)
    .sort(([yearMonthA], [yearMonthB]) => yearMonthA.localeCompare(yearMonthB))
    .map(([yearMonth, movieList]) => ({
      yearMonth: yearMonth,
      date: new Date(yearMonth).toLocaleDateString('ko-KR', { year: 'numeric', month: 'long' }),
      currentPage: 0,
      platforms: [{
        count: movieList.length,
        movies: movieList,
      }],
    }));
});


// 3. 캐러셀 페이지네이션
const prevPage = (group: MovieGroup) => {
  if (group.currentPage > 0) {
    group.currentPage--;
  }
};

const nextPage = (group: MovieGroup) => {
  const totalPages = Math.ceil(group.platforms[0].movies.length / 5);
  if (group.currentPage < totalPages - 1) {
    group.currentPage++;
  }
};

// 4. 이동
const onMovieClick = (movieId: number) => {
  router.push({ 
    name: 'MovieDetail', 
    params: { id: movieId.toString() } 
  });
  emit('movie-click', movieId);
};

// 5. 좋아요 처리
const handleAddToLikes = async (movie: Movie) => {
  if (!isLoggedIn.value) {
    handleLoginRequired();
    return;
  }

  const originalStatus = movie.is_liked;
  movie.is_liked = !originalStatus;

  try {
    if (originalStatus) {
      await axios.delete(`http://127.0.0.1:8000/users/favorites/${movie.id}/`);
    } else {
      await axios.post(`http://127.0.0.1:8000/users/favorites/${movie.id}/`);
    }
  } catch (err) {
    movie.is_liked = originalStatus;
    console.error('좋아요 실패:', err);
    alert('오류가 발생했습니다.');
  }
};

const handleLoginRequired = () => {
  alert('🔒 로그인을 하면 영화를 찜할 수 있습니다!');
  emit('open-auth');
};


// 6. 기타 함수
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
/* 🎨 MIA Cinema Explore Style */
.explore-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding-bottom: 5rem;
  overflow-x: hidden;
}

/* Header */
.explore-header {
  padding: 2rem 0;
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(10, 11, 15, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.btn-back-minimal {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.5rem 1rem;
  border-radius: 100px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.btn-back-minimal:hover {
  background: rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2); /* 은은한 보라색 빛 */
}

.page-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: white;
}

/* Timeline Layout */
.timeline-wrapper {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 3rem;
}

/* Vertical Line */
.timeline-line {
  position: absolute;
  left: 3rem; /* Aligned with padding */
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(
    to bottom,
    rgba(139, 92, 246, 0) 0%,
    rgba(139, 92, 246, 0.5) 10%,
    rgba(139, 92, 246, 0.5) 90%,
    rgba(139, 92, 246, 0) 100%
  );
  z-index: 0;
}

.timeline-group {
  position: relative;
  margin-bottom: 5rem;
  padding-left: 3rem; /* Space for line */
}

.timeline-node {
  position: absolute;
  left: -5px; /* Half of width (11px) offset from padding-left 0 relative to group? No, relative to line */
  left: -0.35rem; /* Adjust based on line position */
  top: 0;
  z-index: 10;
}

.node-dot {
  width: 11px;
  height: 11px;
  background: #0a0b0f;
  border: 2px solid #8b5cf6;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}

.group-content {
  padding-left: 2rem;
}

/* Date Label */
.date-label {
  margin-bottom: 2rem;
}

.month {
  font-size: 1.5rem;
  font-weight: 300;
  color: #8b5cf6;
  letter-spacing: -0.02em;
}

/* Platforms & Carousel */
.platform-section {
  margin-bottom: 2rem;
}

.platform-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.count-badge {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
}

.status-text {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.05);
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
}

.carousel-container {
  position: relative;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.5rem;
}

.movies-row-wrapper {
  overflow: hidden;
}

.movies-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
}

/* Movie Item - The Outline Effect */
.movie-item {
  cursor: pointer;
  position: relative;
  padding: 0.75rem;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  
  /* ⭐ Requested Outline Style ⭐ */
  outline: 2px solid transparent;
  outline-offset: 4px;
}

.movie-item:hover {
  background: rgba(255, 255, 255, 0.03);
  /* Hover 시 하얀색 아웃라인 적용 (요청사항 반영) */
  outline-color: rgba(255, 255, 255, 0.8);
}

.poster-frame {
  position: relative;
  aspect-ratio: 2/3;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.poster-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-item:hover .poster-frame img {
  transform: scale(1.05);
}

.poster-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.6), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.movie-item:hover .poster-overlay {
  opacity: 1;
}

.movie-title {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
  height: 2.8em; /* 2 lines */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.movie-item:hover .movie-title {
  color: #8b5cf6;
}

.meta-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.year-text {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

/* Mini Like Button */
.btn-like-mini {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: rgba(255, 255, 255, 0.5);
}

.btn-like-mini:hover {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-like-mini.active {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.icon-heart {
  width: 1rem;
  height: 1rem;
  fill: none;
  stroke: currentColor;
}

.btn-like-mini.active .icon-heart {
  fill: currentColor;
  stroke: currentColor;
}

/* Nav Buttons */
.nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(10, 11, 15, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 20;
  transition: all 0.2s ease;
  backdrop-filter: blur(4px);
}

.nav-btn:hover:not(:disabled) {
  background: #8b5cf6;
  border-color: #8b5cf6;
}

.nav-btn:disabled {
  opacity: 0;
  pointer-events: none;
}

.nav-btn.prev { left: -1.25rem; }
.nav-btn.next { right: -1.25rem; }

/* FAB */
.fab-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  background: #8b5cf6;
  border: none;
  color: white;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 100;
}

.fab-top:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
}

/* Responsive */
@media (max-width: 1024px) {
  .movies-row {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .movies-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .timeline-wrapper {
    padding: 2rem 1rem;
  }
  
  .timeline-line {
    left: 1rem;
  }
  
  .timeline-group {
    padding-left: 1.5rem;
  }
  
  .nav-btn.prev { left: -0.75rem; }
  .nav-btn.next { right: -0.75rem; }
}
</style>