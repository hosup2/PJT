<template>
  <div class="explore-view min-h-screen bg-[#0f1419] text-white">
    <div class="pt-20 pb-12 px-8">
      
      <h1 class="text-3xl font-bold mb-8">둘러보기 키키</h1>

      <!-- 섹션 1: 공개 예정 영화 카드 -->
      <div class="mb-8">
        <div 
          class="relative bg-gradient-to-r from-gray-800/80 to-gray-900/80 rounded-3xl p-8 cursor-pointer hover:scale-[1.02] transition-all duration-300 overflow-hidden group"
        >
          <!-- 배경 장식 -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-20">
            <div class="grid grid-cols-3 gap-2 p-4">
              <div v-for="i in 6" :key="i" class="aspect-[2/3] bg-blue-500/20 rounded-lg"></div>
            </div>
          </div>

          <!-- 콘텐츠 -->
          <div class="relative z-10">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <span class="text-sm text-gray-400">영화</span>
              </div>
              <button 
                @click="goToFullExplore"
                class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-full transition-colors flex items-center gap-2"
              >
                더보기
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <h2 class="text-2xl font-bold mb-3">
              {{ movieGroups.length > 0 ? movieGroups[0].date : '' }} <br/>
              공개 예정 영화 {{ totalMovieCount }}편을 확인하세요
            </h2>

            <div class="flex flex-wrap gap-2 mb-4">
              <span class="text-sm px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full">#공개예정</span>
              <span class="text-sm px-3 py-1 bg-purple-600/20 text-purple-400 rounded-full">#신작</span>
              <span class="text-sm px-3 py-1 bg-pink-600/20 text-pink-400 rounded-full">#개봉일정</span>
            </div>

            <!-- 미니 프리뷰 -->
            <div class="flex gap-3 overflow-x-auto pb-2">
              <div v-for="(movie, idx) in previewMovies.slice(0, 6)" :key="idx" 
                   @click="onMovieClick(movie.id)"
                   class="flex-shrink-0 w-32 cursor-pointer group">
                <div class="aspect-[2/3] rounded-lg overflow-hidden mb-2">
                  <img :src="movie.poster_path" :alt="movie.title" 
                       class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" />
                </div>
                <p class="text-xs line-clamp-2 group-hover:text-blue-400 transition-colors">{{ movie.title }}</p>
              </div>
              <div v-if="totalMovieCount > 6" 
                   @click="goToFullExplore"
                   class="flex-shrink-0 w-32 aspect-[2/3] rounded-lg bg-gray-700 flex flex-col items-center justify-center cursor-pointer hover:bg-gray-600 transition-colors">
                <span class="text-3xl font-bold mb-2">+{{ totalMovieCount - 6 }}</span>
                <span class="text-xs text-gray-400">더보기</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 섹션 2: 인증회원의 인생작 영화보기 카드 -->
      <div class="mb-8">
        <div 
          class="relative bg-gradient-to-r from-purple-900/40 to-pink-900/40 rounded-3xl p-8 cursor-pointer hover:scale-[1.02] transition-all duration-300 overflow-hidden group"
        >
          <!-- 배경 장식 -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-20">
            <div class="grid grid-cols-3 gap-2 p-4">
              <div v-for="i in 6" :key="i" class="aspect-[2/3] bg-purple-500/20 rounded-lg"></div>
            </div>
          </div>

          <!-- 콘텐츠 -->
          <div class="relative z-10">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-purple-600 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                </div>
                <span class="text-sm text-gray-400">큐레이션</span>
              </div>
              <button class="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-full transition-colors flex items-center gap-2">
                더보기
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <h2 class="text-2xl font-bold mb-3">
              인증회원들의 인생작 영화<br/>
              엄선된 명작을 만나보세요
            </h2>

            <div class="flex flex-wrap gap-2 mb-4">
              <span class="text-sm px-3 py-1 bg-purple-600/20 text-purple-400 rounded-full">#인생영화</span>
              <span class="text-sm px-3 py-1 bg-pink-600/20 text-pink-400 rounded-full">#명작</span>
              <span class="text-sm px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full">#추천</span>
            </div>

            <div class="text-gray-300">
              💎 인증회원들이 추천하는 베스트 컬렉션
            </div>
          </div>
        </div>
      </div>

      <!-- 섹션 3: 영화 커뮤니티 카드 -->
      <div class="mb-8">
        <div 
          class="relative bg-gradient-to-r from-green-900/40 to-teal-900/40 rounded-3xl p-8 cursor-pointer hover:scale-[1.02] transition-all duration-300 overflow-hidden group"
        >
          <!-- 배경 장식 -->
          <div class="absolute right-0 top-0 w-1/2 h-full opacity-20">
            <div class="grid grid-cols-2 gap-2 p-4">
              <div v-for="i in 4" :key="i" class="aspect-video bg-green-500/20 rounded-lg"></div>
            </div>
          </div>

          <!-- 콘텐츠 -->
          <div class="relative z-10">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                  </svg>
                </div>
                <span class="text-sm text-gray-400">커뮤니티</span>
              </div>
              <button class="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-full transition-colors flex items-center gap-2">
                더보기
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <h2 class="text-2xl font-bold mb-3">
              영화 커뮤니티<br/>
              최신 리뷰와 토론에 참여하세요
            </h2>

            <div class="flex flex-wrap gap-2 mb-4">
              <span class="text-sm px-3 py-1 bg-green-600/20 text-green-400 rounded-full">#리뷰</span>
              <span class="text-sm px-3 py-1 bg-teal-600/20 text-teal-400 rounded-full">#토론</span>
              <span class="text-sm px-3 py-1 bg-blue-600/20 text-blue-400 rounded-full">#한줄평</span>
            </div>

            <div class="space-y-2">
              <div class="text-sm text-gray-300">🔥 오늘의 HOT 토픽: "대흥수 - 과연 명작인가?"</div>
              <div class="text-sm text-gray-400">💬 활발한 토론이 진행 중입니다</div>
            </div>
          </div>
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
  return movies.value.slice(0, 6);
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
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>