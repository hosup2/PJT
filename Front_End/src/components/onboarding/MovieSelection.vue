<template>
  <div class="movie-selection">
    <div class="content-wrapper">
      <h1 class="title">좋아하는 영화를 선택해주세요</h1>
      <p class="subtitle">최소 2개 이상 선택해주세요 ({{ selectedMovies.length }}/2)</p>

      <div v-if="loading" class="text-center py-16">
        <p class="text-gray-400">영화 목록을 불러오는 중...</p>
      </div>
      <div v-else-if="error" class="text-center py-16">
        <p class="text-red-400">{{ error }}</p>
      </div>
      <div v-else class="movie-grid">
        <button
          v-for="movie in displayMovies"
          :key="movie.id"
          class="movie-card"
          :class="{ selected: isSelected(movie.id) }"
          @click="toggleMovie(movie.id)"
        >
          <div class="movie-poster">
            <img :src="movie.poster" :alt="movie.title" />
            <div v-if="isSelected(movie.id)" class="selected-overlay">
            </div>
          </div>
          <div class="movie-info">
            <h3 class="movie-title">{{ movie.title }}</h3>
            <p class="movie-year">{{ movie.year }}</p>
          </div>
        </button>
      </div>

      <div class="action-buttons">
        <button class="btn-back" @click="$emit('back')">
          <svg class="back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          이전
        </button>
        <button class="btn-next" :disabled="selectedMovies.length < 2" @click="handleNext">
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

interface Movie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  genres: { name: string }[]; // Assuming genres are objects with a name property
}

interface DisplayMovie {
    id: number;
    title: string;
    poster: string;
    year: number;
    genres: string[];
}

interface Props {
  selectedGenres: string[];
  selectedMovies: number[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update-selection', movies: number[]): void;
  (e: 'next'): void;
  (e: 'back'): void;
}>();

const allMovies = ref<DisplayMovie[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/movies/?ordering=-tmdb_rating&limit=40');
    const moviesData: Movie[] = response.data.results || response.data;
    allMovies.value = moviesData.map(movie => ({
      id: movie.id,
      title: movie.title,
      poster: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 'https://via.placeholder.com/500x750?text=No+Image',
      year: new Date(movie.release_date).getFullYear(),
      genres: movie.genres.map(g => g.name.toLowerCase()), // Assuming genre names need to be lowercased
    }));
  } catch (err) {
    console.error('Failed to fetch movies for onboarding:', err);
    error.value = '영화를 불러오는데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});


const selectedMovies = ref<number[]>(props.selectedMovies);

// Filter movies based on selected genres (simple filtering)
const displayMovies = computed(() => {
  if (props.selectedGenres.length === 0) {
    return allMovies.value;
  }
  return allMovies.value.filter(movie => 
    movie.genres.some(genre => props.selectedGenres.includes(genre))
  );
});

const isSelected = (movieId: number) => {
  return selectedMovies.value.includes(movieId);
};

const toggleMovie = (movieId: number) => {
  if (isSelected(movieId)) {
    selectedMovies.value = selectedMovies.value.filter(id => id !== movieId);
  } else {
    selectedMovies.value = [...selectedMovies.value, movieId];
  }
  emit('update-selection', selectedMovies.value);
};

const handleNext = () => {
  emit('next');
};
</script>

<style scoped>
.movie-selection {
  min-height: calc(100vh - 160px);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.title {
  font-size: 36px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 12px;
  background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  text-align: center;
  color: #A1A1AA;
  font-size: 16px;
  margin-bottom: 48px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.movie-card {
  background: transparent;
  border: none;
  cursor: pointer;
  transition: transform 0.3s ease;
  padding: 0;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-card.selected .movie-poster {
  box-shadow: 0 0 0 4px #8B5CF6;
}

.movie-poster {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2/3;
  margin-bottom: 12px;
  transition: box-shadow 0.3s ease;
}

.movie-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.selected-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.movie-card.selected .selected-overlay {
  opacity: 1;
}

.movie-info {
  text-align: left;
}

.movie-title {
  font-size: 14px;
  font-weight: 600;
  color: #F8F8F8;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.movie-year {
  font-size: 12px;
  color: #A1A1AA;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}

.btn-back,
.btn-next {
  font-weight: bold;
  font-size: 16px;
  padding: 16px 48px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-back {
  background: #27272A;
  color: #F8F8F8;
}

.btn-back:hover {
  background: #3F3F46;
}

.back-icon {
  width: 20px;
  height: 20px;
}

.btn-next {
  background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%);
  color: white;
}

.btn-next:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.4);
}

.btn-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .title {
    font-size: 28px;
  }

  .movie-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 16px;
  }

  .movie-title {
    font-size: 13px;
  }
}
</style>