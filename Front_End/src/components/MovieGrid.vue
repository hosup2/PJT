<template>
  <div>
    <div class="mb-8">
      <p class="text-gray-400">최근 가장 많이 평가된 영화들</p>
    </div>
    
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      <button
        v-for="movie in movies"
        :key="movie.id"
        @click="navigateToMovie(movie.id)"
        class="group cursor-pointer text-left"
      >
        <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
          <img
            :src="getImageUrl(movie.poster_path)"
            :alt="movie.title"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent opacity-0 group-hover:opacity-100 transition-opacity">
            <div class="absolute bottom-3 left-3 right-3">
              <div class="flex items-center gap-1 text-yellow-400 mb-1">
                <Star class="w-4 h-4 fill-yellow-400" />
                <span class="text-sm">{{ movie.tmdb_rating.toFixed(1) }}</span>
              </div>
              <p class="text-xs text-gray-300">{{ movie.stats.rating_count.toLocaleString() }}명 평가</p>
            </div>
          </div>
        </div>
        <h3 class="line-clamp-2 group-hover:text-purple-400 transition-colors">
          {{ movie.title }}
        </h3>
        <p class="text-sm text-gray-500 mt-1">
          {{ new Date(movie.release_date).getFullYear() }}
        </p>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { Star } from 'lucide-vue-next';

interface Movie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  stats: {
    avg_rating: number;
    rating_count: number;
  };
}

defineProps<{
  movies: Movie[];
}>();

const router = useRouter();

const navigateToMovie = (id: number) => {
  router.push({ name: 'MovieDetail', params: { id } });
};

const getImageUrl = (path: string | null) => {
  if (!path) {
    return 'https://via.placeholder.com/500x750?text=No+Image';
  }
  return `https://image.tmdb.org/t/p/w500${path}`;
};
</script>