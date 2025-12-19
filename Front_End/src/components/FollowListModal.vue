<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="modal-overlay"
        @click.self="emit('close')"
      >
        <div class="modal-content">
          <div class="flex items-center justify-between p-4 border-b border-gray-700">
            <div class="w-10"></div>
            <h2 class="text-base font-semibold text-white">
              {{ type === 'followers' ? '팔로워' : '팔로잉' }}
            </h2>
            <button
              @click="emit('close')"
              class="p-1 hover:bg-gray-800 rounded-full transition-colors"
            >
              <X class="w-5 h-5 text-gray-400" />
            </button>
          </div>

          <div class="px-4 py-3 border-b border-gray-700">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="검색"
                class="w-full bg-gray-800 rounded-lg px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none"
              />
            </div>
          </div>

          <div v-if="isLoading" class="flex items-center justify-center" style="height: 400px;">
            <div class="text-gray-400">로딩 중...</div>
          </div>

          <div v-else-if="filteredUsers.length === 0" 
            style="height: 400px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; text-align: center;">
        
        <div style="display: flex; flex-direction: column; align-items: center;">
            <Users class="w-12 h-12 text-gray-600 mb-3" style="margin-bottom: 12px;" />
            <p class="text-gray-400 text-sm" style="margin: 0; width: 100%;">
            {{ searchQuery ? '검색 결과가 없습니다' : (type === 'followers' ? '팔로워가 없습니다' : '팔로잉하는 사용자가 없습니다') }}
            </p>
        </div>
        </div>

          <div v-else class="overflow-y-auto" style="height: 400px;">
            <div class="px-4">
              <div
                v-for="user in filteredUsers"
                :key="user.id"
                class="flex items-center justify-between py-2"
              >
                <button
                  @click="handleUserClick(user.id)"
                  class="flex items-center gap-3 flex-1 min-w-0"
                >
                  <img
                    :src="user.profile_image || '/mia5.png'"
                    :alt="user.username"
                    class="w-8 h-8 rounded-full bg-gray-700 object-cover flex-shrink-0"
                    @error="handleImageError"
                  />
                  <div class="text-left min-w-0 flex-1">
                    <p class="font-semibold text-sm text-white truncate hover:text-purple-400 transition-colors">
                      {{ user.username }}
                    </p>
                    <p v-if="user.email" class="text-xs text-gray-500 truncate">
                      {{ user.email }}
                    </p>
                  </div>
                </button>

                <button
                  v-if="user.id !== currentUserId"
                  @click="handleFollowToggle(user.id)"
                  :class="[
                    'px-4 py-1.5 rounded-lg text-sm font-medium transition-colors flex-shrink-0 ml-3',
                    user.is_following
                      ? 'bg-gray-700 text-gray-200 hover:bg-gray-600'
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
import { ref, watch, computed } from 'vue'; // computed 추가
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

// 검색어 상태 및 필터링 로직 추가
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
  searchQuery.value = ''; // 모달이 열릴 때 검색어 초기화
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

// FollowListModal.vue의 handleFollowToggle 함수 확인 및 보강

const handleFollowToggle = async (targetUserId: number) => {
  try {
    // DB 반영 (POST 요청)
    // 만약 JWT 토큰이 필요하다면 axios 설정에 포함되어 있어야 합니다.
    await axios.post(`http://127.0.0.1:8000/users/${targetUserId}/follow/`);
    
    // 로컬 UI 상태 즉시 반영
    const user = users.value.find(u => u.id === targetUserId);
    if (user) {
      user.is_following = !user.is_following;
    }
    
    // (선택사항) 여기서 부모에게 "데이터가 바뀌었음"을 알려줄 수도 있지만, 
    // 보통 모달을 닫을 때 한 번에 갱신하는 것이 효율적입니다.
  } catch (error) {
    console.error('팔로우 요청 실패:', error);
    alert('로그인이 필요하거나 요청을 처리할 수 없습니다.');
  }
};

const handleUserClick = (userId: number) => {
  // 부모 컴포넌트로 이동할 유저 ID 전달
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
  background-color: rgba(0, 0, 0, 0.65) !important;
}

.modal-content {
  position: relative !important;
  z-index: 2147483647 !important;
  background-color: rgb(17, 24, 39) !important;
  border-radius: 0.75rem !important;
  width: 100% !important;
  max-width: 400px !important;
  display: flex !important;
  flex-direction: column !important;
  border: 1px solid rgb(55, 65, 81) !important;
  overflow: hidden !important;
}

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
  transition: transform 0.2s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.95);
}
</style>