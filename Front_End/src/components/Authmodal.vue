<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content" role="dialog" aria-modal="true">
        <button class="close-button" @click="handleClose" aria-label="Close modal">
          &times;
        </button>
        
        <!-- Login Form -->
        <template v-if="mode === 'login'">
          <h2 class="modal-title">로그인</h2>
          <p class="modal-subtitle">MIA에 오신 것을 환영합니다!</p>

          <form @submit.prevent="handleLoginSubmit">
            <div class="input-group">
              <label for="login-email">ID</label>
              <input 
                id="login-username" 
                v-model="loginForm.username" 
                type="text"  
                required 
              />
            </div>

            <div class="input-group">
              <label for="login-password">비밀번호</label>
              <input 
                id="login-password" 
                v-model="loginForm.password" 
                type="password" 
                required 
              />
            </div>

            <button type="submit" class="submit-button">로그인</button>
          </form>

          <div class="switch-mode">
            <p>계정이 없으신가요? <button @click="mode = 'signup'">회원가입</button></p>
          </div>
        </template>

        <!-- Signup Form -->
        <template v-else>
          <h2 class="modal-title">회원가입</h2>
          <p class="modal-subtitle">MIA와 함께 영화 여행을 시작하세요!</p>

          <form @submit.prevent="handleSignupSubmit">
            <div class="input-group">
              <label for="signup-username">사용자명</label>
              <input 
                id="signup-username" 
                v-model="signupForm.username" 
                type="text" 
                placeholder="username" 
                required 
                minlength="3"
              />
            </div>

            <div class="input-group">
              <label for="signup-email">이메일</label>
              <input 
                id="signup-email" 
                v-model="signupForm.email" 
                type="email" 
                placeholder="you@example.com" 
                required 
              />
            </div>

            <div class="input-group">
              <label for="signup-password">비밀번호</label>
              <input 
                id="signup-password" 
                v-model="signupForm.password" 
                type="password" 
                placeholder="••••••••" 
                required 
                minlength="8"
              />
            </div>

            <div class="input-group">
              <label for="signup-password-confirm">비밀번호 확인</label>
              <input 
                id="signup-password-confirm" 
                v-model="signupForm.passwordConfirm" 
                type="password" 
                placeholder="••••••••" 
                required 
                minlength="8"
              />
            </div>

            <button type="submit" class="submit-button">회원가입</button>
          </form>

          <div class="switch-mode">
            <p>이미 계정이 있으신가요? <button @click="mode = 'login'">로그인</button></p>
          </div>
        </template>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface Props {
  isOpen: boolean;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'login', email: string, password: string): void;
  (e: 'signup', payload: {
    username: string;
    email: string;
    password: string;
    password2: string;
  }): void;
}>();


const mode = ref<'login' | 'signup'>('login');

const loginForm = ref({
  username: '',
  password: ''
});

const signupForm = ref({
  username: '',
  email: '',
  password: '',
  passwordConfirm: ''
});

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    // Reset forms when modal opens
    mode.value = 'login';
    loginForm.value = { email: '', password: '' };
    signupForm.value = { username: '', email: '', password: '', passwordConfirm: '' };
  }
});

const handleClose = () => {
  emit('close');
};

const handleLoginSubmit = () => {
  emit('login', loginForm.value.username, loginForm.value.password);
};

const handleSignupSubmit = () => {
  if (signupForm.value.password !== signupForm.value.passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  emit('signup', {
    username: signupForm.value.username,
    email: signupForm.value.email,
    password: signupForm.value.password,
    password2: signupForm.value.passwordConfirm,
  });
};

</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(10, 10, 20, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  background: #18181B;
  color: #F8F8F8;
  padding: 40px;
  border-radius: 16px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  border: 1px solid #27272A;
  max-height: 90vh;
  overflow-y: auto;
}

.close-button {
  position: absolute;
  top: 15px;
  right: 15px;
  background: transparent;
  border: none;
  color: #71717A;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #FFFFFF;
}

.modal-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
  color: #FFFFFF;
}

.modal-subtitle {
  text-align: center;
  color: #A1A1AA;
  margin-bottom: 32px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #A1A1AA;
}

.input-group input {
  width: 100%;
  background-color: #27272A;
  border: 1px solid #3F3F46;
  border-radius: 8px;
  padding: 12px 16px;
  color: #FFFFFF;
  font-size: 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.input-group input::placeholder {
  color: #71717A;
}

.input-group input:focus {
  outline: none;
  border-color: #8B5CF6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
}

.submit-button {
  width: 100%;
  background-color: #7C3AED;
  color: white;
  font-weight: bold;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  padding: 14px 0;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 16px;
}

.submit-button:hover {
  background-color: #6D28D9;
}

.switch-mode {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: #A1A1AA;
}

.switch-mode button {
  background: none;
  border: none;
  color: #8B5CF6;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
}

.switch-mode button:hover {
  text-decoration: underline;
}

/* Transition animation */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.95);
}
</style>