<template>
  <div class="explore-view min-h-screen bg-black text-white selection:bg-blue-500/30">
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
      <div class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px]"></div>
    </div>

    <div class="relative z-10 pt-24 pb-12 px-6 max-w-7xl mx-auto">
      
      <div class="mb-12 flex items-end justify-between">
        <div>
          <h1 class="text-5xl md:text-6xl font-black mb-4 tracking-tight">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
              Discover
            </span>
            <br />
            New Worlds.
          </h1>
          <p class="text-gray-400 text-lg">MIA가 엄선한 영화, 컬렉션, 그리고 이야기.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-6">

        <div 
          class="md:col-span-8 group relative bg-gray-900/40 backdrop-blur-xl border border-white/10 rounded-[32px] p-8 overflow-hidden hover:border-white/20 transition-all duration-500"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

          <div class="relative z-10 h-full flex flex-col justify-between">
            <div class="flex justify-between items-start mb-6">
              <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-blue-400 text-xs font-bold mb-3">
                  <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                  </span>
                  UPCOMING
                </div>
                <h2 class="text-3xl font-bold mb-2">공개 예정작</h2>
                <p class="text-gray-400 text-sm">
                  {{ movieGroups.length > 0 ? movieGroups[0].date : '곧 공개될' }} 
                  새로운 영화 <span class="text-white font-bold">{{ totalMovieCount }}편</span>을 가장 먼저 만나보세요.
                </p>
              </div>
              
              <button 
                @click="goToFullExplore"
                class="w-10 h-10 rounded-full bg-white/5 hover:bg-white/20 flex items-center justify-center transition-colors group/btn"
              >
                <svg class="w-5 h-5 group-hover/btn:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <div class="flex gap-4 overflow-x-auto pb-4 scrollbar-hide snap-x">
              <div 
                v-for="(movie, idx) in previewMovies.slice(0, 5)" 
                :key="idx" 
                @click="onMovieClick(movie.id)"
                class="flex-shrink-0 w-36 snap-start cursor-pointer group/poster"
              >
                <div class="aspect-[2/3] rounded-2xl overflow-hidden mb-3 relative shadow-lg">
                  <div class="absolute inset-0 bg-black/20 group-hover/poster:bg-transparent transition-colors z-10"></div>
                  <img 
                    :src="movie.poster_path" 
                    :alt="movie.title" 
                    class="w-full h-full object-cover transform group-hover/poster:scale-110 transition-transform duration-500" 
                  />
                </div>
                <p class="text-sm font-medium text-gray-300 group-hover/poster:text-white truncate transition-colors">{{ movie.title }}</p>
                <p class="text-xs text-gray-500">{{ movie.year }}</p>
              </div>
              
              <div 
                v-if="totalMovieCount > 5"
                @click="goToFullExplore"
                class="flex-shrink-0 w-36 aspect-[2/3] rounded-2xl border-2 border-dashed border-white/10 flex flex-col items-center justify-center cursor-pointer hover:border-white/30 hover:bg-white/5 transition-all"
              >
                <span class="text-2xl font-bold text-gray-500">+{{ totalMovieCount - 5 }}</span>
                <span class="text-xs text-gray-600 mt-1">더보기</span>
              </div>
            </div>
          </div>
        </div>

        <div 
          class="md:col-span-4 group relative bg-gray-900/40 backdrop-blur-xl border border-white/10 rounded-[32px] p-8 overflow-hidden hover:border-white/20 transition-all duration-500"
        >
           <div class="absolute top-0 right-0 w-64 h-64 bg-purple-500/20 blur-[80px] -mr-16 -mt-16 rounded-full group-hover:bg-purple-500/30 transition-all"></div>

           <div class="relative z-10 h-full flex flex-col">
            <div class="mb-auto">
              <div class="inline-block px-3 py-1 rounded-full bg-purple-500/20 border border-purple-500/30 text-purple-400 text-xs font-bold mb-4">
                CURATION
              </div>
              <h2 class="text-3xl font-bold mb-3 leading-tight">
                인증회원들의<br/>
                <span class="text-purple-400">인생 영화</span>
              </h2>
              <p class="text-gray-400 text-sm mb-6">
                검증된 시네필들이 선택한<br/>
                절대 실패 없는 명작 컬렉션.
              </p>
            </div>

            <div class="relative h-40 mt-4 flex items-center justify-center">
              <div class="absolute w-24 h-32 bg-gray-800 rounded-lg transform -rotate-12 translate-x-[-40px] border border-white/10 shadow-xl z-10 group-hover:-rotate-[15deg] group-hover:translate-x-[-50px] transition-all duration-500"></div>
              <div class="absolute w-24 h-32 bg-gray-700 rounded-lg transform rotate-0 scale-110 border border-white/10 shadow-2xl z-20"></div>
              <div class="absolute w-24 h-32 bg-gray-800 rounded-lg transform rotate-12 translate-x-[40px] border border-white/10 shadow-xl z-10 group-hover:rotate-[15deg] group-hover:translate-x-[50px] transition-all duration-500"></div>
            </div>

            <button class="mt-8 w-full py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-sm font-medium transition-colors flex items-center justify-center gap-2">
              컬렉션 구경하기
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
            </button>
           </div>
        </div>

        <div 
          class="md:col-span-12 group relative bg-gradient-to-r from-gray-900/60 to-gray-800/60 backdrop-blur-xl border border-white/10 rounded-[32px] p-8 overflow-hidden hover:border-white/20 transition-all duration-500"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-green-500/5 to-teal-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

          <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
            <div class="flex-1">
              <div class="inline-block px-3 py-1 rounded-full bg-green-500/20 border border-green-500/30 text-green-400 text-xs font-bold mb-4">
                COMMUNITY
              </div>
              <h2 class="text-3xl font-bold mb-2">영화 수다</h2>
              <p class="text-gray-400 text-sm max-w-md">
                영화를 보고 난 뒤의 여운, 이곳에서 함께 나누세요. <br class="hidden md:block"/>
                최신작 리뷰부터 심도 깊은 토론까지.
              </p>
            </div>

            <div class="flex-1 w-full md:w-auto">
              <div class="bg-black/40 rounded-2xl p-4 border border-white/5 backdrop-blur-md">
                <div class="flex items-center gap-3 mb-3">
                  <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500 text-white">HOT</span>
                  <span class="text-sm font-medium text-gray-200">"대홍수 - 과연 명작인가?"</span>
                </div>
                <div class="space-y-2">
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-gray-700"></div>
                    <div class="h-2 w-3/4 bg-gray-700 rounded full"></div>
                  </div>
                   <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-gray-700"></div>
                    <div class="h-2 w-1/2 bg-gray-700 rounded full"></div>
                  </div>
                </div>
                <div class="mt-3 text-right">
                  <span class="text-xs text-green-400 font-medium cursor-pointer hover:underline">참여하기 &rarr;</span>
                </div>
              </div>
            </div>

            <button class="shrink-0 px-8 py-3 bg-green-600 hover:bg-green-500 rounded-full text-white font-bold shadow-lg shadow-green-900/50 transition-all transform group-hover:scale-105">
              커뮤니티 입장
            </button>
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
  return movies.value.slice(0, 10); // 슬라이더를 위해 조금 더 많이 가져옴
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
/* 가로 스크롤바 숨기기 (크롬, 사파리, 오페라) */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
/* 가로 스크롤바 숨기기 (IE, 엣지, 파이어폭스) */
.scrollbar-hide {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
}
</style>