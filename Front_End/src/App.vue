<template>
  <div class="min-h-screen bg-gray-950 text-gray-100">
    <Navigation 
      :current-view="currentView" 
      @navigate="handleNavigate"
    />
    
    <main class="container mx-auto px-4 py-8 max-w-7xl">
      <MovieGrid 
        v-if="currentView === 'home'"
        @movie-click="handleMovieClick" 
      />
      
      <MovieDetail 
        v-if="currentView === 'movie' && selectedMovieId"
        :movie-id="selectedMovieId"
        @back="handleBack"
      />
      
      <UserProfile 
        v-if="currentView === 'profile'"
        :user-id="1" 
      />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Navigation from './components/Navigation.vue';
import MovieGrid from './components/MovieGrid.vue';
import MovieDetail from './components/MovieDetail.vue';
import UserProfile from './components/UserProfile.vue';

type ViewType = 'home' | 'movie' | 'profile';

const currentView = ref<ViewType>('home');
const selectedMovieId = ref<number | null>(null);

const handleNavigate = (view: ViewType) => {
  currentView.value = view;
};

const handleMovieClick = (movieId: number) => {
  selectedMovieId.value = movieId;
  currentView.value = 'movie';
};

const handleBack = () => {
  currentView.value = 'home';
};
</script>
