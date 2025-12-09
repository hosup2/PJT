<template>
  <div class="preference-complete">
    <div class="content-wrapper">
      <div class="success-animation">
        <div class="check-circle-large">
          <svg class="check-icon-large" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>

      <h1 class="title">선호도 분석 완료!</h1>
      <p class="subtitle">당신의 취향을 파악했어요. 이제 맞춤 추천을 받아보세요!</p>

      <div class="summary-section">
        <div class="summary-card">
          <h3 class="summary-title">선택한 장르</h3>
          <div class="genre-tags">
            <span v-for="genre in genreNames" :key="genre" class="genre-tag">
              {{ genre }}
            </span>
          </div>
        </div>

        <div class="summary-card">
          <h3 class="summary-title">선택한 영화</h3>
          <p class="summary-count">총 {{ selectedMovies.length }}개의 영화</p>
        </div>
      </div>

      <div class="action-buttons">
        <button class="btn-complete" @click="handleComplete">
          시작하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  selectedGenres: string[];
  selectedMovies: number[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'complete'): void;
}>();

const genreMap: Record<string, string> = {
  action: '액션',
  comedy: '코미디',
  romance: '로맨스',
  thriller: '스릴러',
  horror: '공포',
  sf: 'SF',
  fantasy: '판타지',
  drama: '드라마',
  animation: '애니메이션',
  documentary: '다큐멘터리',
  crime: '범죄',
  adventure: '모험',
};

const genreNames = computed(() => {
  return props.selectedGenres.map(id => genreMap[id] || id);
});

const handleComplete = () => {
  emit('complete');
};
</script>

<style scoped>
.preference-complete {
  min-height: calc(100vh - 160px);
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
  text-align: center;
}

.success-animation {
  margin-bottom: 32px;
  display: flex;
  justify-content: center;
}

.check-circle-large {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.check-icon-large {
  width: 64px;
  height: 64px;
  color: white;
  stroke-width: 3;
}

.title {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 12px;
  background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: #A1A1AA;
  font-size: 16px;
  margin-bottom: 48px;
  line-height: 1.6;
}

.summary-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 48px;
}

.summary-card {
  background: #18181B;
  border: 1px solid #27272A;
  border-radius: 16px;
  padding: 24px;
  text-align: left;
}

.summary-title {
  font-size: 18px;
  font-weight: 600;
  color: #F8F8F8;
  margin-bottom: 16px;
}

.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.genre-tag {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.2) 100%);
  border: 1px solid #8B5CF6;
  color: #C4B5FD;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.summary-count {
  color: #A1A1AA;
  font-size: 16px;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

.btn-complete {
  background: linear-gradient(90deg, #8B5CF6 0%, #7C3AED 100%);
  color: white;
  font-weight: bold;
  font-size: 18px;
  padding: 18px 64px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-complete:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(139, 92, 246, 0.5);
}

@media (max-width: 768px) {
  .title {
    font-size: 28px;
  }

  .check-circle-large {
    width: 100px;
    height: 100px;
  }

  .check-icon-large {
    width: 52px;
    height: 52px;
  }

  .btn-complete {
    padding: 16px 48px;
    font-size: 16px;
  }
}
</style>