<template>
  <div class="min-h-screen bg-gray-950 text-white">
    <!-- Navigation을 맨 위에 fixed로 겹치기 -->
    <Navigation 
      :current-view="currentView"
      :is-logged-in="isLoggedIn"
      :current-user="currentUser"
      @navigate="handleNavigate"
      @open-auth="showAuthModal = true"
      @logout="handleLogout"
      @edit-profile="showProfileEditModal = true"
    />

    <div class="animate-float" style="position: fixed; bottom: 32px; right: 32px; z-index: 50;">
      <img src="/mia.png" alt="MIA 로봇" style="height: 100px; width: auto;" class="drop-shadow-2xl cursor-pointer hover:scale-110 transition-transform" />
    </div>

    <!-- main을 padding 없이 시작 -->
    <main class="relative">
      <!-- 홈 화면 -->
      <template v-if="currentView === 'home'">
        <!-- HeroSection을 화면 맨 위에서 시작 -->
        <HeroSection />
        
        <!-- 인기 영화 -->
        <div class="container mx-auto px-6 py-12 max-w-7xl">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-3xl font-bold">인기 영화</h2>
            <button class="text-purple-400 hover:text-purple-300 text-sm font-medium flex items-center gap-1">
              전체보기
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
          
          <MovieGrid 
            :movies="mockMovies"
            @movie-click="handleMovieClick"
          />
        </div>
      </template>

      <!-- 영화 상세 -->
      <MovieDetail 
        v-if="currentView === 'movie' && selectedMovieId"
        :movie-id="selectedMovieId"
        :current-user="currentUser"
        :is-logged-in="isLoggedIn"
        @back="currentView = 'home'"
        @profile-click="handleNavigate"
        @open-auth="showAuthModal = true"
        @navigate-to-user="handleNavigateToUser"
      />

      <!-- 프로필 -->
      <UserProfile 
        v-if="currentView === 'profile' && selectedUserId"
        :user-id="selectedUserId"
        :current-user-id="currentUser?.id"
        @movie-click="handleMovieClick"
        @go-home="currentView = 'home'"
        @update-profile="handleUpdateProfile"
      />
    </main>

    <!-- 로그인 모달 -->
    <AuthModal
      :is-open="showAuthModal"
      @close="showAuthModal = false"
      @login="handleLogin"
      @signup="handleSignup"
    />

    <!-- 프로필 편집 모달 -->
    <ProfileEditModal
      :is-open="showProfileEditModal"
      :user="currentUser || { username: '', email: '', profile_image: '' }"
      @close="showProfileEditModal = false"
      @save="handleProfileEdit"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Navigation from './components/Navigation.vue';
import HeroSection from './components/HeroSection.vue';
import MovieGrid from './components/MovieGrid.vue';
import MovieDetail from './components/MovieDetail.vue';
import UserProfile from './components/UserProfile.vue';
import AuthModal from './components/AuthModal.vue';
import ProfileEditModal from './components/ProfileEditModal.vue';
import { mockMovies, mockUsers } from './data/mockData';

interface User {
  id: number;
  username: string;
  email: string;
  profile_image?: string;
}

const currentView = ref<'home' | 'movie' | 'profile'>('home');
const selectedMovieId = ref<number | null>(null);
const selectedUserId = ref<number | null>(null);
const isLoggedIn = ref(false);
const currentUser = ref<User | null>(null);
const showAuthModal = ref(false);
const showProfileEditModal = ref(false);

const handleMovieClick = (movieId: number) => {
  selectedMovieId.value = movieId;
  currentView.value = 'movie';
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const handleNavigate = (view: 'home' | 'movie' | 'profile', userId?: number) => {
  currentView.value = view;
  selectedUserId.value = userId || currentUser.value?.id || null;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const handleLogin = (email: string, password: string) => {
  const user = mockUsers.find(u => u.email === email);
  if (user) {
    currentUser.value = user;
    isLoggedIn.value = true;
    showAuthModal.value = false;
    alert('로그인 성공!');
  } else {
    alert('사용자를 찾을 수 없습니다.');
  }
};

const handleSignup = (username: string, email: string, password: string) => {
  const newUser: User = {
    id: mockUsers.length + 1,
    username,
    email,
    profile_image: '/mia2.png'  // 👈 기본 프로필 이미지를 mia2.png로 설정
  };
  
  mockUsers.push(newUser);
  
  currentUser.value = newUser;
  isLoggedIn.value = true;
  showAuthModal.value = false;
  alert('회원가입 성공!');
};

const handleLogout = () => {
  currentUser.value = null;
  isLoggedIn.value = false;
  currentView.value = 'home';
  alert('로그아웃되었습니다.');
};

const handleNavigateToUser = (userId: number) => {
  selectedUserId.value = userId; 
  currentView.value = 'profile';
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const handleUpdateProfile = (username: string, profileImage: string) => {
  if (currentUser.value) {
    currentUser.value.username = username;
    currentUser.value.profile_image = profileImage;
    
    const userInArray = mockUsers.find(u => u.id === currentUser.value?.id);
    if (userInArray) {
      userInArray.username = username;
      userInArray.profile_image = profileImage;
    }
    
    alert('프로필이 업데이트되었습니다!');
  }
};

const handleProfileEdit = (username: string, profileImage: string) => {
  if (currentUser.value) {
    currentUser.value.username = username;
    currentUser.value.profile_image = profileImage;
    
    const userInArray = mockUsers.find(u => u.id === currentUser.value?.id);
    if (userInArray) {
      userInArray.username = username;
      userInArray.profile_image = profileImage;
    }
    
    alert('프로필이 업데이트되었습니다!');
  }
  showProfileEditModal.value = false;
};
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>