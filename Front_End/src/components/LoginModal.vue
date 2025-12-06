<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content" role="dialog" aria-modal="true">
        <button class="close-button" @click="handleClose" aria-label="Close modal">
          &times;
        </button>
        
        <h2 class="modal-title">로그인</h2>
        <p class="modal-subtitle">MIA에 오신 것을 환영합니다!</p>

        <form @submit.prevent="handleSubmit">
          <div class="input-group">
            <label for="email">이메일</label>
            <input id="email" v-model="email" type="email" placeholder="you@example.com" required />
          </div>

          <div class="input-group">
            <label for="password">비밀번호</label>
            <input id="password" v-model="password" type="password" placeholder="••••••••" required />
          </div>

          <button type="submit" class="submit-button">로그인</button>
        </form>

        <div class="switch-mode">
          <p>계정이 없으신가요? <button @click="handleSwitchMode">회원가입</button></p>
        </div>
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
  (e: 'login', payload: { email: string; password: string }): void;
  (e: 'switch-to-signup'): void;
}>();

const email = ref('');
const password = ref('');

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    // Reset form when modal opens
    email.value = '';
    password.value = '';
  }
});

const handleClose = () => {
  emit('close');
};

const handleSubmit = () => {
  emit('login', { email: email.value, password: password.value });
};

const handleSwitchMode = () => {
  // In a real app, this might emit an event to open a different modal
  alert('회원가입 UI로 전환하는 기능은 아직 구현되지 않았습니다.');
  emit('switch-to-signup');
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
  background: #18181B; /* Darker gray */
  color: #F8F8F8;
  padding: 40px;
  border-radius: 16px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  border: 1px solid #27272A;
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
}

.input-group input::placeholder {
  color: #71717A;
}

.input-group input:focus {
  outline: none;
  border-color: #8B5CF6; /* Purple-500 */
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
}

.submit-button {
  width: 100%;
  background-color: #7C3AED; /* Purple-600 */
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
  background-color: #6D28D9; /* Purple-700 */
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
  color: #8B5CF6; /* Purple-500 */
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
