<template>
  <div v-if="movie">
    <button
      @click="emit('back')"
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
  :src="movie.backdrops"
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
        :movie-id="movieId"
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
import { ref, computed } from 'vue';
import { ArrowLeft, Calendar, Clock, Star, Heart } from 'lucide-vue-next';
import { mockMovies, mockComments } from '../data/mockData';
import StarRating from './StarRating.vue';
import RatingDistributionChart from './RatingDistributionChart.vue';
import CommentSection from './CommentSection.vue';

interface Props {
  movieId: number;
  isLoggedIn: boolean;
  currentUserId?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  back: [];
  openAuth: [];
  navigateToUser: [userId: number];
}>();

const userRating = ref(0);
const isMovieLiked = ref(false);
const movieLikesCount = ref(142);

const movie = computed(() => mockMovies.find(m => m.id === props.movieId));
const comments = ref(mockComments.filter(c => c.movie_id === props.movieId));

const handleRatingChange = (rating: number) => {
  userRating.value = rating;
  // TODO: API call to save rating
};

const handleLikeMovie = () => {
  if (!props.isLoggedIn) return;
  isMovieLiked.value = !isMovieLiked.value;
  movieLikesCount.value += isMovieLiked.value ? 1 : -1;
  // TODO: API call to save like
};

const handleSubmitComment = (content: string, spoiler: boolean) => {
  // TODO: API call to submit comment
  const newComment = {
    id: Date.now(),
    user_id: props.currentUserId || 1,
    movie_id: props.movieId,
    review_content: content,
    spoiler: spoiler,
    created_at: new Date().toISOString(),
    username: '현재 사용자', // TODO: Get from current user
    profile_image: 'https://i.pravatar.cc/150?img=1',
    likes_count: 0,
    isLiked: false
  };
  comments.value.unshift(newComment);
};

const handleLikeComment = (commentId: number) => {
  const comment = comments.value.find(c => c.id === commentId);
  if (comment) {
    comment.isLiked = !comment.isLiked;
    comment.likes_count += comment.isLiked ? 1 : -1;
    // TODO: API call to save like
  }
};

const handleNavigateToUser = (userId: number) => {
  emit('navigateToUser', userId);
};
</script>