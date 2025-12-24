<template>
  <!-- 🔥 아웃라인만 있는 와이어프레임 스타일 -->
  <div class="chart-wrapper">
    <h2 class="chart-title">
      평점 분포 <span class="count-text">({{ totalCount.toLocaleString() }}명)</span>
    </h2>
    
    <div class="ratings-container">
      <div 
        v-for="rating in ratings" 
        :key="rating.value"
        class="rating-row"
      >
        <span class="star-label">
          {{ rating.label }}
        </span>
        
        <!-- 🔥 와이어프레임 프로그레스 바 -->
        <div class="progress-container">
          <div
            class="progress-fill"
            :style="{ width: `${getPercentage(rating.count)}%` }"
          />
        </div>
        
        <span class="count-text">
          {{ rating.count.toLocaleString() }}
        </span>
        
        <span class="percent-text">
          {{ getPercentage(rating.count).toFixed(0) }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  movieId: number;
  distribution: Record<string, number>;
  totalCount: number;
}

const props = defineProps<Props>();

const ratings = computed(() => [
  { value: '5.0', label: '★★★★★', count: props.distribution['5.0'] || 0 },
  { value: '4.0', label: '★★★★', count: props.distribution['4.0'] || 0 },
  { value: '3.0', label: '★★★', count: props.distribution['3.0'] || 0 },
  { value: '2.0', label: '★★', count: props.distribution['2.0'] || 0 },
  { value: '1.0', label: '★', count: props.distribution['1.0'] || 0 },
]);

const getPercentage = (count: number) => {
  return props.totalCount > 0 ? (count / props.totalCount) * 100 : 0;
};
</script>

<style scoped>
/* 🔥 와이어프레임 컨테이너 */
.chart-wrapper {
  background: transparent;
  border: 2px solid rgba(139, 92, 246, 0.12);
  border-radius: 12px;
  padding: 1.5rem;
  transition: border-color 0.3s ease;
}

.chart-wrapper:hover {
  border-color: rgba(139, 92, 246, 0.25);
}

/* 제목 */
.chart-title {
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: white;
  font-weight: 600;
}

/* 평점 컨테이너 */
.ratings-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* 평점 행 */
.rating-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 별 라벨 */
.star-label {
  color: #fbbf24;
  width: 6rem;
  font-size: 0.875rem;
  flex-shrink: 0;
}

/* 🔥 와이어프레임 프로그레스 바 컨테이너 */
.progress-container {
  flex: 1;
  height: 1.5rem;
  background: transparent;
  border: 2px solid rgba(139, 92, 246, 0.12);
  border-radius: 100px;
  overflow: hidden;
  position: relative;
}

/* 🔥 프로그레스 바 채우기 */
.progress-fill {
  height: 100%;
    /* 원래의 노란색 그라데이션 복구 */
    background: linear-gradient(
      90deg,
      rgba(251, 191, 36, 1) 0%,    /* 시작: 진한 금색 */
      rgba(255, 249, 63, 1) 100%   /* 끝: 밝은 노란색 */
    );
    border-radius: 100px;
    transition: width 0.5s ease;
    /* 노란색 빛 번짐 효과 */
    box-shadow: 0 0 10px rgba(251, 191, 36, 0.5);
}

/* 개수 텍스트 */
.count-text {
  color: rgba(255, 255, 255, 0.4);
  width: 4rem;
  text-align: right;
  font-size: 0.875rem;
  flex-shrink: 0;
}

/* 퍼센트 텍스트 */
.percent-text {
  color: rgba(255, 255, 255, 0.3);
  width: 3rem;
  text-align: right;
  font-size: 0.875rem;
  flex-shrink: 0;
}
</style>