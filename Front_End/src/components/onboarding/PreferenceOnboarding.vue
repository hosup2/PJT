<template>
  <div class="onboarding-container">
    <!-- Progress Bar -->
    <OnboardingProgress :current-step="currentStep" :total-steps="3" />

    <!-- Step 1: Genre Selection -->
    <transition name="slide-fade" mode="out-in">
      <GenreSelection
        v-if="currentStep === 1"
        :selected-genres="selectedGenres"
        @update-selection="selectedGenres = $event"
        @next="handleGenreNext"
      />

      <!-- Step 2: Movie Selection -->
      <MovieSelection
        v-else-if="currentStep === 2"
        :selected-genres="selectedGenres"
        :selected-movies="selectedMovies"
        @update-selection="selectedMovies = $event"
        @next="handleMovieNext"
        @back="currentStep = 1"
      />

      <!-- Step 3: Complete -->
      <PreferenceComplete
        v-else-if="currentStep === 3"
        :selected-genres="selectedGenres"
        :selected-movies="selectedMovies"
        @complete="handleComplete"
      />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import OnboardingProgress from './OnboardingProgress.vue';
import GenreSelection from './GenreSelection.vue';
import MovieSelection from './MovieSelection.vue';
import PreferenceComplete from './PreferenceComplete.vue';

interface Props {
  userId: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'complete', data: { genres: string[], movies: number[] }): void;
  (e: 'skip'): void;
}>();

const currentStep = ref(1);
const selectedGenres = ref<string[]>([]);
const selectedMovies = ref<number[]>([]);

const handleGenreNext = () => {
  if (selectedGenres.value.length < 3) {
    alert('최소 3개의 장르를 선택해주세요.');
    return;
  }
  currentStep.value = 2;
};

const handleMovieNext = () => {
  if (selectedMovies.value.length < 5) {
    alert('최소 5개의 영화를 선택해주세요.');
    return;
  }
  currentStep.value = 3;
};

const handleComplete = () => {
  emit('complete', {
    genres: selectedGenres.value,
    movies: selectedMovies.value
  });
};
</script>

<style scoped>
.onboarding-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 100%);
  color: #FFFFFF;
  padding: 40px 20px;
}

/* Transition animations */
.slide-fade-enter-active {
  transition: all 0.4s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  transform: translateX(30px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}
</style>