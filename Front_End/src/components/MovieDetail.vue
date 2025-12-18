<template>
  <div v-if="loading" class="text-center p-12">
    <p>Loading...</p>
  </div>
  <div v-else-if="error" class="text-center p-12 text-red-400">
    <p>{{ error }}</p>
  </div>
  <div v-else-if="movie" class="pb-12">
    <!-- Back Button -->
    <button
      @click="router.back()"
      class="flex items-center gap-2 text-gray-400 hover:text-gray-200 transition-colors mb-6"
    >
      <ArrowLeft class="w-5 h-5" />
      <span>뒤로가기</span>
    </button>

    <!-- Hero Section with Backdrop and Poster -->
    <div class="relative w-full h-[500px] mb-12 rounded-lg overflow-hidden">
      <!-- Background Backdrop Image -->
      <div class="absolute inset-0">
        <img
          :src="backdropUrl"
          :alt="movie.title"
          class="w-full h-full object-cover"
        />
        <!-- Gradient Overlay -->
        <div class="absolute inset-0 bg-gradient-to-r from-black/90 via-black/60 to-transparent"></div>
      </div>
      
      <!-- Content Container -->
      <div class="relative h-full flex items-center px-8 gap-8 max-w-7xl mx-auto">
        <!-- Movie Info on Left -->
        <div class="flex-1 z-10 max-w-2xl">
          <div class="flex items-center gap-4 mb-2">
            <h1 class="text-5xl font-bold">{{ movie.title }}</h1>
            <button
              @click="handleLikeMovie"
              :disabled="!isLoggedIn"
              :class="[
                'p-2 rounded-full transition-colors',
                isMovieLiked ? 'bg-red-500/20 text-red-400' : 'bg-gray-800 text-gray-400',
                isLoggedIn ? 'hover:bg-red-500/30 cursor-pointer' : 'cursor-not-allowed opacity-50'
              ]"
            >
              <Heart :class="['w-8 h-8', isMovieLiked && 'fill-current']" />
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

          <!-- Rating Display in Hero -->
          <div class="flex items-center gap-6 text-white">
            <div class="flex items-center gap-2">
              <Star class="w-8 h-8 text-yellow-400 fill-yellow-400" />
              <span class="text-4xl font-bold">{{ movie.stats.avg_rating.toFixed(1) }}</span>
            </div>
            
            <div v-if="movie.tmdb_rating" class="border-l border-white/30 pl-6">
              <p class="text-sm text-gray-300 mb-1">TMDb</p>
              <p class="text-2xl">{{ movie.tmdb_rating.toFixed(1) }}/10</p>
            </div>
          </div>
        </div>

        <!-- Small Poster on Right -->
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

    <!-- Main Content Grid -->
    <div class="grid md:grid-cols-[2fr,1fr] gap-8 max-w-7xl mx-auto px-4">
      <!-- Left Column -->
      <div>
        <!-- Overview -->
        <div class="mb-8">
          <h2 class="text-2xl font-bold mb-3">줄거리</h2>
          <p class="text-gray-300 leading-relaxed">{{ movie.overview }}</p>
        </div>

        <!-- Rating Distribution -->
        <div class="mb-8">
          <RatingDistributionChart 
            :movie-id="parseInt(id)"
            :distribution="movie.stats.rating_distribution"
            :total-count="movie.stats.rating_count"
          />
        </div>

        <!-- Comments Section -->
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

      <!-- Right Column - Actions -->
      <div>
        <div class="bg-gray-900 rounded-lg p-6 sticky top-24">
          <!-- Rating Stats -->
          <div class="mb-6 pb-6 border-b border-gray-800">
            <div class="flex items-center gap-3 mb-2">
              <Star class="w-6 h-6 text-yellow-400 fill-yellow-400" />
              <span class="text-3xl font-bold">{{ movie.stats.avg_rating.toFixed(1) }}</span>
            </div>
            <p class="text-sm text-gray-400">
              {{ movie.stats.rating_count.toLocaleString() }}명 평가
            </p>
          </div>

          <!-- User Rating -->
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
import { ref, onMounted, computed, inject } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeft, Calendar, Clock, Star, Heart } from 'lucide-vue-next';
import StarRating from './StarRating.vue';
import RatingDistributionChart from './RatingDistributionChart.vue';
import CommentSection from './CommentSection.vue';

// --- Interfaces ---
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
        // Add a cache-busting parameter
        _: new Date().getTime(),
      },
    });
    movie.value = response.data;

    // Set initial user-specific state
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

    // 영화 데이터 전체를 새로고침하여 댓글 목록 업데이트
    await fetchMovieData();
    
    // 입력 필드 초기화
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

  // Optimistic update
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
    // Revert optimistic update on failure
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

  const yy = String(date.getFullYear()); // year
  const mm = String(date.getMonth() + 1).padStart(2, '0'); // month
  const dd = String(date.getDate()).padStart(2, '0'); // day

  return `${yy}.${mm}.${dd}`;
};

</script>