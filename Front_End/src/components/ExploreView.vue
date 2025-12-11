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
import { computed } from 'vue';
import { mockMovies, mockLikedMovies } from '../data/mockData';

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

// 타임라인 형식으로 날짜별로 영화 그룹화
const movieGroups = computed(() => {
  return [
    {
      date: '토요일',
      platforms: [
        {
          count: 1,
          movies: mockMovies.slice(0, 1)
        }
      ]
    },
    {
      date: '12.15',
      platforms: [
        {
          count: 4,
          movies: mockMovies.slice(1, 5)
        }
      ]
    },
    {
      date: '12.17',
      platforms: [
        {
          count: 3,
          movies: mockMovies.slice(5, 8)
        }
      ]
    },
    {
      date: '12.20',
      platforms: [
        {
          count: 4,
          movies: mockMovies.slice(8, 12)
        }
      ]
    }
  ];
});

const handleLoginRequired = () => {
  alert('🔒 로그인을 하여서 찜해보세요!');
  emit('open-auth');
};

const handleAddToLikes = (movieId: number) => {
  const movie = mockMovies.find(m => m.id === movieId);
  if (!movie) return;
  
  // 이미 좋아요한 영화인지 확인
  const alreadyLiked = mockLikedMovies.some(m => m.id === movieId);
  
  if (alreadyLiked) {
    alert('이미 좋아요한 영화입니다! 🎬');
    return;
  }
  
  // 좋아요 목록에 추가
  mockLikedMovies.push({
    id: movie.id,
    title: movie.title,
    poster_path: movie.poster_path,
    release_date: movie.release_date || '2024-01-01'
  });
  
  alert('✨ 내가 좋아하는 영화에 추가되었습니다!');
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