<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="modal-overlay"
        @click.self="emit('close')"
      >
        <div class="modal-content">
          <!-- Header -->
          <div class="flex items-center justify-between p-4 border-b border-gray-800">
            <h2 class="text-xl font-bold">
              {{ type === 'followers' ? '팔로워' : '팔로잉' }}
            </h2>
            <button
              @click="emit('close')"
              class="p-2 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="isLoading" class="flex-1 flex items-center justify-center p-8">
            <div class="text-gray-400">로딩 중...</div>
          </div>

          <!-- Empty State -->
          <div v-else-if="users.length === 0" class="flex-1 flex items-center justify-center p-8">
            <div class="text-center">
              <Users class="w-12 h-12 text-gray-600 mx-auto mb-3" />
              <p class="text-gray-400">
                {{ type === 'followers' ? '팔로워가 없습니다' : '팔로잉하는 사용자가 없습니다' }}
              </p>
            </div>
          </div>

          <!-- User List -->
          <div v-else class="flex-1 overflow-y-auto p-4">
            <div class="space-y-3">
              <div
                v-for="user in users"
                :key="user.id"
                class="flex items-center justify-between p-3 bg-gray-800/50 rounded-lg hover:bg-gray-800 transition-colors"
              >
                <button
                  @click="handleUserClick(user.id)"
                  class="flex items-center gap-3 flex-1 min-w-0"
                >
                  <img
                    :src="user.profile_image || '/mia5.png'"
                    :alt="user.username"
                    class="w-12 h-12 rounded-full bg-gray-700 object-cover flex-shrink-0"
                    @error="handleImageError"
                  />
                  <div class="text-left min-w-0">
                    <p class="font-semibold truncate hover:text-purple-400 transition-colors">
                      {{ user.username }}
                    </p>
                    <p v-if="user.email" class="text-sm text-gray-500 truncate">
                      {{ user.email }}
                    </p>
                  </div>
                </button>

                <!-- Follow/Unfollow Button (자기 자신이 아닐 때만) -->
                <button
                  v-if="user.id !== currentUserId"
                  @click="handleFollowToggle(user.id)"
                  :class="[
                    'px-4 py-1.5 rounded-lg text-sm font-medium transition-colors flex-shrink-0',
                    user.is_following
                      ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      : 'bg-purple-600 text-white hover:bg-purple-700'
                  ]"
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
import { ref, watch } from 'vue';
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

const fetchFollowList = async () => {
  if (!props.isOpen) return;
  
  isLoading.value = true;
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
    
    // Update local state
    const user = users.value.find(u => u.id === targetUserId);
    if (user) {
      user.is_following = !user.is_following;
    }
  } catch (error) {
    console.error('Failed to toggle follow:', error);
    alert('요청을 처리할 수 없습니다.');
  }
};

const handleUserClick = (userId: number) => {
  emit('navigateToUser', userId);
  emit('close');
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
.modal-overlay {
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  z-index: 2147483647 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 1rem !important;
  background-color: rgba(0, 0, 0, 0.8) !important;
}

.modal-content {
  position: relative !important;
  z-index: 2147483647 !important;
  background-color: rgb(17, 24, 39) !important;
  border-radius: 1rem !important;
  width: 100% !important;
  max-width: 28rem !important;
  max-height: 600px !important;
  display: flex !important;
  flex-direction: column !important;
  border: 1px solid rgb(55, 65, 81) !important;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}
</style>