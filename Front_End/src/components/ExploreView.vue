<template>
  <div class="explore-view min-h-screen bg-black text-white selection:bg-blue-500/30">
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
      <div class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px]"></div>
    </div>

    <div class="relative z-10 pt-24 pb-12 px-6 w-full">
      
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

      <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">

        <div 
          @click="goToFullExplore"
          class="md:col-span-6 group relative bg-gray-900/40 backdrop-blur-xl border border-white/10 rounded-[32px] px-8 py-5 overflow-hidden hover:border-white/20 transition-all duration-500 cursor-pointer"
        >
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/10 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="absolute top-0 left-0 h-full w-16 bg-gradient-to-r from-gray-900/80 to-transparent z-20 pointer-events-none rounded-l-[32px]"></div>
          <div class="absolute top-0 right-0 h-full w-16 bg-gradient-to-l from-gray-900/80 to-transparent z-20 pointer-events-none rounded-r-[32px]"></div>

          <div class="relative z-10 h-full flex flex-col justify-between">
            
            <div class="flex justify-between items-start mb-1">
              <div class="pl-6">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-blue-400 text-xs font-bold mb-2">
                  <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                  </span>
                  UPCOMING
                </div>
                <h2 class="text-3xl font-bold mb-1">공개 예정작</h2>
                <p class="text-gray-400 text-sm">
                  {{ movieGroups.length > 0 ? movieGroups[0].date : '곧 공개될' }} 
                  새로운 영화 <span class="text-white font-bold">{{ totalMovieCount }}편</span>을 가장 먼저 만나보세요.
                </p>
              </div>
              
              <div
                class="w-10 h-10 rounded-full bg-white/5 group-hover:bg-white/20 flex items-center justify-center transition-colors"
              >
                <svg class="w-5 h-5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>

            <div class="relative w-full overflow-hidden py-2">
              <div class="flex w-max gap-6 animate-marquee">
                
                <div class="flex gap-6">
                  <div 
                    v-for="(movie, idx) in previewMovies" 
                    :key="`org-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="cursor-pointer group/poster flex-shrink-0 transition-transform duration-300 hover:scale-110 hover:z-50 origin-center"
                    style="width: 190px;"
                  >
                    <div class="aspect-[2/3] rounded-2xl overflow-hidden mb-3 relative shadow-lg transform transition-transform duration-500">
                      <div class="absolute inset-0 bg-black/20 group-hover/poster:bg-transparent transition-colors z-10"></div>
                      <img 
                        :src="movie.poster_path" 
                        :alt="movie.title" 
                        class="w-full h-full object-cover" 
                      />
                    </div>
                    <p class="text-sm font-medium text-gray-300 group-hover/poster:text-white truncate transition-colors">{{ movie.title }}</p>
                    <p class="text-xs text-gray-500">{{ movie.year }}</p>
                  </div>
                </div>

                <div class="flex gap-6" aria-hidden="true">
                  <div 
                    v-for="(movie, idx) in previewMovies" 
                    :key="`clone-${movie.id}`" 
                    @click.stop="onMovieClick(movie.id)"
                    class="cursor-pointer group/poster flex-shrink-0 transition-transform duration-300 hover:scale-110 hover:z-50 origin-center"
                    style="width: 190px;"
                  >
                    <div class="aspect-[2/3] rounded-2xl overflow-hidden mb-3 relative shadow-lg transform transition-transform duration-500">
                      <div class="absolute inset-0 bg-black/20 group-hover/poster:bg-transparent transition-colors z-10"></div>
                      <img 
                        :src="movie.poster_path" 
                        :alt="movie.title" 
                        class="w-full h-full object-cover" 
                      />
                    </div>
                    <p class="text-sm font-medium text-gray-300 group-hover/poster:text-white truncate transition-colors">{{ movie.title }}</p>
                    <p class="text-xs text-gray-500">{{ movie.year }}</p>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <div class="md:col-span-12
                    bg-gray-900/40 backdrop-blur-xl
                    border border-white/10 rounded-[32px]
                    p-8">

          <div class="grid grid-cols-2 gap-6 items-start">
            
            <!-- 카드 1 -->
            <div
              v-for="item in lifeMovies.slice(0,3)"
              :key="item.user.id"
              class="rounded-2xl bg-black/40 border border-white/10 p-4"
            >
              <div class="aspect-[2/3] overflow-hidden rounded-xl">
                <img
                  :src="`https://image.tmdb.org/t/p/w154${item.movie.poster_path}`"
                  class="w-full h-full object-cover"
                />
              </div>

              <div class="mt-3 text-center">
                <p class="text-xs text-purple-400 font-bold truncate">
                  {{ item.user.username }}
                </p>
                <p class="text-sm font-semibold truncate">
                  {{ item.movie.title }}
                </p>
                <p v-if="item.review" class="text-xs text-yellow-400">
                  ★ {{ item.review.rating }}/5
                </p>
              </div>
            </div>

            <!-- ⭐ 문구 카드 -->
            <div class="flex flex-col justify-center">
              <div class="inline-block px-3 py-1 rounded-full
                          bg-purple-500/20 border border-purple-500/30
                          text-purple-400 text-xs font-bold mb-3">
                CURATION
              </div>
              <h2 class="text-3xl font-bold leading-tight">
                인증회원들의<br />
                <span class="text-purple-400">인생 영화</span>
              </h2>
            </div>

          </div>
        </div>



        
        <router-link
        to="/community"
        class="md:col-span-12 group relative bg-gradient-to-r from-gray-900/60 to-gray-800/60 backdrop-blur-xl border border-white/10 rounded-[32px] p-8 overflow-hidden hover:border-white/20 transition-all duration-500 block"
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
            
            <div class="shrink-0 flex items-center justify-center text-green-400">
                <span class="text-sm font-bold">커뮤니티 입장</span>
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
            </div>

          </div>
        </router-link>

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

</script>

<style scoped>
@keyframes marquee {
  0% { transform: translateX(0); }
  /* 자연스러운 무한 스크롤을 위해 -50%로 설정 (원본+복제본 구조) */
  100% { transform: translateX(-800%); } 
}

.animate-marquee {
  animation: marquee 100s linear infinite;
  will-change: transform;
}

.animate-marquee:hover {
  animation-play-state: paused;
}
</style>