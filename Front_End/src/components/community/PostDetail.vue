<template>
  <div class="detail-container bg-gray-900 text-white min-h-screen p-8">
    <div v-if="loading" class="text-center text-gray-400">게시글을 불러오는 중...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>
    
    <div v-else-if="post" class="max-w-4xl mx-auto">
      <!-- Post Header -->
      <div class="post-header border-b border-gray-700 pb-6 mb-6">
        <h1 class="text-4xl font-bold mb-4">{{ post.title }}</h1>
        <div class="flex justify-between items-center">
          <div class="author-info text-sm text-gray-400">
            <span>작성자: <strong>{{ post.author.username }}</strong></span>
            <span class="mx-2">|</span>
            <span>{{ formatDate(post.created_at) }}</span>
          </div>
          <button 
            v-if="currentUser?.id === post.author.id" 
            @click="deletePost" 
            class="btn-delete bg-red-600 hover:bg-red-700 text-white text-xs font-bold py-1 px-3 rounded-md transition-colors">
            삭제
          </button>
        </div>
      </div>

      <!-- Post Content -->
      <div class="post-content text-gray-300 leading-relaxed min-h-[200px] mb-8 whitespace-pre-wrap">
        {{ post.content }}
      </div>

      <!-- Comments Section -->
      <div class="comments-section mt-12">
        <h3 class="text-xl font-semibold mb-6">댓글 ({{ post.comments.length }})</h3>
        
        <!-- Comment Form -->
        <div class="comment-form mb-8" v-if="isLoggedIn">
          <textarea 
            v-model="newComment" 
            rows="3"
            class="w-full bg-gray-800 border border-gray-600 rounded-lg p-3 text-white focus:ring-blue-500 focus:border-blue-500"
            placeholder="댓글을 입력하세요..."
          ></textarea>
          <button @click="addComment" class="mt-2 w-full md:w-auto float-right bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors">
            댓글 등록
          </button>
        </div>
        
        <!-- Comments List -->
        <ul class="space-y-4">
          <li v-for="comment in post.comments" :key="comment.id" class="comment-item bg-gray-800 p-4 rounded-lg">
            <div class="flex justify-between items-start">
              <div>
                <strong class="text-white">{{ comment.author.username }}</strong>
                <p class="text-gray-400 text-sm mt-2">{{ comment.content }}</p>
              </div>
              <div class="text-xs text-gray-500 text-right flex-shrink-0 ml-4">
                {{ formatDate(comment.created_at) }}
                <button 
                  v-if="currentUser?.id === comment.author.id" 
                  @click="deleteComment(comment.id)" 
                  class="ml-2 text-red-500 hover:underline">
                  삭제
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import type { Ref } from 'vue';

// --- Interfaces ---
interface Author {
  id: number;
  username: string;
}
interface Comment {
  id: number;
  author: Author;
  content: string;
  created_at: string;
}
interface Post {
  id: number;
  author: Author;
  title: string;
  content: string;
  created_at: string;
  comments: Comment[];
}
interface User {
  id: number;
  username: string;
  email: string;
}

// --- Setup ---
const route = useRoute();
const router = useRouter();
const currentUser = inject<Ref<User | null>>('currentUser');
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');

const post = ref<Post | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const newComment = ref('');

const postId = route.params.id;

// --- Data Fetching ---
onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/community/posts/${postId}/`);
    post.value = response.data;
  } catch (err) {
    console.error('Failed to fetch post:', err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});

// --- Methods ---
const addComment = async () => {
  if (!newComment.value.trim() || !post.value) return;

  try {
    const token = localStorage.getItem('access');
    const response = await axios.post(
      `http://127.0.0.1:8000/community/posts/${postId}/comments/`, 
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    post.value.comments.push(response.data);
    newComment.value = '';
  } catch (err) {
    console.error('Failed to add comment:', err);
    alert('댓글 등록에 실패했습니다. 로그인 상태를 확인해주세요.');
  }
};

const deletePost = async () => {
  if (!post.value || !confirm('정말로 이 게시글을 삭제하시겠습니까?')) return;
  try {
    const token = localStorage.getItem('access');
    await axios.delete(`http://127.0.0.1:8000/community/posts/${postId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert('게시글이 삭제되었습니다.');
    router.push({ name: 'Community' });
  } catch (err) {
    console.error('Failed to delete post:', err);
    alert('게시글 삭제에 실패했습니다.');
  }
};

const deleteComment = async (commentId: number) => {
  if (!post.value || !confirm('정말로 이 댓글을 삭제하시겠습니까?')) return;
  try {
    const token = localStorage.getItem('access');
    await axios.delete(`http://127.0.0.1:8000/community/posts/${postId}/comments/${commentId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    post.value.comments = post.value.comments.filter(c => c.id !== commentId);
  } catch (err) {
    console.error('Failed to delete comment:', err);
    alert('댓글 삭제에 실패했습니다.');
  }
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('ko-KR');
};
</script>

<style scoped>
.whitespace-pre-wrap {
  white-space: pre-wrap;
}
</style>