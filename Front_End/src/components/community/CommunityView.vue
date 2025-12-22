<template>
  <div class="community-container bg-gray-900 text-white min-h-screen p-8">
    <div class="header max-w-4xl mx-auto mb-8">
      <h1 class="text-4xl font-bold">🎬 영화 수다방</h1>
      <button @click="goToCreate" class="btn-write bg-pink-500 hover:bg-pink-600 text-white font-bold py-2 px-4 rounded-lg transition-colors">
        글쓰기
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-400">로딩 중...</div>
    <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>

    <div v-else class="post-list max-w-4xl mx-auto space-y-4">
      <div 
        v-for="post in posts" 
        :key="post.id" 
        class="post-item bg-gray-800 p-6 rounded-lg cursor-pointer transition-all hover:bg-gray-700 hover:scale-[1.02]"
        @click="goToDetail(post.id)"
      >
        <!-- TODO: 백엔드 Post 모델에 영화 필드 추가 필요 -->
        <!-- <div class="movie-tag text-sm text-pink-400 mb-2">🍿 {{ post.movieTitle }}</div> -->
        <h3 class="post-title text-xl font-semibold text-white mb-3">{{ post.title }}</h3>
        <div class="post-meta text-xs text-gray-400 flex items-center gap-4">
          <span>작성자: {{ post.author.username }}</span>
          <span>{{ formatDate(post.created_at) }}</span>
          <span>댓글 {{ post.comment_count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

interface Author {
  id: number;
  username: string;
}

interface Post {
  id: number;
  author: Author;
  title: string;
  created_at: string;
  comment_count: number;
}

const router = useRouter();
const posts = ref<Post[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/posts/');
    posts.value = response.data.results || response.data; // 페이지네이션 고려
  } catch (err) {
    console.error('Failed to fetch posts:', err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const goToCreate = () => {
  router.push({ name: 'PostCreate' });
};

const goToDetail = (id: number) => {
  router.push({ name: 'PostDetail', params: { id } });
};
</script>

<style scoped>
.community-container {
  font-family: 'Pretendard', sans-serif;
}
.header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
}
.post-item {
  border-bottom: 1px solid #4a5568; /* gray-700 */
}
.post-item:last-child {
  border-bottom: none;
}
</style>