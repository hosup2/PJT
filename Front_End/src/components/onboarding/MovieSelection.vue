<template>
  <div class="movie-selection">
    <div class="content-wrapper">
      <h1 class="title">좋아하는 영화를 선택해주세요</h1>
      <p class="subtitle">최소 5개 이상 선택해주세요 ({{ selectedMovies.length }}/5)</p>

      <div class="movie-grid">
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
              <div class="check-circle">
                <svg class="check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
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
        <button class="btn-next" :disabled="selectedMovies.length < 5" @click="handleNext">
          다음
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Movie {
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

// Mock movie data - 실제로는 props.selectedGenres에 따라 필터링된 영화들을 API에서 가져와야 함
const allMovies: Movie[] = [
  { id: 1, title: '인터스텔라', poster: 'https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg', year: 2014, genres: ['sf', 'drama'] },
  { id: 2, title: '다크 나이트', poster: 'https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg', year: 2008, genres: ['action', 'crime'] },
  { id: 3, title: '기생충', poster: 'https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg', year: 2019, genres: ['drama', 'thriller'] },
  { id: 4, title: '어벤져스: 엔드게임', poster: 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', year: 2019, genres: ['action', 'sf'] },
  { id: 5, title: '코코', poster: 'https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg', year: 2017, genres: ['animation', 'fantasy'] },
  { id: 6, title: '헤어질 결심', poster: 'https://image.tmdb.org/t/p/w500/yXKmy4FMPIbhUH23NqYLbFpVCyh.jpg', year: 2022, genres: ['romance', 'thriller'] },
  { id: 7, title: '조커', poster: 'https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg', year: 2019, genres: ['drama', 'crime'] },
  { id: 8, title: '겨울왕국', poster: 'https://image.tmdb.org/t/p/w500/kgwjIb1CkFCMvESYlMG8mfjfAQW.jpg', year: 2013, genres: ['animation', 'fantasy'] },
  { id: 9, title: '인셉션', poster: 'https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg', year: 2010, genres: ['sf', 'thriller'] },
  { id: 10, title: '라라랜드', poster: 'https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg', year: 2016, genres: ['romance', 'drama'] },
  { id: 11, title: '설국열차', poster: 'https://image.tmdb.org/t/p/w500/koP1qo31J6H0s8SvbFTyTT0HHGG.jpg', year: 2013, genres: ['sf', 'action'] },
  { id: 12, title: '범죄도시', poster: 'https://image.tmdb.org/t/p/w500/jBJWaqoSCiARWtfV0GlqHrcdidd.jpg', year: 2017, genres: ['action', 'crime'] },
  { id: 13, title: '반지의 제왕', poster: 'https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg', year: 2001, genres: ['fantasy', 'adventure'] },
  { id: 14, title: '컨저링', poster: 'https://image.tmdb.org/t/p/w500/wVYREutTvI2tmxr6ujrHT704wGF.jpg', year: 2013, genres: ['horror', 'thriller'] },
  { id: 15, title: '쇼생크 탈출', poster: 'https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg', year: 1994, genres: ['drama'] },
  { id: 16, title: '어바웃 타임', poster: 'https://image.tmdb.org/t/p/w500/vPVN0ZRFH7zB4cwH8wJbnAHPZYA.jpg', year: 2013, genres: ['romance', 'comedy'] },
  { id: 17, title: '해리포터', poster: 'https://image.tmdb.org/t/p/w500/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg', year: 2001, genres: ['fantasy', 'adventure'] },
  { id: 18, title: '타이타닉', poster: 'https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg', year: 1997, genres: ['romance', 'drama'] },
  { id: 19, title: '매드 맥스', poster: 'https://image.tmdb.org/t/p/w500/hA2ple9q4qnwxp3hKVNhroipsir.jpg', year: 2015, genres: ['action', 'sf'] },
  { id: 20, title: '아바타', poster: 'https://image.tmdb.org/t/p/w500/6EiRUJpuoeQPghrs3YNktfnqOVh.jpg', year: 2009, genres: ['sf', 'fantasy'] },
];

const selectedMovies = ref<number[]>(props.selectedMovies);

// Filter movies based on selected genres (simple filtering)
const displayMovies = computed(() => {
  if (props.selectedGenres.length === 0) {
    return allMovies;
  }
  return allMovies.filter(movie => 
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

.movie-card.selected {
  transform: scale(1.05);
}

.movie-poster {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 2/3;
  margin-bottom: 12px;
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
  background: rgba(139, 92, 246, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-circle {
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.check-icon {
  width: 36px;
  height: 36px;
  color: #8B5CF6;
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

  .check-circle {
    width: 50px;
    height: 50px;
  }

  .check-icon {
    width: 30px;
    height: 30px;
  }
}
</style>