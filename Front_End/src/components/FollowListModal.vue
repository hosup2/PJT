네, **MIA Cinema (Pure Black)** 디자인 시스템을 `FollowListModal`에도 적용했습니다.

기존의 **기능(검색, 팔로우 토글, 유저 클릭, 로딩 상태)**은 100% 유지하면서, Tailwind CSS 클래스 대신 **커스텀 CSS(Scoped Style)**를 사용하여 전체적인 디자인 통일감을 높였습니다.

```vue
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="modal-overlay"
        @click.self="emit('close')"
      >
        <div class="modal-content">
          <div class="modal-header">
            <div class="header-spacer"></div>
            <h2 class="modal-title">
              {{ type === 'followers' ? '팔로워' : '팔로잉' }}
            </h2>
            <button @click="emit('close')" class="btn-close">
              <X class="icon-sm" />
            </button>
          </div>

          <div class="search-container">
            <div class="search-box">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="검색"
                class="search-input"
              />
            </div>
          </div>

          <div class="list-container">
            
            <div v-if="isLoading" class="state-container">
              <div class="spinner-minimal"></div>
            </div>

            <div v-else-if="filteredUsers.length === 0" class="state-container">
              <Users class="icon-lg text-muted" />
              <p class="empty-text">
                {{ searchQuery ? '검색 결과가 없습니다' : (type === 'followers' ? '팔로워가 없습니다' : '팔로잉하는 사용자가 없습니다') }}
              </p>
            </div>

            <div v-else class="user-list">
              <div
                v-for="user in filteredUsers"
                :key="user.id"
                class="user-item"
              >
                <button
                  @click="handleUserClick(user.id)"
                  class="user-info-btn"
                >
                  <img
                    :src="user.profile_image || '/mia5.png'"
                    :alt="user.username"
                    class="user-avatar"
                    @error="handleImageError"
                  />
                  <div class="text-wrapper">
                    <p class="username">{{ user.username }}</p>
                    <p v-if="user.email" class="email">{{ user.email }}</p>
                  </div>
                </button>

                <button
                  v-if="user.id !== currentUserId"
                  @click="handleFollowToggle(user.id)"
                  :class="['btn-follow', { following: user.is_following }]"
                >
                  {{ user.is_following ? '팔로잉' : '팔로우' }}
                </button>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import { X, Users } from 'lucide-vue-next';
import axios from 'axios';

interface User {
  id: number;
  username: string;
  email?: string;
  profile_image?: string;
  is_following: boolean;
}

interface Props {
  isOpen: boolean;
  userId: number;
  type: 'followers' | 'following';
  currentUserId?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  navigateToUser: [userId: number];
}>();

const users = ref<User[]>([]);
const isLoading = ref(false);
const searchQuery = ref('');

const filteredUsers = computed(() => {
  const query = searchQuery.value.trim().toLowerCase();
  if (!query) return users.value;
  
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) || 
    user.email?.toLowerCase().includes(query)
  );
});

const fetchFollowList = async () => {
  if (!props.isOpen) return;
  
  isLoading.value = true;
  searchQuery.value = ''; 
  try {
    const endpoint = props.type === 'followers' 
      ? `http://127.0.0.1:8000/users/${props.userId}/followers/`
      : `http://127.0.0.1:8000/users/${props.userId}/following/`;
    
    const response = await axios.get(endpoint);
    users.value = response.data;
  } catch (error) {
    console.error('Failed to fetch follow list:', error);
    users.value = [];
  } finally {
    isLoading.value = false;
  }
};

const handleFollowToggle = async (targetUserId: number) => {
  try {
    await axios.post(`http://127.0.0.1:8000/users/${targetUserId}/follow/`);
    const user = users.value.find(u => u.id === targetUserId);
    if (user) {
      user.is_following = !user.is_following;
    }
  } catch (error) {
    console.error('팔로우 요청 실패:', error);
    alert('로그인이 필요하거나 요청을 처리할 수 없습니다.');
  }
};

const handleUserClick = (userId: number) => {
  emit('navigateToUser', userId);
};

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/mia5.png';
};

watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    fetchFollowList();
  }
});
</script>

<style scoped>
/* 🎨 MIA Cinema Modal Style */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}

.modal-content {
  position: relative;
  width: 100%;
  max-width: 400px;
  background-color: #0a0b0f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Header */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.02);
}

.header-spacer { width: 24px; }

.modal-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.btn-close {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Search */
.search-container {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.search-box {
  position: relative;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.625rem 1rem;
  color: white;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #8b5cf6;
  background: rgba(255, 255, 255, 0.08);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

/* List Container */
.list-container {
  height: 400px;
  overflow-y: auto;
  position: relative;
}

/* Scrollbar Customization */
.list-container::-webkit-scrollbar {
  width: 4px;
}
.list-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

/* State (Loading / Empty) */
.state-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.4);
}

.spinner-minimal {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.icon-lg {
  width: 3rem;
  height: 3rem;
  margin-bottom: 0.75rem;
  opacity: 0.3;
}

.empty-text {
  font-size: 0.875rem;
  margin: 0;
}

/* User List Items */
.user-list {
  padding: 0.5rem 0;
}

.user-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  transition: background 0.2s;
}

.user-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.user-info-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
  background: transparent;
  border: none;
  padding: 0;
  cursor: pointer;
  text-align: left;
}

.user-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
  background: rgba(255, 255, 255, 0.1);
  flex-shrink: 0;
}

.text-wrapper {
  min-width: 0;
}

.username {
  font-size: 0.9375rem;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.125rem;
  transition: color 0.2s;
}

.user-info-btn:hover .username {
  color: #8b5cf6;
}

.email {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Follow Button */
.btn-follow {
  padding: 0.375rem 1rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  flex-shrink: 0;
  margin-left: 0.75rem;
  background: #8b5cf6;
  color: white;
}

.btn-follow:hover {
  background: #7c3aed;
}

.btn-follow.following {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.btn-follow.following:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #f87171; /* Hover to unfollow hint color? Optional */
}

/* Transition Animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95) translateY(10px);
}

.icon-sm { width: 1.25rem; height: 1.25rem; }
.text-muted { color: rgba(255, 255, 255, 0.3); }
</style>

```