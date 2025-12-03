<template>
  <nav class="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 max-w-7xl">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center gap-2">
          <Film class="w-8 h-8 text-purple-500" />
          <span class="text-xl">MIA</span>
        </div>
        
        <div class="flex items-center gap-6">
          <button
            @click="emit('navigate', 'home')"
            :class="[
              'flex items-center gap-2 transition-colors',
              currentView === 'home' ? 'text-purple-400' : 'text-gray-400 hover:text-gray-200'
            ]"
          >
            <Home class="w-5 h-5" />
            <span>홈</span>
          </button>
          
          <button
            @click="emit('navigate', 'profile')"
            :class="[
              'flex items-center gap-2 transition-colors',
              currentView === 'profile' ? 'text-purple-400' : 'text-gray-400 hover:text-gray-200'
            ]"
          >
            <User class="w-5 h-5" />
            <span>프로필</span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { Film, User, Home } from 'lucide-vue-next';

interface Props {
  currentView: 'home' | 'movie' | 'profile';
}

defineProps<Props>();

const emit = defineEmits<{
  navigate: [view: 'home' | 'movie' | 'profile'];
}>();
</script>
