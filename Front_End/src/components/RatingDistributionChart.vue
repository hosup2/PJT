<template>
  <div class="bg-gray-900 rounded-lg p-6">
    <h2 class="text-xl mb-6">
      평점 분포 <span class="text-gray-400">({{ totalCount.toLocaleString() }}명)</span>
    </h2>
    
    <div class="space-y-3">
      <div 
        v-for="rating in ratings" 
        :key="rating.value"
        class="flex items-center gap-4"
      >
        <span class="text-yellow-400 w-24 text-sm">
          {{ rating.label }}
        </span>
        
        <div class="flex-1 bg-gray-800 rounded-full h-6 overflow-hidden">
          <div
            class="bg-gradient-to-r from-yellow-500 to-yellow-400 h-full rounded-full transition-all duration-500"
            :style="{ width: `${getPercentage(rating.count)}%` }"
          />
        </div>
        
        <span class="text-gray-400 w-16 text-right text-sm">
          {{ rating.count.toLocaleString() }}
        </span>
        
        <span class="text-gray-500 w-12 text-right text-sm">
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
