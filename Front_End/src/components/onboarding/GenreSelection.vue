<template>
  <div class="genre-selection">
    <div class="content-wrapper">
      <h1 class="title">어떤 장르를 좋아하시나요?</h1>
      <p class="subtitle">최소 2개 이상 선택해주세요</p>

      <div class="genre-grid">
        <button
          v-for="genre in genres"
          :key="genre.id"
          class="genre-card"
          :class="{ selected: isSelected(genre.id) }"
          @click="toggleGenre(genre.id)"
        >
          <div class="genre-icon">{{ genre.emoji }}</div>
          <div class="genre-name">{{ genre.name }}</div>
        </button>
      </div>

      <div class="action-buttons">
        <button class="btn-next" :disabled="selectedGenres.length < 2" @click="handleNext">
          다음 ({{ selectedGenres.length }}/2)
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Genre {
  id: string;
  name: string;
  emoji: string;
}

interface Props {
  selectedGenres: string[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update-selection', genres: string[]): void;
  (e: 'next'): void;
}>();

const genres: Genre[] = [
  { id: 'action', name: '액션', emoji: '💥' },
  { id: 'comedy', name: '코미디', emoji: '😂' },
  { id: 'romance', name: '로맨스', emoji: '💕' },
  { id: 'thriller', name: '스릴러', emoji: '🔪' },
  { id: 'horror', name: '공포', emoji: '👻' },
  { id: 'sf', name: 'SF', emoji: '🚀' },
  { id: 'fantasy', name: '판타지', emoji: '🧙' },
  { id: 'drama', name: '드라마', emoji: '🎭' },
  { id: 'animation', name: '애니메이션', emoji: '🎨' },
  { id: 'documentary', name: '다큐멘터리', emoji: '📽️' },
  { id: 'crime', name: '범죄', emoji: '🕵️' },
  { id: 'adventure', name: '모험', emoji: '🗺️' },
];

const selectedGenres = ref<string[]>(props.selectedGenres);

const isSelected = (genreId: string) => {
  return selectedGenres.value.includes(genreId);
};

const toggleGenre = (genreId: string) => {
  if (isSelected(genreId)) {
    selectedGenres.value = selectedGenres.value.filter(id => id !== genreId);
  } else {
    selectedGenres.value = [...selectedGenres.value, genreId];
  }
  emit('update-selection', selectedGenres.value);
};

const handleNext = () => {
  emit('next');
};
</script>

<style scoped>
.genre-selection {
  min-height: calc(100vh - 160px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  max-width: 1000px;
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

.genre-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 20px;
  margin-bottom: 48px;
}

.genre-card {
  position: relative;
  background: #18181B;
  border: 2px solid #27272A;
  border-radius: 16px;
  padding: 32px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.genre-card:hover {
  border-color: #8B5CF6;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2);
}

.genre-card.selected {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
  border-color: #8B5CF6;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.3);
}

.genre-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.genre-name {
  font-size: 16px;
  font-weight: 600;
  color: #F8F8F8;
}

.check-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 28px;
  height: 28px;
  background: #8B5CF6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-icon {
  width: 16px;
  height: 16px;
  color: white;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

.btn-next {
  background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%);
  color: white;
  font-weight: bold;
  font-size: 16px;
  padding: 16px 48px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
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

  .genre-grid {
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 12px;
  }

  .genre-card {
    padding: 24px 16px;
  }

  .genre-icon {
    font-size: 36px;
  }

  .genre-name {
    font-size: 14px;
  }
}
</style>