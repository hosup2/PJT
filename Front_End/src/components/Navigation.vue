<template>
  <nav class="cinema-nav">
    <div class="nav-inner">
      <div class="nav-content">
        
        <router-link 
          :to="{ name: 'Home' }"
          class="nav-logo"
        >
          <img src="/mia_logo1.png" alt="MIA 로고" class="logo-img" />
        </router-link>
        
        <div class="nav-menu">
          
          <router-link
            :to="{ name: 'Home' }"
            class="menu-link"
            active-class="active"
          >
            <Home class="icon-sm" />
            <span>홈</span>
          </router-link>

          <router-link
            :to="{ name: 'Explore' }"
            class="menu-link"
            active-class="active"
          >
            <Film class="icon-sm" />
            <span>둘러보기</span>
          </router-link>
          
          <template v-if="isLoggedIn">
            <router-link
              v-if="currentUser"
              :to="{ name: 'UserProfile', params: { userId: currentUser.id } }"
              class="menu-link"
              active-class="active"
            >
              <User class="icon-sm" />
              <span>내 영화</span>
            </router-link>
            
            <div class="user-menu-wrapper" ref="userMenuRef">
              <button
                @click="showUserMenu = !showUserMenu"
                class="user-btn"
                :class="{ 'active': showUserMenu }"
              >
                <img
                  v-if="currentUser?.profile_image"
                  :src="currentUser.profile_image"
                  :alt="currentUser.username"
                  class="user-avatar"
                />
                <div v-else class="user-avatar-placeholder">
                  {{ currentUser?.username.charAt(0).toUpperCase() }}
                </div>
              </button>
              
              <transition name="fade-slide">
                <div v-if="showUserMenu" class="dropdown-panel">
                  <div class="dropdown-arrow"></div>
                  <button @click="handleProfileEdit" class="dropdown-item">
                    프로필 편집
                  </button>
                  <div class="dropdown-divider"></div>
                  <button @click="handleLogout" class="dropdown-item">
                    로그아웃
                  </button>
                </div>
              </transition>
            </div>
          </template>
          
          <template v-else>
            <button
              @click="emit('openAuth')"
              class="btn-login"
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
  isLoggedIn: boolean;
  currentUser?: User | null;
}

defineProps<Props>();

const emit = defineEmits<{
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

<style scoped>
/* 🎨 MIA Cinema Navbar Style */
.cinema-nav {
  /* 🔥 핵심 수정: Fixed 제거하고 Relative로 변경 */
  position: relative; 
  width: 100%;
  z-index: 50;
  background: #0a0b0f; /* 배경을 불투명한 Pure Black으로 설정 */
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 5rem; /* 64px */
}

/* Logo */
.nav-logo {
  display: flex;
  align-items: center;
  opacity: 1;
  transition: opacity 0.2s;
}

.nav-logo:hover {
  opacity: 0.8;
}

.logo-img {
  height: 4rem;
  filter: drop-shadow(0 2px 6px rgb(66, 27, 156));
}

/* Menu */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Menu Links */
.menu-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 8px; /* 둥근 정도를 조금 줄여서 모던하게 */
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9375rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.menu-link:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}

/* 🔥 Active State: 테두리(Line) 제거, 텍스트 색상과 배경만 은은하게 */
.menu-link.active {
  color: #8b5cf6; /* 텍스트 보라색 */
  background: rgba(139, 92, 246, 0.1); /* 배경 아주 연하게 */
  font-weight: 600;
}

.icon-sm {
  width: 1.125rem;
  height: 1.125rem;
}

/* User Menu */
.user-menu-wrapper {
  position: relative;
  margin-left: 0.5rem;
}

.user-btn {
  display: flex;
  align-items: center;
  padding: 0;
  background: transparent;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.user-btn:hover, .user-btn.active {
  transform: scale(1.05);
}

.user-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: border-color 0.2s;
}

.user-btn:hover .user-avatar {
  border-color: #8b5cf6;
}

.user-avatar-placeholder {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

/* Dropdown Panel */
.dropdown-panel {
  position: absolute;
  top: calc(100% + 0.75rem);
  right: 0;
  width: 160px;
  background: #0a0b0f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8);
  z-index: 100;
  transform-origin: top right;
}

.dropdown-arrow {
  position: absolute;
  top: -6px;
  right: 12px;
  width: 12px;
  height: 12px;
  background: #0a0b0f;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-left: 1px solid rgba(255, 255, 255, 0.1);
  transform: rotate(45deg);
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.625rem 1rem;
  text-align: left;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.dropdown-item:hover {
  background: rgba(139, 92, 246, 0.1);
  color: #c084fc;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0.25rem 0.5rem;
}

/* Login Button */
.btn-login {
  padding: 0.5rem 1.25rem;
  background: transparent;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login:hover {
  background: rgba(139, 92, 246, 0.1);
  border-color: #8b5cf6;
  color: #8b5cf6;
}

/* Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-inner {
    padding: 0 1rem;
  }
  
  .nav-menu {
    gap: 0.5rem;
  }
  
  .menu-link span {
    display: none;
  }
  
  .menu-link {
    padding: 0.5rem;
  }
}
</style>