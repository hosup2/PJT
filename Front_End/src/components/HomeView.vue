<template>
  <div class="home-container">
    <HeroSection @navigate-to-explore="navigateToExplore" />
    
    <section class="content-section">
      <div class="section-inner">
        <header class="section-header">
          <div class="header-text">
            <span class="section-label">TRENDING NOW</span>
            <h2 class="section-title">인기 영화</h2>
          </div>
          
          <button @click="navigateToExplore" class="btn-view-all">
            <span>전체보기</span>
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </header>
        
        <MovieGrid 
          :movies="popularMovies"
          @movie-click="handleMovieClick"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import HeroSection from './Herosection.vue';
import MovieGrid from './MovieGrid.vue';

// 인터페이스 유지
interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
  release_date: string; // MovieGrid에서 날짜를 쓰므로 API 응답에 포함되어야 함 (없으면 추가 필요)
  tmdb_rating?: number;
  stats?: {
    avg_rating: number;
    rating_count: number;
  };
}

const router = useRouter();
const popularMovies = ref<Movie[]>([]);

const fetchPopularMovies = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/movies/featured/'); 
    const featuredMovies = response.data;

    // 데이터 매핑 시 release_date 등이 있는지 확인 필요
    popularMovies.value = featuredMovies.map((featured: any) => featured.movie);
  } catch (error) {
    console.error('인기 영화를 가져오는 데 실패했습니다:', error);
  }
};

onMounted(fetchPopularMovies);

const handleMovieClick = (movieId: number) => {
  router.push({ name: 'MovieDetail', params: { id: movieId } });
};

const navigateToExplore = () => {
  router.push({ name: 'Explore' });
};
</script>

<style scoped>
/* 🎨 MIA Cinema Home Style */
.home-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}

/* CONTENT SECTION */
.content-section {
  padding: 2rem 0 6rem;
  background: linear-gradient(to bottom, #0a0b0f 0%, #0f1014 100%);
}

.section-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
}

/* SECTION HEADER */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 0.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.header-text {
  display: flex;
  flex-direction: column;
}

.section-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #8b5cf6; /* MIA Purple */
  margin-bottom: 0.5rem;
  text-transform: uppercase;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  margin: 0;
  color: #ffffff;
}

/* VIEW ALL BUTTON */
.btn-view-all {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9375rem;
  font-weight: 500;
  padding: 0.5rem 0;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view-all:hover {
  color: #8b5cf6;
  transform: translateX(4px);
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .section-inner {
    padding: 0 1.5rem;
  }
  
  .section-title {
    font-size: 1.75rem;
  }
  
  .section-header {
    align-items: center;
  }
}
</style>