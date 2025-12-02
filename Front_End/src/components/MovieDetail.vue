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
      <!-- Poster -->
      <div class="relative aspect-[2/3] rounded-lg overflow-hidden bg-gray-800">
        <img
          :src="movie.poster_path"
          :alt="movie.title"
          class="w-full h-full object-cover"
        />
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
            <StarRating
              :initial-rating="userRating"
              @change="handleRatingChange"
            />
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

    <!-- Ratings List -->
    <div>
      <RatingsList :ratings="movieRatings" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ArrowLeft, Calendar, Clock, Star } from 'lucide-vue-next';
import { mockMovies, mockRatings } from '../data/mockData';
import StarRating from './StarRating.vue';
import RatingDistributionChart from './RatingDistributionChart.vue';
import RatingsList from './RatingsList.vue';

interface Props {
  movieId: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  back: [];
}>();

const userRating = ref(0);

const movie = computed(() => mockMovies.find(m => m.id === props.movieId));
const movieRatings = computed(() => mockRatings.filter(r => r.movie_id === props.movieId));

const handleRatingChange = (rating: number) => {
  userRating.value = rating;
};
</script>
