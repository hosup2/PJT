<template>
  <div v-if="loading" class="text-center p-12">
    <p>Loading...</p>
  </div>
  <div v-else-if="error" class="text-center p-12 text-red-400">
    <p>{{ error }}</p>
  </div>
  <div v-else-if="movie">
    <button
      @click="router.back()"
      class="flex items-center gap-2 text-gray-400 hover:text-gray-200 transition-colors mb-6"
    >
      <ArrowLeft class="w-5 h-5" />
      <span>뒤로가기</span>
    </button>

<div class="grid md:grid-cols-[300px,1fr] gap-8 mb-12">
 <div class="justify-self-center">
  <div
  class="relative rounded-lg overflow-hidden bg-gray-800 block mx-auto"
  style="width: 300px; height: 400px;"
  >
  <img
  :src="backdropUrl"
  :alt="movie.title"
  class="w-full h-full object-cover"
  />
</div>
</div>

      <!-- Info -->
      <div>
        <h1 class="text-4xl mb-2">{{ movie.title }}</h1>
        <p v-if="movie.original_title !== movie.title" class="text-xl text-gray-400 mb-4">
          {{ movie.original_title }}
        </p>

        <div class="flex flex-wrap items-center gap-4 mb-6 text-gray-400">
          <div class="flex items-center gap-2">
            <Calendar class="w-4 h-4" />
            <span>{{ new Date(movie.release_date).getFullYear() }}</span>
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
            class="px-3 py-1 bg-gray-800 rounded-full text-sm"
          >
            {{ genre }}
          </span>
        </div>

        <div class="bg-gray-900 rounded-lg p-6 mb-6">
          <div class="flex items-center gap-6 mb-4">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <Star class="w-6 h-6 text-yellow-400 fill-yellow-400" />
                <span class="text-3xl">{{ movie.stats.avg_rating.toFixed(1) }}</span>
              </div>
              <p class="text-sm text-gray-400">
                {{ movie.stats.rating_count.toLocaleString() }}명 평가
              </p>
            </div>
            
            <div v-if="movie.tmdb_rating" class="border-l border-gray-700 pl-6">
              <p class="text-sm text-gray-400 mb-1">TMDb</p>
              <p class="text-xl">{{ movie.tmdb_rating.toFixed(1) }}/10</p>
            </div>
            
            <div v-if="movie.imdb_rating" class="border-l border-gray-700 pl-6">
              <p class="text-sm text-gray-400 mb-1">IMDb</p>
              <p class="text-xl">{{ movie.imdb_rating.toFixed(1) }}/10</p>
            </div>
          </div>

          <div class="border-t border-gray-800 pt-4">
            <p class="text-sm text-gray-400 mb-3">이 영화를 평가해주세요</p>
            <div v-if="isLoggedIn">
              <StarRating
                :initial-rating="userRating"
                @change="handleRatingChange"
              />
            </div>
            <button
              v-else
              @click="emit('openAuth')"
              class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
            >
              로그인하고 평가하기
            </button>
          </div>

          <!-- Like Button -->
          <div class="border-t border-gray-800 pt-4 mt-4">
            <button
              @click="handleLikeMovie"
              :disabled="!isLoggedIn"
              :class="[
                'flex items-center gap-2 transition-colors',
                isMovieLiked ? 'text-red-400' : 'text-gray-400',
                isLoggedIn ? 'hover:text-red-400 cursor-pointer' : 'cursor-not-allowed'
              ]"
            >
              <Heart :class="['w-5 h-5', isMovieLiked && 'fill-current']" />
              <span>{{ isMovieLiked ? '좋아요 취소' : '좋아요' }}</span>
              <span class="text-sm text-gray-500">({{ movieLikesCount }})</span>
            </button>
          </div>
        </div>

        <div class="mb-6">
          <h2 class="text-xl mb-3">줄거리</h2>
          <p class="text-gray-300 leading-relaxed">{{ movie.overview }}</p>
        </div>
      </div>
    </div>

    <!-- Rating Distribution -->
    <div class="mb-12">
      <RatingDistributionChart 
        :movie-id="parseInt(id)"
        :distribution="movie.stats.rating_distribution"
        :total-count="movie.stats.rating_count"
      />
    </div>

    <!-- Comments Section -->
    <div>
      <h2 class="text-2xl mb-6">리뷰 ({{ comments.length }})</h2>
      <CommentSection
        :comments="comments"
        :is-logged-in="isLoggedIn"
        @submit-comment="handleSubmitComment"
        @like-comment="handleLikeComment"
        @navigate-to-user="handleNavigateToUser"
        @open-auth="emit('openAuth')"
      />
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
  comments: Comment[]; // Assuming comments are nested
}

interface Comment {
  id: number;
  user_id: number;
  username: string;
  profile_image: string;
  review_content: string;
  spoiler: boolean;
  created_at: string;
  likes_count: number;
  isLiked: boolean;
}

interface User {
  id: number;
  username: string;
}

// --- Props & Emits ---
const props = defineProps<{
  id: string; // From router params
}>();

const emit = defineEmits<{
  openAuth: [];
}>();


// --- State ---
const router = useRouter();
const movie = ref<Movie | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

// Injected global state
const isLoggedIn = inject<ref<boolean>>('isLoggedIn', ref(false));
const currentUser = inject<ref<User | null>>('currentUser', ref(null));


// --- Data Fetching ---
onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${props.id}/`);
    // Assuming the API returns the full movie object structure including comments
    // and correctly formatted poster/backdrop paths
    movie.value = response.data;
  } catch (err) {
    console.error(`Failed to fetch movie ${props.id}:`, err);
    error.value = '영화 정보를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
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
        return `https://image.tmdb.org/t/p/w1280${movie.value.backdrops}`;
    }
    return movie.value?.backdrops || '';
});


// --- Event Handlers ---
const userRating = ref(0); // This would also come from API if user has rated
const isMovieLiked = ref(false); // This would come from API
const movieLikesCount = ref(movie.value?.stats.rating_count || 0); // This is an approximation

const handleRatingChange = (rating: number) => {
  if (!isLoggedIn.value) return emit('openAuth');
  userRating.value = rating;
  console.log(`User rating changed to ${rating}. TODO: Implement API call.`);
  // TODO: API POST to /movies/{props.id}/rate/
};

const handleLikeMovie = () => {
  if (!isLoggedIn.value) return emit('openAuth');
  isMovieLiked.value = !isMovieLiked.value;
  movieLikesCount.value += isMovieLiked.value ? 1 : -1;
  console.log(`Movie like status: ${isMovieLiked.value}. TODO: Implement API call.`);
  // TODO: API POST to /movies/{props.id}/like/
};

const handleSubmitComment = (content: string, spoiler: boolean) => {
  console.log(`Submitting comment: ${content}. TODO: Implement API call.`);
  // TODO: API POST to /movies/{props.id}/comments/
  // On success, re-fetch comments or optimistically add to list.
};

const handleLikeComment = (commentId: number) => {
  console.log(`Liking comment ${commentId}. TODO: Implement API call.`);
  // TODO: API POST to /comments/{commentId}/like/
};

const handleNavigateToUser = (userId: number) => {
  router.push({ name: 'UserProfile', params: { userId } });
};

</script>