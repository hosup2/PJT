<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content" role="dialog" aria-modal="true">
        <button class="close-button" @click="handleClose" aria-label="Close modal">
          &times;
        </button>

        <h2 class="modal-title">프로필 편집</h2>
        <p class="modal-subtitle">나만의 프로필을 설정하세요</p>

        <form @submit.prevent="handleSubmit">
          <!-- Profile Image Preview -->
          <div class="profile-image-section">
            <div class="profile-image-wrapper">
              <img
                :src="formData.profile_image"
                alt="프로필 사진"
                class="profile-image"
              />
              <button
                type="button"
                @click="showImageUrlInput = !showImageUrlInput"
                class="edit-image-button"
                aria-label="Edit profile image"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                  <circle cx="12" cy="13" r="4"></circle>
                </svg>
              </button>
            </div>
            
            <div v-if="showImageUrlInput" class="image-url-section">
              <div class="input-group">
                <label for="profile-image-url">프로필 이미지 URL</label>
                <input
                  id="profile-image-url"
                  v-model="formData.profile_image"
                  type="url"
                  placeholder="https://example.com/image.jpg"
                />
              </div>
              <p class="helper-text">
                💡 랜덤 프로필: 
                <button type="button" @click="setRandomProfile" class="random-profile-button">
                  https://i.pravatar.cc/150
                </button>
              </p>
            </div>
          </div>

          <!-- Username -->
          <div class="input-group">
            <label for="username">사용자 이름</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="사용자 이름을 입력하세요"
              required
              maxlength="20"
            />
            <p class="character-count">{{ formData.username.length }}/20</p>
          </div>

          <!-- Email (read-only) -->
          <div class="input-group">
            <label for="email">이메일</label>
            <input
              id="email"
              :value="formData.email"
              type="email"
              disabled
              class="disabled-input"
            />
            <p class="helper-text">이메일은 변경할 수 없습니다</p>
          </div>

          <!-- Action Buttons -->
          <div class="button-group">
            <button type="button" @click="handleClose" class="cancel-button">
              취소
            </button>
            <button type="submit" class="submit-button">
              저장
            </button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

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

const handleClose = () => {
  emit('close');
};

const setRandomProfile = () => {
  const styles = ['avataaars', 'bottts', 'pixel-art', 'lorelei', 'adventurer', 'big-smile', 'fun-emoji'];
  const randomStyle = styles[Math.floor(Math.random() * styles.length)];
  const randomSeed = Math.random().toString(36).substring(7) + Date.now();
  
  formData.value.profile_image = `https://api.dicebear.com/7.x/${randomStyle}/svg?seed=${randomSeed}`;
};
const handleSubmit = () => {
  emit('save', formData.value.username, formData.value.profile_image);
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

/* Profile Image Section */
.profile-image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24px;
}

.profile-image-wrapper {
  position: relative;
  margin-bottom: 16px;
}

.profile-image {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #27272A;
  border: 3px solid #3F3F46;
}

.edit-image-button {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background-color: #7C3AED;
  border: 3px solid #18181B;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
  color: white;
}

.edit-image-button:hover {
  background-color: #6D28D9;
}

.image-url-section {
  width: 100%;
}

/* Input Groups */
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

.disabled-input {
  cursor: not-allowed;
  opacity: 0.6;
}

.character-count {
  margin-top: 4px;
  font-size: 12px;
  color: #71717A;
  text-align: right;
}

.helper-text {
  margin-top: 4px;
  font-size: 12px;
  color: #71717A;
}

.random-profile-button {
  background: none;
  border: none;
  color: #8B5CF6;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
  font-size: 12px;
}

.random-profile-button:hover {
  text-decoration: underline;
}

/* Button Group */
.button-group {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.cancel-button,
.submit-button {
  flex: 1;
  font-weight: bold;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  padding: 14px 0;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.cancel-button {
  background-color: #27272A;
  color: #A1A1AA;
}

.cancel-button:hover {
  background-color: #3F3F46;
}

.submit-button {
  background-color: #7C3AED;
  color: white;
}

.submit-button:hover {
  background-color: #6D28D9;
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