<template>
  <div>
    <!-- HeroSection을 화면 맨 위에서 시작 -->
    <HeroSection @navigate-to-explore="navigateToExplore" />
    
    <!-- 인기 영화 -->
    <div class="container mx-auto px-6 py-12 max-w-7xl">
      <div class="flex items-center justify-between mb-8">
        <h2 class="text-3xl font-bold">인기 영화</h2>
        <button @click="navigateToExplore" class="text-purple-400 hover:text-purple-300 text-sm font-medium flex items-center gap-1">
          전체보기
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      
      <MovieGrid 
        :movies="popularMovies"
        @movie-click="handleMovieClick"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import HeroSection from './Herosection.vue';
import MovieGrid from './MovieGrid.vue';

interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
}

const router = useRouter();
const popularMovies = ref<Movie[]>([]);

const fetchPopularMovies = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/movies/featured/'); 
    const featuredMovies = response.data;

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
