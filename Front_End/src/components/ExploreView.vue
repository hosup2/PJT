<template>
  <div class="explore-view min-h-screen bg-[#0f1419]">
    <div class="pt-20 pb-12 relative">
      <!-- 타임라인 세로 라인 -->
      <div class="absolute left-12 top-20 bottom-0 w-0.5 bg-gradient-to-b from-blue-500/50 via-purple-500/50 to-transparent"></div>
      
      <!-- 타임라인 컨텐츠 -->
      <div class="space-y-16 pl-8">
        <!-- 날짜별 섹션 반복 -->
        <div v-for="(group, index) in movieGroups" :key="index" class="relative">
          <!-- 타임라인 점 -->
          <div class="absolute left-4 top-0 w-5 h-5 rounded-full bg-blue-500 border-4 border-[#0f1419] z-10"></div>
          
          <!-- 날짜 헤더 -->
          <div class="ml-16 mb-6">
            <span class="text-blue-400 font-semibold text-lg">{{ group.date }}</span>
          </div>
          
          <!-- 플랫폼별 영화 리스트 -->
          <div class="ml-16 space-y-8">
            <div v-for="(platform, pIndex) in group.platforms" :key="pIndex">
              <!-- 플랫폼 헤더 -->
              <div class="flex items-center gap-3 mb-6">
                <h2 class="text-xl font-semibold">
                  <span class="text-white">{{ platform.count }}편</span>
                  <span class="text-gray-400 ml-2">공개예정</span>
                </h2>
              </div>
              
              <!-- 영화 카드 그리드 -->
              <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                <div 
                  v-for="movie in platform.movies" 
                  :key="movie.id"
                  @click="onMovieClick(movie.id)"
                  class="cursor-pointer group"
                >
                  <div class="relative overflow-hidden rounded-xl mb-3 bg-gray-900">
                    <img 
                      :src="movie.poster_path" 
                      :alt="movie.title"
                      class="w-full aspect-[2/3] object-cover transition-transform duration-300 group-hover:scale-105"
                    />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  
                  <div class="space-y-2 px-1">
                    <h3 class="font-medium text-sm line-clamp-2 leading-tight">{{ movie.title }}</h3>
                    <div class="flex items-center justify-between">
                      <div class="text-xs text-gray-500">{{ movie.year }}</div>
                      <button 
                        v-if="isLoggedIn"
                        class="w-8 h-8 rounded-full bg-gray-800/90 border border-gray-700 flex items-center justify-center hover:bg-purple-600 hover:border-purple-500 transition-all group/btn"
                        @click.stop="handleAddToLikes(movie.id)"
                        title="좋아요에 추가"
                      >
                        <svg class="w-4 h-4 group-hover/btn:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                      </button>
                      <button 
                        v-else
                        class="w-8 h-8 rounded-full bg-gray-800/90 border border-gray-700 flex items-center justify-center hover:bg-gray-700 hover:border-gray-600 transition-all"
                        @click.stop="handleLoginRequired"
                        title="로그인이 필요합니다"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 맨 위로 버튼 -->
      <button 
        @click="scrollToTop"
        class="fixed bottom-8 right-8 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 shadow-lg flex items-center justify-center transition-all z-50"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// Movie 인터페이스 정의 (API 응답에 맞춰 조정)
interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
  release_date: string;
  // API 응답에 따라 필요한 다른 속성들 추가
  year?: number; // year는 release_date에서 파생될 수 있으므로 선택적으로 처리
}

// 컴포넌트 Props와 Emits 정의
interface Props {
  isLoggedIn?: boolean;
  currentUserId?: number;
}

const props = withDefaults(defineProps<Props>(), {
  isLoggedIn: false,
  currentUserId: undefined
});

const emit = defineEmits<{
  (e: 'movie-click', movieId: number): void;
  (e: 'open-auth'): void;
}>();

// API에서 받아온 영화 목록을 저장할 반응형 변수
const movies = ref<Movie[]>([]);
const error = ref<string | null>(null);

// 컴포넌트가 마운트될 때 API 호출
onMounted(async () => {
  try {
    // Django API 엔드포인트에서 영화 목록을 가져옵니다.
    const response = await axios.get('http://127.0.0.1:8000/movies/');
    // DRF 페이지네이션을 사용하는 경우, 결과는 response.data.results에 있습니다.
    const results = response.data.results || response.data;
    
    // year 속성 추가 및 poster_path가 없는 경우 기본 이미지 설정
    movies.value = results.map((movie: any) => ({
      ...movie,
      year: new Date(movie.release_date).getFullYear(),
      poster_path: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/500x750?text=No+Image'
    }));

  } catch (err) {
    console.error('Failed to fetch movies:', err);
    error.value = '영화 목록을 불러오는 데 실패했습니다.';
  }
});

// 타임라인 형식으로 날짜별로 영화 그룹화하는 computed 속성
const movieGroups = computed(() => {
  if (!movies.value.length) {
    return [];
  }

  // 날짜를 기준으로 영화들을 그룹화
  const groups: { [key: string]: Movie[] } = movies.value.reduce((acc, movie) => {
    const date = movie.release_date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(movie);
    return acc;
  }, {} as { [key: string]: Movie[] });

  // 템플릿이 기대하는 구조로 변환
  return Object.entries(groups)
    .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime()) // 최신 날짜 순으로 정렬
    .map(([date, movieList]) => ({
      date: new Date(date).toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'long' }),
      platforms: [
        {
          count: movieList.length,
          movies: movieList,
        },
      ],
    }));
});

const handleLoginRequired = () => {
  alert('🔒 로그인을 하여서 찜해보세요!');
  emit('open-auth');
};

const handleAddToLikes = (movieId: number) => {
  // TODO: 실제 '좋아요' API 연동 필요
  alert(`'${movies.value.find(m => m.id === movieId)?.title}' 영화를 좋아합니다! (API 연동 필요)`);
};

const onMovieClick = (movieId: number) => {
  emit('movie-click', movieId);
};

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>

<style scoped>
/* 타임라인 스타일 */
</style>