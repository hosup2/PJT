<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <!-- Backdrop -->
    <div 
      class="absolute inset-0 bg-black/80 backdrop-blur-sm"
      @click="emit('close')"
    />
    
    <!-- Modal -->
    <div class="relative bg-gray-900 rounded-lg w-full max-w-md p-8">
      <button
        @click="emit('close')"
        class="absolute top-4 right-4 text-gray-400 hover:text-gray-200"
      >
        <X class="w-6 h-6" />
      </button>

      <h2 class="text-2xl mb-6">프로필 편집</h2>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Profile Image Preview -->
        <div class="flex flex-col items-center">
          <div class="relative mb-4">
            <img
              :src="formData.profile_image"
              alt="프로필 사진"
              class="w-32 h-32 rounded-full object-cover bg-gray-800"
            />
            <button
              type="button"
              @click="showImageUrlInput = !showImageUrlInput"
              class="absolute bottom-0 right-0 w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center hover:bg-purple-700 transition-colors"
            >
              <Camera class="w-5 h-5" />
            </button>
          </div>
          
          <div v-if="showImageUrlInput" class="w-full">
            <label class="block text-sm text-gray-400 mb-2">프로필 이미지 URL</label>
            <input
              v-model="formData.profile_image"
              type="url"
              class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-500 transition-colors mb-2"
              placeholder="https://example.com/image.jpg"
            />
            <p class="text-xs text-gray-500">
              💡 랜덤 프로필: <button type="button" @click="setRandomProfile" class="text-purple-400 hover:text-purple-300">https://i.pravatar.cc/150</button>
            </p>
          </div>
        </div>

        <!-- Username -->
        <div>
          <label class="block text-sm text-gray-400 mb-2">사용자 이름</label>
          <input
            v-model="formData.username"
            type="text"
            required
            maxlength="20"
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="사용자 이름을 입력하세요"
          />
          <p class="text-xs text-gray-500 mt-1">{{ formData.username.length }}/20</p>
        </div>

        <!-- Email (read-only) -->
        <div>
          <label class="block text-sm text-gray-400 mb-2">이메일</label>
          <input
            :value="formData.email"
            type="email"
            disabled
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-gray-500 cursor-not-allowed"
          />
          <p class="text-xs text-gray-500 mt-1">이메일은 변경할 수 없습니다</p>
        </div>

        <div class="flex gap-3">
          <button
            type="button"
            @click="emit('close')"
            class="flex-1 px-4 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
          >
            취소
          </button>
          <button
            type="submit"
            class="flex-1 px-4 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
          >
            저장
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { X, Camera } from 'lucide-vue-next';

interface User {
  username: string;
  email: string;
  profile_image?: string;
}

interface Props {
  isOpen: boolean;
  user: User;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  save: [username: string, profileImage: string];
}>();

const showImageUrlInput = ref(false);
const formData = ref({
  username: '',
  email: '',
  profile_image: ''
});

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    formData.value = {
      username: props.user.username,
      email: props.user.email,
      profile_image: props.user.profile_image || 'https://i.pravatar.cc/150'
    };
    showImageUrlInput.value = false;
  }
});

const setRandomProfile = () => {
  formData.value.profile_image = `https://i.pravatar.cc/150?img=${Math.floor(Math.random() * 70) + 1}`;
};

const handleSubmit = () => {
  emit('save', formData.value.username, formData.value.profile_image);
};
</script>