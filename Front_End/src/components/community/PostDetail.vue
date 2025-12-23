<template>
  <div class="detail-container">
    <!-- Loading -->
    <div v-if="loading" class="state-minimal">
      <div class="spinner-minimal-large"></div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-minimal">
      <svg width="48" height="48" fill="currentColor" viewBox="0 0 20 20" style="color: #f5576c; margin-bottom: 1rem;">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
      </svg>
      <p>{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else-if="post" class="detail-content">
      <!-- Back Button -->
      <button @click="goBack" class="btn-back-detail">
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
        </svg>
        <span>목록</span>
      </button>

      <!-- Post Article -->
      <article class="post-article-minimal">
        <!-- Movie Info (if exists) -->
        <div
          v-if="post.movie_title"
          class="movie-info-banner clickable"
          @click="goToMovieDetail"
        >
          <img
            v-if="post.movie_poster"
            :src="`https://image.tmdb.org/t/p/w200${post.movie_poster}`"
            :alt="post.movie_title"
            class="movie-poster-banner"
          />
          <div class="movie-text">
            <span class="movie-label-banner">ABOUT THIS MOVIE</span>
            <h3>{{ post.movie_title }}</h3>
          </div>
        </div>


        <!-- Post Header -->
        <header class="post-header-minimal">
          <h1 class="post-title-minimal">{{ post.title }}</h1>

          <div class="author-bar">
            <div class="author-section-minimal">
              <img
                :src="post.author.profile_image || '/mia5.png'"
                class="avatar-image"
              />
              <div class="author-text">
                <strong>{{ post.author.username }}</strong>
                <div class="meta-text">
                  <span>{{ formatDate(post.created_at) }}</span>
                  <span class="meta-sep">·</span>
                  <span>조회 {{ post.view_count }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <button
              v-if="currentUser?.id === post.author.id"
              @click="deletePost"
              class="btn-delete-minimal"
            >
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              삭제
            </button>
          </div>
        </header>

        <!-- Post Body -->
        <div class="post-body-minimal">
          {{ post.content }}
        </div>
      </article>

      <!-- Comments Section -->
      <section class="comments-section-minimal">
        <h3 class="comments-header">
          댓글 <span class="comment-count-badge">{{ post.comments.length }}</span>
        </h3>

        <!-- Comment Form -->
        <div v-if="isLoggedIn" class="comment-form-minimal">
          <img
            :src="currentUser?.profile_image || '/mia5.png'"
            class="comment-avatar-image"
          />
          <div class="form-textarea-wrapper">
            <textarea
              v-model="newComment"
              rows="4"
              placeholder="댓글을 입력하세요..."
              class="comment-textarea-minimal"
              @keydown.ctrl.enter="addComment"
            ></textarea>
            <div class="form-footer">
              <span class="hint-text">Ctrl+Enter로 빠른 등록</span>
              <button @click="addComment" class="btn-comment-submit">
                등록
              </button>
            </div>
          </div>
        </div>

        <div v-else class="login-notice">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
          </svg>
          <p>댓글을 작성하려면 로그인이 필요합니다</p>
        </div>

        <!-- Comments List -->
        <ul class="comments-list-minimal">
          <li
            v-for="comment in post.comments"
            :key="comment.id"
            class="comment-item-minimal"
          >
            <img
              :src="comment.author.profile_image || '/mia5.png'"
              class="comment-avatar-image"
            />

            <div class="comment-content">
              <div class="comment-header-minimal">
                <strong>{{ comment.author.username }}</strong>
                <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
              </div>
              <p class="comment-body-text">{{ comment.content }}</p>
              <div class="comment-actions-minimal">
                <button
                  v-if="currentUser?.id !== comment.author.id && isLoggedIn"
                  @click="replyToUser(comment.author.username)"
                  class="btn-action-minimal"
                >
                  답글
                </button>
                <button
                  v-if="currentUser?.id === comment.author.id"
                  @click="deleteComment(comment.id)"
                  class="btn-action-minimal btn-action-delete"
                >
                  삭제
                </button>
              </div>
            </div>
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import type { Ref } from 'vue';

interface Author {
  id: number;
  username: string;
  profile_image?: string;
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
  movie_id?: number;
  movie_title?: string;
  movie_poster?: string;
  created_at: string;
  view_count: number;
  comments: Comment[];
}

interface User {
  id: number;
  username: string;
  email: string;
}

const route = useRoute();
const router = useRouter();
const currentUser = inject<Ref<User | null>>('currentUser');
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');

const post = ref<Post | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const newComment = ref('');

const postId = route.params.id;

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

const getAuthToken = (): string | null => {
  const possibleKeys = ['access', 'token', 'accessToken', 'auth_token', 'access_token'];
  
  for (const key of possibleKeys) {
    const token = localStorage.getItem(key);
    if (token) {
      console.log(`Token found with key: ${key}`);
      return token;
    }
  }
  
  console.log('All localStorage keys:', Object.keys(localStorage));
  return null;
};

const addComment = async () => {
  if (!newComment.value.trim() || !post.value) return;

  try {
    const token = getAuthToken();
    
    if (!token) {
      alert('로그인이 필요합니다. 다시 로그인해주세요.');
      router.push('/');
      return;
    }

    const response = await axios.post(
      `http://127.0.0.1:8000/community/posts/${postId}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    post.value.comments.push(response.data);
    newComment.value = '';
  } catch (err: any) {
    console.error('Failed to add comment:', err);
    
    if (err.response?.status === 401 || err.response?.status === 403) {
      alert('로그인이 만료되었습니다. 다시 로그인해주세요.');
      ['access', 'token', 'accessToken', 'refresh'].forEach(key => {
        localStorage.removeItem(key);
      });
      router.push('/');
    } else {
      alert('댓글 등록에 실패했습니다.');
    }
  }
};

const deletePost = async () => {
  if (!post.value || !confirm('정말로 이 게시글을 삭제하시겠습니까?')) return;

  try {
    const token = getAuthToken();
    
    if (!token) {
      alert('로그인이 필요합니다.');
      router.push('/');
      return;
    }

    await axios.delete(`http://127.0.0.1:8000/community/posts/${postId}/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert('게시글이 삭제되었습니다.');
    router.push('/community');
  } catch (err: any) {
    console.error('Failed to delete post:', err);
    
    if (err.response?.status === 401 || err.response?.status === 403) {
      alert('권한이 없거나 로그인이 만료되었습니다.');
      router.push('/');
    } else {
      alert('게시글 삭제에 실패했습니다.');
    }
  }
};

const deleteComment = async (commentId: number) => {
  if (!post.value || !confirm('정말로 이 댓글을 삭제하시겠습니까?')) return;

  try {
    const token = getAuthToken();
    
    if (!token) {
      alert('로그인이 필요합니다.');
      return;
    }

    await axios.delete(
      `http://127.0.0.1:8000/community/posts/${postId}/comments/${commentId}/`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    post.value.comments = post.value.comments.filter(c => c.id !== commentId);
  } catch (err: any) {
    console.error('Failed to delete comment:', err);
    
    if (err.response?.status === 401 || err.response?.status === 403) {
      alert('권한이 없거나 로그인이 만료되었습니다.');
    } else {
      alert('댓글 삭제에 실패했습니다.');
    }
  }
};

const replyToUser = (username: string) => {
  newComment.value = `@${username} `;
  const textarea = document.querySelector('.comment-textarea-minimal') as HTMLTextAreaElement;
  textarea?.focus();
};

const goBack = () => {
  router.back(); // Go back to the previous entry in the history stack
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatRelativeTime = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return '방금';
  if (diffMins < 60) return `${diffMins}분`;
  if (diffHours < 24) return `${diffHours}시간`;
  if (diffDays < 7) return `${diffDays}일`;

  return date.toLocaleDateString('ko-KR', { month: 'numeric', day: 'numeric' });
};

const goToMovieDetail = () => {
  if (!post.value?.movie_id) return;

  router.push({
    name: 'MovieDetail',
    params: { id: post.value.movie_id }
  });
};

</script>

<style scoped>
/* MIA Cinema Style - Pure Black */
.detail-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding: 3rem 0 5rem;
}

/* States */
.state-minimal {
  text-align: center;
  padding: 6rem 2rem;
  color: rgba(255, 255, 255, 0.4);
}

.spinner-minimal-large {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1.5rem;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Content */
.detail-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 3rem;
}

.movie-info-banner.clickable {
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.movie-info-banner.clickable:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}


.btn-back-detail {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.625rem 1rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 2.5rem;
}

.btn-back-detail:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Post Article */
.post-article-minimal {
  margin-bottom: 3rem;
}

.movie-info-banner {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  margin-bottom: 3rem;
}

.movie-poster-banner {
  width: 80px;
  height: 120px;
  border-radius: 4px;
  object-fit: cover;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}

.movie-text {
  flex: 1;
}

.movie-label-banner {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #8b5cf6;
  margin-bottom: 0.5rem;
}

.movie-text h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0;
}

/* Post Header */
.post-header-minimal {
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  margin-bottom: 3rem;
}

.post-title-minimal {
  font-size: 2.5rem;
  font-weight: 400;
  letter-spacing: -0.02em;
  line-height: 1.3;
  color: #ffffff;
  margin: 0 0 2rem 0;
}

.author-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-section-minimal {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar-minimal {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 1rem;
}

.author-text strong {
  display: block;
  font-size: 0.9375rem;
  color: #ffffff;
  margin-bottom: 0.25rem;
}

.meta-text {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.35);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-sep {
  opacity: 0.5;
}

.btn-delete-minimal {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid rgba(245, 87, 108, 0.2);
  color: #f5576c;
  padding: 0.625rem 1rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-delete-minimal:hover {
  background: rgba(245, 87, 108, 0.1);
  border-color: rgba(245, 87, 108, 0.3);
}

/* Post Body */
.post-body-minimal {
  font-size: 1.0625rem;
  line-height: 1.9;
  color: rgba(255, 255, 255, 0.85);
  white-space: pre-wrap;
  word-break: break-word;
  letter-spacing: 0.01em;
}

/* Comments Section */
.comments-section-minimal {
  padding-top: 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.comments-header {
  font-size: 1.125rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 2rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.comment-count-badge {
  background: rgba(139, 92, 246, 0.15);
  color: #8b5cf6;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
}

/* Comment Form */
.comment-form-minimal {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.form-avatar-small {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.form-textarea-wrapper {
  flex: 1;
}

.comment-textarea-minimal {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 0.875rem 1rem;
  color: #ffffff;
  font-size: 0.9375rem;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
  transition: all 0.2s ease;
}

.comment-textarea-minimal:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.comment-textarea-minimal::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.75rem;
}

.hint-text {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.3);
}

.btn-comment-submit {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-comment-submit:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

/* Login Notice */
.login-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 3rem;
}

.login-notice p {
  margin: 0;
  font-size: 0.875rem;
}

/* Comments List */
.comments-list-minimal {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.comment-item-minimal {
  display: flex;
  gap: 1rem;
}

.comment-avatar-small {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header-minimal {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.comment-header-minimal strong {
  font-size: 0.875rem;
  color: #ffffff;
}

.comment-time {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.3);
}

.comment-body-text {
  font-size: 0.9375rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 0.75rem 0;
  word-break: break-word;
}

.comment-actions-minimal {
  display: flex;
  gap: 1rem;
}

.btn-action-minimal {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s ease;
}

.btn-action-minimal:hover {
  color: rgba(255, 255, 255, 0.7);
}

.btn-action-delete:hover {
  color: #f5576c;
}

/* Responsive */
@media (max-width: 768px) {
  .detail-container {
    padding: 2rem 0 4rem;
  }

  .detail-content {
    padding: 0 1.5rem;
  }

  .post-title-minimal {
    font-size: 1.75rem;
  }

  .author-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .movie-info-banner {
    flex-direction: column;
    text-align: center;
  }
}
.avatar-image {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}

.comment-avatar-image {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  object-fit: cover;
}
</style>