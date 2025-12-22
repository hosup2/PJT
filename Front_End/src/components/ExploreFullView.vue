<template>
  <div class="explore-view min-h-screen bg-[#0f1419] text-white">
    <div class="pt-20 pb-12 relative">

      <div class="px-8 mb-6">
        <button 
          @click="goBack"
          class="flex items-center gap-2 px-4 py-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          <span>뒤로가기</span>
        </button>
      </div>
      
      <div class="absolute left-12 top-20 bottom-0 w-0.5 bg-gradient-to-b from-blue-500/50 via-purple-500/50 to-transparent"></div>
      
      <div class="space-y-24 pl-8">
        <div v-for="(group, index) in movieGroups" :key="index" class="relative">
          <div class="absolute left-4 top-0 w-5 h-5 rounded-full bg-blue-500 border-4 border-[#0f1419] z-10"></div>
          
          <div class="ml-16 rounded-2xl p-8">
            <div class="mb-5">
              <span class="text-blue-400 font-semibold text-lg">{{ group.date }}</span>
            </div>
            
            <div class="space-y-8">
              <div v-for="(platform, pIndex) in group.platforms" :key="pIndex">
                <div class="flex items-center gap-3 mb-6">
                  <h2 class="text-xl font-semibold">
                    <span class="text-white">{{ platform.count }}편  </span>
                    <span class="text-gray-400 ml-2">공개예정</span>
                  </h2>
                </div>
                
                <div class="relative group/carousel">
                  
                  <!-- 이전 버튼 -->
                  <button 
                    v-if="platform.movies.length > 5"
                    @click="prevPage(group)"
                    :disabled="group.currentPage === 0"
                    class="w-12 h-12 rounded-full flex items-center justify-center text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:bg-gray-700/80"
                    style="position: absolute; top: 50%; transform: translateY(-50%); left: -2.5rem; z-index: 20; background-color: rgba(0,0,0,0.5); backdrop-filter: blur(8px);"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                  </button>

                  <div class="p-6 rounded-3xl" style="background-color: rgb(17, 24, 39); border-radius: 2rem;">
                    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                      <!-- 각 영화별 개별 카드 (페이지네이션 적용) -->
                      <div 
                        v-for="movie in platform.movies.slice(group.currentPage * 5, (group.currentPage * 5) + 5)"
                        :key="movie.id"
                        @click="onMovieClick(movie.id)"
                        class="cursor-pointer group p-3 rounded-lg bg-gray-700/70 hover:bg-gray-600/90 transition-all shadow-md"
                        style="outline: 2px solid transparent; outline-offset: 11px; transition: outline 0.3s ease;"
                        @mouseenter="$event.currentTarget.style.outline = '2px solid white'"
                        @mouseleave="$event.currentTarget.style.outline = '2px solid transparent'"
                      >
                        <div class="relative rounded-2xl mb-3 bg-gray-900 shadow-lg" style="overflow: hidden;">
                          <img 
                            :src="movie.poster_path" 
                            :alt="movie.title"
                            class="w-full aspect-[2/3] object-cover transition-transform duration-300 group-hover:scale-110"
                            style= "border-radius: 1rem;"
                          />
                          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        </div>
                        
                        <div class="space-y-2 px-1">
                          <div class="flex items-center justify-between gap-2">
                            <h3 class="font-medium text-sm line-clamp-2 leading-tight flex-1 group-hover:text-blue-400 transition-colors">
                              {{ movie.title }}
                            </h3>
                            
                            <button 
                              v-if="isLoggedIn"
                              class="flex-shrink-0 w-11 h-11 rounded-full flex items-center justify-center transition-colors group/btn"
                              :class="movie.is_liked 
                                ? 'bg-red-600/20 text-red-400' 
                                : 'bg-gray-700 text-gray-400 hover:bg-gray-600'"
                              @click.stop="handleAddToLikes(movie)"
                              :title="movie.is_liked ? '좋아요 취소' : '좋아요 추가'"
                            >
                              <svg 
                                xmlns="http://www.w3.org/2000/svg"
                                class="w-6 h-6 transition-transform duration-200 group-hover/btn:scale-110" 
                                viewBox="0 0 24 24"
                                stroke-width="2"
                              >
                                <path 
                                  stroke-linecap="round" 
                                  stroke-linejoin="round" 
                                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                                  :stroke="movie.is_liked ? '#ef4444' : 'currentColor'"
                                  :fill="movie.is_liked ? '#ef4444' : 'none'"
                                />
                              </svg>
                            </button>
                          </div>
                          
                          <div class="text-xs text-gray-500">{{ movie.year }}</div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 다음 버튼 -->
                  <button
                    v-if="platform.movies.length > 5"
                    @click="nextPage(group)"
                    :disabled="group.currentPage >= Math.ceil(platform.movies.length / 5) - 1"
                    class="w-12 h-12 rounded-full flex items-center justify-center text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:bg-gray-700/80"
                    style="position: absolute; top: 50%; transform: translateY(-50%); right: -2.5rem; z-index: 20; background-color: rgba(0,0,0,0.5); backdrop-filter: blur(8px);"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
                  </button>
                  
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button 
        @click="scrollToTop"
        class="fixed bottom-8 right-8 w-14 h-14 rounded-full bg-blue-600 hover:bg-blue-700 shadow-xl flex items-center justify-center transition-all z-50 hover:scale-110 active:scale-95"
      >
        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

// 2. 그룹화 로직 (데이터가 변경될 때마다 실행)
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
    .sort(([yearMonthA], [yearMonthB]) => yearMonthA.localeCompare(yearMonthB)) // 오름차순 정렬
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
  movie.is_liked = !originalStatus; // UI 즉시 변경

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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>