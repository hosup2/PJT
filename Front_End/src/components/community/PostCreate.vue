<template>
  <div class="create-container bg-gray-900 text-white min-h-screen p-8">
    <div class="max-w-3xl mx-auto bg-gray-800 p-8 rounded-lg">
      <h2 class="text-3xl font-bold mb-6">새 글 작성</h2>
      
      <form @submit.prevent="submitPost">
        <div class="form-group mb-6">
          <label for="title" class="block mb-2 text-sm font-medium text-gray-300">제목</label>
          <input id="title" v-model="title" type="text" placeholder="제목을 입력하세요" required 
                 class="w-full bg-gray-700 border border-gray-600 rounded-lg p-2.5 text-white focus:ring-blue-500 focus:border-blue-500" />
        </div>

        <div class="form-group mb-6">
          <label for="content" class="block mb-2 text-sm font-medium text-gray-300">내용</label>
          <textarea id="content" v-model="content" rows="10" placeholder="자유롭게 이야기해주세요" required
                    class="w-full bg-gray-700 border border-gray-600 rounded-lg p-2.5 text-white focus:ring-blue-500 focus:border-blue-500"></textarea>
        </div>
        
        <div v-if="error" class="text-red-400 text-sm mb-4">{{ error }}</div>

        <button type="submit" :disabled="isSubmitting" class="btn-submit w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors disabled:bg-gray-500">
          {{ isSubmitting ? '등록 중...' : '등록하기' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import type { Ref } from 'vue';

const router = useRouter();
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');

const title = ref('');
const content = ref('');
const error = ref<string | null>(null);
const isSubmitting = ref(false);

const submitPost = async () => {
  if (!isLoggedIn?.value) {
    error.value = '글을 작성하려면 로그인이 필요합니다.';
    // Optionally, trigger the login modal
    return;
  }

  if (!title.value.trim() || !content.value.trim()) {
    error.value = '제목과 내용을 모두 입력해주세요.';
    return;
  }

  isSubmitting.value = true;
  error.value = null;

  try {
    const token = localStorage.getItem('access');
    const response = await axios.post('http://127.0.0.1:8000/community/posts/', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    // 성공적으로 생성되면, 해당 게시글 상세 페이지로 이동
    router.push({ name: 'PostDetail', params: { id: response.data.id } });

  } catch (err) {
    console.error('Failed to create post:', err);
    error.value = '게시글 등록에 실패했습니다. 다시 시도해주세요.';
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.create-container {
  font-family: 'Pretendard', sans-serif;
}
</style>