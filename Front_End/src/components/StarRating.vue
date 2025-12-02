<template>
  <div class="flex items-center gap-2">
    <div class="flex items-center gap-1">
      <button
        v-for="star in stars"
        :key="star"
        type="button"
        :disabled="readonly"
        @click="handleClick(star)"
        @mouseenter="() => !readonly && (hover = star)"
        @mouseleave="() => !readonly && (hover = 0)"
        :class="[
          readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110',
          'transition-transform'
        ]"
      >
        <Star
          :class="[
            sizeClasses[size],
            isFilled(star) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-600',
            'transition-colors'
          ]"
        />
      </button>
    </div>
    
    <span v-if="currentRating > 0" class="text-gray-400">
      {{ currentRating.toFixed(1) }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Star } from 'lucide-vue-next';

interface Props {
  initialRating?: number;
  readonly?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const props = withDefaults(defineProps<Props>(), {
  initialRating: 0,
  readonly: false,
  size: 'md'
});

const emit = defineEmits<{
  change: [rating: number];
}>();

const currentRating = ref(props.initialRating);
const hover = ref(0);

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8'
};

const stars = [1, 2, 3, 4, 5];

const handleClick = (value: number) => {
  if (props.readonly) return;
  currentRating.value = value;
  emit('change', value);
};

const isFilled = (star: number) => {
  const rating = hover.value || currentRating.value;
  return star <= rating;
};
</script>
