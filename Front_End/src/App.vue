<template>
  <div class="min-h-screen bg-gray-950 text-white">
    <!-- 온보딩 화면 (회원가입 후 표시) -->
    <PreferenceOnboarding
      v-if="showOnboarding && currentUser"
      :user-id="currentUser.id"
      @complete="handleOnboardingComplete"
      @skip="handleOnboardingSkip"
    />

    <!-- 일반 앱 화면 -->
    <template v-else>
      <Navigation 
        :is-logged-in="isLoggedIn"
        :current-user="currentUser"
        @open-auth="showAuthModal = true"
        @logout="handleLogout"
        @edit-profile="showProfileEditModal = true"
      />

      <div class="animate-float" style="position: fixed; bottom: 32px; right: 32px; z-index: 50;">
        <img src="/mia.png" alt="MIA 로봇" style="height: 100px; width: auto;" class="drop-shadow-2xl cursor-pointer hover:scale-110 transition-transform" />
      </div>

      <main class="relative pt-20"> <!-- Add padding top to account for fixed navigation -->
        <router-view v-slot="{ Component, route }">
          <transition name="fade" mode="out-in">
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </main>

      <!-- 로그인 모달 -->
      <AuthModal
        :is-open="showAuthModal"
        :is-loading="isLoading"
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
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Navigation from './components/Navigation.vue';
import AuthModal from './components/AuthModal.vue';
import ProfileEditModal from './components/ProfileEditModal.vue';
import PreferenceOnboarding from './components/onboarding/PreferenceOnboarding.vue';

interface User {
  id: number;
  username: string;
  email: string;
  profile_image?: string;
  preferences?: {
    genres: string[];
    movies: number[];
  };
}

const router = useRouter();
const isLoggedIn = ref(false);
const currentUser = ref<User | null>(null);
const showAuthModal = ref(false);
const showProfileEditModal = ref(false);
const showOnboarding = ref(false);
const isLoading = ref(false); // 로딩 상태 추가

// Provide user state to all child components
provide('isLoggedIn', isLoggedIn);
provide('currentUser', currentUser);
provide('openAuthModal', () => showAuthModal.value = true);

// ---- Authentication Logic ----
const setAuthTokens = (access: string, refresh: string) => {
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
  axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
};

const clearAuthTokens = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  delete axios.defaults.headers.common['Authorization'];
};

const fetchCurrentUser = async () => {
  try {
    const { data } = await axios.get('http://127.0.0.1:8000/users/me/');
    currentUser.value = data;
    isLoggedIn.value = true;
  } catch (error) {
    console.error('Failed to fetch user', error);
    handleLogout(); // Clear state if user fetch fails
  }
};

// On app startup, check for existing tokens
onMounted(() => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    fetchCurrentUser();
  }
});

const handleLogin = async (username: string, password: string) => {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    const { data } = await axios.post(
      'http://127.0.0.1:8000/api/token/',
      { username, password }
    );

    setAuthTokens(data.access, data.refresh);
    await fetchCurrentUser();
    showAuthModal.value = false;
  } catch {
    alert('로그인에 실패했습니다.');
  } finally {
    isLoading.value = false;
  }
};

interface SignupPayload {
  username: string;
  email: string;
  password: string;
  password2: string;
}

const handleSignup = async (payload: SignupPayload) => {
  if (isLoading.value) return;
  isLoading.value = true;
  try {
    console.log('📦 signup payload:', payload); // 디버깅용

    await axios.post('http://127.0.0.1:8000/users/signup/', payload);

    // 회원가입 직후 로그인 시도
    await handleLogin(payload.username, payload.password);

    showOnboarding.value = true; // 온보딩 시작
    showAuthModal.value = false; // 모달 닫기
  } catch (error: any) {
    console.error('Signup failed', error);
    let errorMsg = '알 수 없는 오류가 발생했습니다.';
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const errorKey = Object.keys(errors)[0];
      if (errorKey && Array.isArray(errors[errorKey]) && errors[errorKey].length > 0) {
        errorMsg = errors[errorKey][0];
      } else {
        errorMsg = JSON.stringify(errors);
      }
    }
    alert(`회원가입에 실패했습니다: ${errorMsg}`);
  } finally {
    isLoading.value = false;
  }
};


const handleLogout = () => {
  clearAuthTokens();
  currentUser.value = null;
  isLoggedIn.value = false;
  showOnboarding.value = false;
  alert('로그아웃되었습니다.');
  if(router.currentRoute.value.path !== '/') {
    router.push('/');
  }
};

// ---- Profile & Onboarding ----

const handleProfileEdit = async (username: string, profileImage: string) => {
  if (currentUser.value) {
    try {
      // NOTE: This assumes your API accepts form-data for file uploads
      // This is a simplified version. A real implementation would use FormData.
      const { data } = await axios.patch(`http://127.0.0.1:8000/users/me/update/`, {
        username: username,
        // profile_image update needs FormData and is more complex. Skipping for now.
      });
      currentUser.value = data; // Update user with response
      alert('프로필이 업데이트되었습니다!');
    } catch(error) {
       console.error('Profile update failed', error);
       alert('프로필 업데이트에 실패했습니다.');
    }
  }
  showProfileEditModal.value = false;
};

const handleOnboardingComplete = async (data: { genres: string[], movies: number[] }) => {
  if (currentUser.value) {
     try {
        await axios.post(`http://127.0.0.1:8000/users/preferences/`, {
            genres: data.genres,
            movie_pks: data.movies
        });
        // Re-fetch user to get updated preferences
        await fetchCurrentUser();
        showOnboarding.value = false;
        alert('선호도가 저장되었습니다! 이제 맞춤 추천을 받아보세요.');
     } catch(error) {
        console.error('Onboarding save failed', error);
        alert('선호도 저장에 실패했습니다.');
     }
  }
};

const handleOnboardingSkip = () => {
  showOnboarding.value = false;
  alert('선호도 설정을 건너뛰었습니다. 나중에 프로필에서 설정할 수 있습니다.');
};

// Watch for route changes to provide global props if needed
watch(() => router.currentRoute.value.path, (newPath) => {
  // This is a good place to add logic that runs on every route change
});

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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>