<template>
  <div class="grid-container">
    <div class="grid-header">
      <p class="grid-subtitle">최근 가장 많이 평가된 영화들</p>
    </div>
    
    <div class="cinema-grid">
      <button
        v-for="movie in movies"
        :key="movie.id"
        @click="navigateToMovie(movie.id)"
        class="movie-card"
      >
        <div class="poster-wrapper">
          <img
            :src="getImageUrl(movie.poster_path)"
            :alt="movie.title"
            class="poster-image"
          />
          <div class="poster-overlay">
            <div class="overlay-content">
              <div class="rating-badge">
                <Star class="icon-star" />
                <span class="rating-score">{{ movie.tmdb_rating ? movie.tmdb_rating.toFixed(1) : '0.0' }}</span>
              </div>
              <p class="rating-count" v-if="movie.stats">
                {{ movie.stats.rating_count.toLocaleString() }}명 평가
              </p>
            </div>
          </div>
        </div>

        <div class="movie-info">
          <h3 class="movie-title">
            {{ movie.title }}
          </h3>
          <p class="movie-year">
            {{ new Date(movie.release_date).getFullYear() }}
          </p>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { Star } from 'lucide-vue-next';

// 기존 인터페이스 유지
interface Movie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
  tmdb_rating?: number; // 상위 컴포넌트 데이터 구조 고려하여 optional 처리
  stats?: {
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

<style scoped>
/* 🎨 MIA Cinema Grid Style */
.grid-container {
  width: 100%;
}

.grid-header {
  margin-bottom: 2rem;
}

.grid-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  letter-spacing: 0.02em;
}

/* GRID LAYOUT */
.cinema-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 2rem;
}

/* CARD ITEM */
.movie-card {
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  text-align: left;
  transition: transform 0.3s ease;
  width: 100%;
}

.movie-card:hover {
  transform: translateY(-8px);
}

/* POSTER */
.poster-wrapper {
  position: relative;
  aspect-ratio: 2/3;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  background: rgba(255, 255, 255, 0.05);
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-card:hover .poster-image {
  transform: scale(1.05);
}

/* OVERLAY */
.poster-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.9) 0%,
    rgba(0, 0, 0, 0.4) 40%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.movie-card:hover .poster-overlay {
  opacity: 1;
}

.overlay-content {
  width: 100%;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #fbbf24; /* Yellow */
  margin-bottom: 0.25rem;
}

.icon-star {
  width: 1rem;
  height: 1rem;
  fill: currentColor;
}

.rating-score {
  font-size: 0.875rem;
  font-weight: 700;
  color: #fbbf24;
}

.rating-count {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
}

/* INFO TEXT */
.movie-info {
  padding: 0 0.25rem;
}

.movie-title {
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 0.25rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.2s ease;
}

.movie-card:hover .movie-title {
  color: #8b5cf6; /* Highlight Purple */
}

.movie-year {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

/* RESPONSIVE */
@media {
  .cinema-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 2rem;
  }
}

@media (max-width: 1200px) {
  .cinema-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 900px) {
  .cinema-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .cinema-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

</style>