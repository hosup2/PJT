<template>
  <nav class="border-b border-gray-800/30 bg-gray-950/70 backdrop-blur-md fixed top-0 w-full z-50 shadow-lg">
    <div class="container mx-auto px-6 max-w-7xl">
      <div class="flex items-center justify-between h-20">
        <!-- 작은 로고 -->
        <button 
          @click="emit('navigate', 'home')"
          class="flex items-center gap-2 hover:opacity-90 transition-all duration-200"
        >
          <img src="/mia_logo1.png" alt="MIA 로고" style="height: 80px; width: auto; margin-left: 30px" />
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
            
            <div class="relative" ref="userMenuRef">
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
              
              <!-- 말풍선 스타일 드롭다운 -->
              <div
                v-if="showUserMenu"
                style="position: absolute; left: calc(100% + 8px); top: 0; width: 140px; background-color: #111827; border: 1px solid rgba(147, 51, 234, 0.3); border-radius: 12px; box-shadow: 0 20px 25px -5px rgba(147, 51, 234, 0.3), 0 8px 10px -6px rgba(147, 51, 234, 0.3); padding: 4px; z-index: 9999;"
              >
                <!-- 왼쪽 말풍선 화살표 -->
                <div style="position: absolute; left: -8px; top: 12px; width: 16px; height: 16px; background-color: #111827; border-left: 1px solid rgba(147, 51, 234, 0.3); border-bottom: 1px solid rgba(147, 51, 234, 0.3); transform: rotate(45deg);"></div>
                
                <!-- 프로필 편집 버튼 -->
                <button
                  @click="handleProfileEdit"
                  style="width: 100%; padding: 8px 12px; text-align: center; color: #d1d5db; font-weight: 500; font-size: 0.875rem; border-radius: 8px; border: none; background: transparent; cursor: pointer; transition: all 0.2s; margin-bottom: 2px;"
                  @mouseover="$event.target.style.backgroundColor = '#9333ea'; $event.target.style.color = '#ffffff'"
                  @mouseout="$event.target.style.backgroundColor = 'transparent'; $event.target.style.color = '#d1d5db'"
                >
                  프로필 편집
                </button>

                <!-- 구분선 -->
                <div style="height: 1px; background-color: rgba(147, 51, 234, 0.2); margin: 4px 8px;"></div>
                
                <!-- 로그아웃 버튼 -->
                <button
                  @click="handleLogout"
                  style="width: 100%; padding: 8px 12px; text-align: center; color: #d1d5db; font-weight: 500; font-size: 0.875rem; border-radius: 8px; border: none; background: transparent; cursor: pointer; transition: all 0.2s; margin-top: 2px;"
                  @mouseover="$event.target.style.backgroundColor = '#9333ea'; $event.target.style.color = '#ffffff'"
                  @mouseout="$event.target.style.backgroundColor = 'transparent'; $event.target.style.color = '#d1d5db'"
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
import { ref, onMounted, onUnmounted } from 'vue';
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
  editProfile: [];
}>();

const showUserMenu = ref(false);
const userMenuRef = ref<HTMLElement | null>(null);

const handleLogout = () => {
  showUserMenu.value = false;
  emit('logout');
};

const handleProfileEdit = () => {
  showUserMenu.value = false;
  emit('editProfile');
};

// 외부 클릭 감지
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    showUserMenu.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>