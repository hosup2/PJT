<template>
  <nav class="border-b border-gray-800/50 bg-gray-950/95 backdrop-blur-md fixed top-0 z-50 shadow-lg">
    <div class="container mx-auto px-6 max-w-7xl">
      <div class="flex items-center justify-between h-16">
        <!-- 작은 로고 -->
        <button 
          @click="emit('navigate', 'home')"
          class="flex items-center gap-2 hover:opacity-90 transition-all duration-200"
        >
          <!-- <img src="/mia.png" alt="MIA 로봇" style="height: 40px; width: auto;" /> -->
          <img src="/mia_logo1.png" alt="MIA 로고" style="height: 70px; width: auto;" />
        </button>
        
        <!-- 메뉴 -->
        <div class="flex items-center gap-6">
          <button
            @click="emit('navigate', 'home')"
            :class="[
              'flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 font-medium',
              currentView === 'home' 
                ? 'text-white bg-purple-600 shadow-lg shadow-purple-500/30' 
                : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
            ]"
          >
            <Home class="w-5 h-5" />
            <span class="text-base">홈</span>
          </button>

          <button
            class="flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 font-medium text-gray-300 hover:text-white hover:bg-gray-800/50"
          >
            <Film class="w-5 h-5" />
            <span class="text-base">둘러보기</span>
          </button>
          
          <template v-if="isLoggedIn">
            <button
              @click="emit('navigate', 'profile', currentUser?.id)"
              :class="[
                'flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-200 font-medium',
                currentView === 'profile' 
                  ? 'text-white bg-purple-600 shadow-lg shadow-purple-500/30' 
                  : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
              ]"
            >
              <User class="w-5 h-5" />
              <span class="text-base">내 영화</span>
            </button>
            
            <div class="relative">
              <button
                @click="showUserMenu = !showUserMenu"
                class="flex items-center gap-2 px-3 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800/50 transition-all duration-200"
              >
                <img
                  v-if="currentUser?.profile_image"
                  :src="currentUser.profile_image"
                  :alt="currentUser.username"
                  class="w-8 h-8 rounded-full object-cover ring-2 ring-gray-700 hover:ring-purple-500 transition-all"
                />
                <div v-else class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-purple-700 flex items-center justify-center ring-2 ring-gray-700 hover:ring-purple-500 transition-all">
                  <span class="text-xs font-semibold">{{ currentUser?.username.charAt(0).toUpperCase() }}</span>
                </div>
              </button>
              
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl py-2"
              >
                <button
                  @click="handleLogout"
                  class="w-full px-4 py-3 text-left text-gray-300 hover:bg-gray-800 hover:text-white transition-colors font-medium"
                >
                  로그아웃
                </button>
              </div>
            </div>
          </template>
          
          <template v-else>
            <button
              @click="emit('openAuth')"
              class="px-6 py-2.5 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white rounded-lg transition-all duration-200 font-semibold shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 hover:scale-105"
            >
              로그인
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Film, User, Home } from 'lucide-vue-next';

interface User {
  id: number;
  username: string;
  email: string;
  profile_image?: string;
}

interface Props {
  currentView: 'home' | 'movie' | 'profile';
  isLoggedIn: boolean;
  currentUser?: User | null;
}

defineProps<Props>();

const emit = defineEmits<{
  navigate: [view: 'home' | 'movie' | 'profile', userId?: number];
  openAuth: [];
  logout: [];
}>();

const showUserMenu = ref(false);

const handleLogout = () => {
  showUserMenu.value = false;
  emit('logout');
};
</script>