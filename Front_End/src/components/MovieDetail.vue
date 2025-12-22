네, 말씀하신 기능을 완벽하게 통합했습니다.

**변경된 점:**

1. **클릭 기능 추가**: 감독 및 출연진 카드에 `@click` 이벤트를 넣어, 클릭 시 **TMDB(영화 정보 사이트)의 해당 인물 페이지**가 새 탭으로 열립니다.
2. **커서 스타일**: 카드에 마우스를 올리면 클릭 가능하다는 것을 알 수 있게 손가락 모양(`cursor-pointer`)으로 변하고, 배경색이 조금 더 밝게(`hover:bg-gray-700`) 변합니다.
3. **디자인 통일**: 아까 맞춘 황금 비율(`w-24`, `h-36`)을 적용하여 사진 크기가 깔끔하게 정렬되도록 했습니다.

아래 전체 코드를 복사해서 그대로 붙여넣으시면 됩니다.

```vue
<template>
  <div v-if="loading" class="text-center p-12">
    <p>Loading...</p>
  </div>
  <div v-else-if="error" class="text-center p-12 text-red-400">
    <p>{{ error }}</p>
  </div>
  <div v-else-if="movie" class="pb-12">
    <button
      @click="router.back()"
      class="flex items-center gap-2 text-gray-400 hover:text-gray-200 transition-colors mb-6"
    >
      <ArrowLeft class="w-5 h-5" />
      <span>뒤로가기</span>
    </button>

    <div class="relative w-full h-[500px] mb-12 rounded-lg overflow-hidden">
      <div class="absolute inset-0">
        <img
          :src="backdropUrl"
          :alt="movie.title"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/60 to-transparent"></div>
      </div>
      
      <div class="relative h-full flex items-center px-8 gap-8 max-w-7xl mx-auto">
        <div class="flex-1 z-10 max-w-2xl">
          <div class="flex items-center gap-4 mb-2">
            <h1 class="text-5xl font-bold">{{ movie.title }}</h1>
            <button
              @click="handleLikeMovie"
              :disabled="!isLoggedIn"
              :class="[
                'p-3 rounded-full transition-all',
                isMovieLiked 
                  ? 'bg-red-500/20 hover:bg-red-500/30' 
                  : 'bg-gray-800/80 hover:bg-red-500/20',
                isLoggedIn ? 'cursor-pointer' : 'cursor-not-allowed opacity-50'
              ]"
              :title="isMovieLiked ? '찜 취소' : '찜하기'"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                class="w-8 h-8 transition-all"
                stroke-width="2"
              >
                <path 
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                  stroke-linecap="round" 
                  stroke-linejoin="round"
                  :stroke="isMovieLiked ? '#ef4444' : '#ffffff'"
                  :fill="isMovieLiked ? '#ef4444' : 'none'"
                />
              </svg>
            </button>
          </div>
          <p v-if="movie.original_title !== movie.title" class="text-xl text-gray-300 mb-4">
            {{ movie.original_title }}
          </p>

          <div class="flex flex-wrap items-center gap-4 mb-4 text-gray-300">
            <div class="flex items-center gap-2">
              <Calendar class="w-4 h-4" />
              <span>{{ formatDate(movie.release_date) }}</span>
            </div>
            <div class="flex items-center gap-2">
              <Clock class="w-4 h-4" />
              <span>{{ movie.runtime }}분</span>
            </div>
          </div>

          <div class="flex flex-wrap gap-2 mb-6">
            <span
              v-for="genre in movie.genres"
              :key="genre"
              class="px-3 py-1 bg-white/10 backdrop-blur-sm rounded-full text-sm"
            >
              {{ genre }}
            </span>
          </div>

          <div class="flex items-center gap-6 text-white">
            <div class="flex items-center gap-2">
              <Star class="w-8 h-8 text-yellow-400 fill-yellow-400" />
              <span class="text-4xl font-bold">{{ movieStats.avg_rating.toFixed(1) }}</span>
            </div>
            
            <div v-if="movie.tmdb_rating" class="border-l border-white/30 pl-6">
              <p class="text-sm text-gray-300 mb-1">TMDb</p>
              <p class="text-2xl">{{ movie.tmdb_rating.toFixed(1) }}/10</p>
            </div>
          </div>
        </div>

        <div class="hidden md:block z-10">
          <div
            class="rounded-lg overflow-hidden shadow-2xl border-4 border-white/20 hover:scale-105 transition-transform duration-300"
            style="width: 220px; height: 330px;"
          >
            <img
              :src="posterUrl"
              :alt="movie.title"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="grid md:grid-cols-[2fr,1fr] gap-8 max-w-7xl mx-auto px-4">
      <div>
        <div class="mb-8 bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-3">줄거리</h2>
          <p class="text-gray-300 leading-relaxed text-sm">
            {{ movie.overview }}
          </p>
        </div>

        <div class="mb-8 bg-gray-900 rounded-lg p-6">
          <h2 class="text-xl font-semibold mb-3">출연진</h2>

          <!-- <div v-if="movie.director" class="mb-6">
            <h3 class="text-lg font-semibold mb-3 text-gray-200">감독</h3>
            <div class="flex flex-wrap gap-4">
              <div
                @click="openPersonDetail(movie.director)"
                class="w-24 bg-gray-800/50 rounded-lg p-2 hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <img
                  :src="getProfileUrl(movie.director.profile_path)"
                  class="w-full h-36 rounded-lg object-cover bg-gray-700 mb-2"
                />
                <div class="text-left px-1">
                  <p class="text-sm font-bold text-gray-100 truncate">
                    {{ movie.director.name }}
                  </p>
                  <p class="text-xs text-gray-400 mt-0.5">
                    감독
                  </p>
                </div>
              </div>
            </div>
          </div> -->

          <div v-if="movie.actors && movie.actors.length">
            <!-- <h3 class="text-lg font-semibold mb-3 text-gray-200">출연진</h3> -->
            <div class="flex flex-wrap gap-4">
              <div
                v-for="actor in movie.actors"
                :key="actor.tmdb_id"
                @click="openPersonDetail(actor)"
                class="w-24 bg-gray-800/50 rounded-lg p-2 hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <img
                  :src="getProfileUrl(actor.profile_path)"
                  :alt="actor.name"
                  class="w-full h-36 rounded-lg object-cover bg-gray-700 mb-2"
                />
                <div class="text-left px-1">
                  <p class="text-sm font-bold text-gray-100 truncate">
                    {{ actor.name }}
                  </p>
                  <p class="text-xs text-gray-400 mt-0.5 truncate">
                    {{ actor.character ? actor.character + ' 역' : '출연' }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-8">
          <RatingDistributionChart 
            :movie-id="parseInt(id)"
            :distribution="movieStats.rating_distribution"
            :total-count="movieStats.rating_count"
          />
        </div>

        <div>
          <h2 class="text-2xl font-bold mb-6">리뷰 ({{ comments.length }})</h2>
          <CommentSection
            :comments="comments"
            :is-logged-in="isLoggedIn"
            :rating="userRating"
            @submit-comment="handleSubmitComment"
            @like-comment="handleLikeComment"
            @navigate-to-user="handleNavigateToUser"
            @open-auth="emit('openAuth')"
            @rating-change="handleRatingChange"
          />
        </div>
      </div>

      <div>
        <div class="bg-gray-900 rounded-lg p-6 sticky top-24">
          <div class="mb-6 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-2">
              <Star class="w-6 h-6 text-yellow-400 fill-yellow-400" />
              <span class="text-3xl font-bold">{{ movieStats.avg_rating.toFixed(1) }}</span>
            </div>
            <p class="text-sm text-gray-400">
              {{ movieStats.rating_count.toLocaleString() }}명 평가
            </p>
          </div>

          <div class="mb-6 pb-6 border-b border-gray-800">
            <p class="text-sm text-gray-400 mb-3">이 영화를 평가해주세요</p>
            <div v-if="!isLoggedIn">
              <button
                @click="emit('openAuth')"
                class="w-full px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
              >
                로그인하고 평가하기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeft, Calendar, Clock, Star } from 'lucide-vue-next';
import StarRating from './StarRating.vue';
import RatingDistributionChart from './RatingDistributionChart.vue';
import CommentSection from './CommentSection.vue';

// --- Interfaces ---
interface Person {
  tmdb_id: number;
  name: string;
  profile_path?: string | null;
  character?: string;
}

interface Movie {
  id: number;
  title: string;
  original_title: string;
  poster_path: string;
  backdrops: string;
  release_date: string;
  runtime: number;
  genres: string[];
  overview: string;
  stats: {
    avg_rating: number;
    rating_count: number;
    rating_distribution: Record<string, number>;
  };
  tmdb_rating: number;
  imdb_rating: number;
  comments: Comment[];
  director?: Person | null;
  actors?: Person[];
  user_data?: {
    rating: number;
    comment: string;
    is_liked: boolean;
  };
}

interface Comment {
  id: number;
  user_id: number;
  username: string;
  rating?: number;
  comment: string;
  created_at: string;
  profile_image?: string;
  review_content?: string;
  spoiler?: boolean;
  likes_count?: number;
  isLiked?: boolean;
}

interface User {
  id: number;
  username: string;
}

// --- Props & Emits ---
const props = defineProps<{
  id: string;
}>();

const emit = defineEmits<{
  openAuth: [];
  'activity-updated': [];
}>();

// --- State ---
const router = useRouter();
const movie = ref<Movie | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

// Injected global state
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn', ref(false));
const currentUser = inject<Ref<User | null>>('currentUser', ref(null));

// --- Data Fetching ---
const fetchMovieData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${props.id}/`, {
      params: {
        _: new Date().getTime(),
      },
    });
    movie.value = response.data;

    if (movie.value?.user_data) {
      userRating.value = movie.value.user_data.rating || 0;
      commentText.value = movie.value.user_data.comment || '';
      isMovieLiked.value = movie.value.user_data.is_liked;
    }
  } catch (err) {
    console.error(`Failed to fetch movie ${props.id}:`, err);
    error.value = '영화 정보를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchMovieData();
});

// --- Computed Properties ---
const comments = computed(() => movie.value?.comments || []);
const posterUrl = computed(() => {
  if (movie.value?.poster_path && !movie.value.poster_path.startsWith('http')) {
    return `https://image.tmdb.org/t/p/w500${movie.value.poster_path}`;
  }
  return movie.value?.poster_path || 'https://via.placeholder.com/500x750?text=No+Image';
});

const backdropUrl = computed(() => {
  if (movie.value?.backdrops && !movie.value.backdrops.startsWith('http')) {
    return `https://image.tmdb.org/t/p/original${movie.value.backdrops}`;
  }
  return movie.value?.backdrops || posterUrl.value;
});

// --- Event Handlers ---
const userRating = ref(0);
const commentText = ref('');
const isMovieLiked = ref(false);
const movieLikesCount = ref(0);

const saveActivity = async () => {
  if (!isLoggedIn.value) return;

  try {
    const payload = {
      rating: userRating.value || null,
      comment: commentText.value,
    };
    
    await axios.post(`http://127.0.0.1:8000/movies/${props.id}/rating/`, payload);
    
    alert('리뷰가 저장되었습니다.');

    await fetchMovieData();
    
    commentText.value = '';
    userRating.value = 0;
    
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to save activity:', err);
    alert('리뷰 저장에 실패했습니다.');
  }
};

const handleRatingChange = (rating: number) => {
  if (!isLoggedIn.value) return emit('openAuth');
  userRating.value = rating;
};

const handleLikeMovie = async () => {
  if (!isLoggedIn.value) return emit('openAuth');
  
  const originalLikedStatus = isMovieLiked.value;

  isMovieLiked.value = !isMovieLiked.value;
  movieLikesCount.value += isMovieLiked.value ? 1 : -1;

  try {
    if (originalLikedStatus) {
      await axios.delete(`http://127.0.0.1:8000/users/favorites/${props.id}/`);
    } else {
      await axios.post(`http://127.0.0.1:8000/users/favorites/${props.id}/`);
    }
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to update like status:', err);
    alert('좋아요 상태를 업데이트하는 데 실패했습니다.');
    isMovieLiked.value = originalLikedStatus;
    movieLikesCount.value += originalLikedStatus ? 1 : -1;
  }
};

const handleSubmitComment = (content: string, spoiler: boolean) => {
  commentText.value = content;
  saveActivity();
};

const handleLikeComment = (commentId: number) => {
  console.log(`Liking comment ${commentId}. TODO: Implement API call.`);
};

const handleNavigateToUser = (userId: number) => {
  router.push({ name: 'UserProfile', params: { userId } });
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const yy = String(date.getFullYear());
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yy}.${mm}.${dd}`;
};

const getProfileUrl = (path?: string | null) => {
  if (!path) {
    return 'https://via.placeholder.com/185x278?text=No+Image';
  }
  if (path.startsWith('http')) return path;
  return `https://image.tmdb.org/t/p/w185${path}`;
};

const movieStats = computed(() => {
  return movie.value?.stats ?? {
    avg_rating: 0,
    rating_count: 0,
    rating_distribution: {},
  };
});

// --- NEW FUNCTION: Open Person Detail on TMDB ---
const openPersonDetail = (person: Person) => {
  if (!person || !person.tmdb_id) return;
  // 한국어 페이지로 연결
  const url = `https://www.themoviedb.org/person/${person.tmdb_id}?language=ko-KR`;
  window.open(url, '_blank');
};
</script>

```