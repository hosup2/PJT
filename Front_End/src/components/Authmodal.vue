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

      <h2 class="text-2xl mb-6">{{ mode === 'login' ? '로그인' : '회원가입' }}</h2>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div v-if="mode === 'signup'">
          <label class="block text-sm text-gray-400 mb-2">사용자 이름</label>
          <input
            v-model="formData.username"
            type="text"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="사용자 이름을 입력하세요"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400 mb-2">이메일</label>
          <input
            v-model="formData.email"
            type="email"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="이메일을 입력하세요"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-400 mb-2">비밀번호</label>
          <input
            v-model="formData.password"
            type="password"
            required
            class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="비밀번호를 입력하세요"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-purple-600 hover:bg-purple-700 text-white py-3 rounded-lg transition-colors"
        >
          {{ mode === 'login' ? '로그인' : '회원가입' }}
        </button>
      </form>

      <div class="mt-6 text-center">
        <button
          @click="toggleMode"
          class="text-sm text-gray-400 hover:text-gray-200"
        >
          {{ mode === 'login' ? '계정이 없으신가요? 회원가입' : '이미 계정이 있으신가요? 로그인' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { X } from 'lucide-vue-next';

interface Props {
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  close: [];
  login: [email: string, password: string];
  signup: [username: string, email: string, password: string];
}>();

const mode = ref<'login' | 'signup'>('login');
const formData = ref({
  username: '',
  email: '',
  password: ''
});

watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    formData.value = {
      username: '',
      email: '',
      password: ''
    };
  }
});

const toggleMode = () => {
  mode.value = mode.value === 'login' ? 'signup' : 'login';
  formData.value = {
    username: '',
    email: '',
    password: ''
  };
};

const handleSubmit = () => {
  if (mode.value === 'login') {
    emit('login', formData.value.email, formData.value.password);
  } else {
    emit('signup', formData.value.username, formData.value.email, formData.value.password);
  }
};
</script>