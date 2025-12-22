<template>
  <div class="create-container">
    <!-- Minimal Header -->
    <header class="create-header">
      <button @click="goBack" class="btn-back-minimal">
        <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="header-text">
        <span class="page-label">CREATE POST</span>
        <h1 class="page-title">새 이야기</h1>
      </div>
    </header>

    <div class="create-content">
      <form @submit.prevent="submitPost" class="create-form">
        <!-- Movie Selection -->
        <div class="form-group">
          <label class="form-label">영화 선택</label>
          <p class="form-description">이 글과 관련된 영화가 있다면 선택해주세요</p>

          <!-- Selected Movie -->
          <div v-if="selectedMovie" class="selected-movie-card">
            <img
              :src="`https://image.tmdb.org/t/p/w185${selectedMovie.poster_path}`"
              :alt="selectedMovie.title"
              class="selected-poster"
            />
            <div class="selected-info">
              <h4>{{ selectedMovie.title }}</h4>
              <p>{{ selectedMovie.release_date?.substring(0, 4) }}</p>
            </div>
            <button type="button" @click="clearMovie" class="btn-clear-minimal">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Movie Search -->
          <div v-else class="search-section">
            <div class="search-input-container">
              <input
                v-model="movieSearchQuery"
                @input="searchMovies"
                type="text"
                placeholder="영화 제목 검색..."
                class="search-input-minimal"
              />
              <svg class="search-icon-minimal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </div>

            <!-- Searching -->
            <div v-if="movieSearching" class="searching-state">
              <div class="spinner-small"></div>
              <span>검색 중...</span>
            </div>

            <!-- Results -->
            <div v-if="movieSearchResults.length > 0" class="search-results-minimal">
              <div
                v-for="movie in movieSearchResults"
                :key="movie.id"
                @click="selectMovie(movie)"
                class="result-item-minimal"
              >
                <img
                  v-if="movie.poster_path"
                  :src="`https://image.tmdb.org/t/p/w92${movie.poster_path}`"
                  :alt="movie.title"
                  class="result-poster-mini"
                />
                <div v-else class="result-placeholder-mini">🎬</div>
                <div class="result-details">
                  <h5>{{ movie.title }}</h5>
                  <p>{{ movie.release_date?.substring(0, 4) || '—' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Title -->
        <div class="form-group">
          <label for="title" class="form-label">제목</label>
          <input
            id="title"
            v-model="title"
            type="text"
            placeholder="제목을 입력하세요"
            required
            class="input-minimal"
          />
        </div>

        <!-- Content -->
        <div class="form-group">
          <label for="content" class="form-label">내용</label>
          <textarea
            id="content"
            v-model="content"
            rows="16"
            placeholder="자유롭게 이야기해주세요..."
            required
            class="textarea-minimal"
          ></textarea>
          <div class="char-counter">{{ content.length }} / 1,000</div>
        </div>

        <!-- Error -->
        <div v-if="error" class="error-minimal">
          <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
          </svg>
          {{ error }}
        </div>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="btn-submit-minimal"
        >
          <span v-if="isSubmitting">등록 중...</span>
          <span v-else>게시하기</span>
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

interface Movie {
  id: number;
  title: string;
  poster_path: string | null;
  release_date: string;
}

const router = useRouter();
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');

const title = ref('');
const content = ref('');
const error = ref<string | null>(null);
const isSubmitting = ref(false);

const selectedMovie = ref<Movie | null>(null);
const movieSearchQuery = ref('');
const movieSearchResults = ref<Movie[]>([]);
const movieSearching = ref(false);
let searchTimeout: number | null = null;

const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY || '';
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

const searchMovies = () => {
  if (searchTimeout) clearTimeout(searchTimeout);

  if (!movieSearchQuery.value.trim()) {
    movieSearchResults.value = [];
    return;
  }

  if (!TMDB_API_KEY || TMDB_API_KEY === 'YOUR_TMDB_API_KEY') {
    console.warn('TMDb API key is not configured');
    return;
  }

  movieSearching.value = true;
  searchTimeout = window.setTimeout(async () => {
    try {
      const response = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
        params: {
          api_key: TMDB_API_KEY,
          query: movieSearchQuery.value,
          language: 'ko-KR'
        }
      });
      movieSearchResults.value = response.data.results.slice(0, 5);
    } catch (err) {
      console.error('Failed to search movies:', err);
    } finally {
      movieSearching.value = false;
    }
  }, 300);
};

const selectMovie = (movie: Movie) => {
  selectedMovie.value = movie;
  movieSearchQuery.value = '';
  movieSearchResults.value = [];
};

const clearMovie = () => {
  selectedMovie.value = null;
};

const goBack = () => {
  router.back();
};

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

const submitPost = async () => {
  if (!isLoggedIn?.value) {
    error.value = '글을 작성하려면 로그인이 필요합니다.';
    alert('로그인이 필요합니다.');
    router.push('/');
    return;
  }

  if (!title.value.trim() || !content.value.trim()) {
    error.value = '제목과 내용을 모두 입력해주세요.';
    return;
  }

  if (content.value.length > 1000) {
    error.value = '내용은 1000자를 초과할 수 없습니다.';
    return;
  }

  isSubmitting.value = true;
  error.value = null;

  try {
    const token = getAuthToken();

    if (!token) {
      console.error('No auth token found in localStorage');
      throw new Error('로그인 정보를 찾을 수 없습니다. 다시 로그인해주세요.');
    }

    const postData: any = {
      title: title.value,
      content: content.value
    };

    if (selectedMovie.value) {
      postData.movie_id = selectedMovie.value.id;
      postData.movie_title = selectedMovie.value.title;
      postData.movie_poster = selectedMovie.value.poster_path;
    }

    console.log('Submitting post with token:', token.substring(0, 20) + '...');

    const response = await axios.post(
      'http://127.0.0.1:8000/community/posts/',
      postData,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('✅ Post created successfully:', response.data);

    if (response.data?.id) {
      const postId = String(response.data.id);
      console.log(`Redirecting to post detail: ${postId}`);

      try {
        await router.push(`/community/${postId}`);
      } catch (routerError) {
        console.error('Router push failed:', routerError);
        await router.push('/community');
      }
    } else {
      console.warn('No post ID in response, redirecting to community list');
      await router.push('/community');
    }

  } catch (err: any) {
    console.error('Failed to create post:', err);
    console.error('Error response:', err.response?.data);

    if (err.response?.status === 401) {
      error.value = '로그인이 만료되었습니다. 다시 로그인해주세요.';

      ['access', 'token', 'accessToken', 'refresh'].forEach(key => {
        localStorage.removeItem(key);
      });

      alert('로그인이 만료되었습니다. 다시 로그인해주세요.');
      router.push('/');

    } else if (err.response?.status === 400) {
      const errorData = err.response.data;
      if (typeof errorData === 'object') {
        const firstError = Object.values(errorData)[0];
        error.value = Array.isArray(firstError) ? firstError[0] : String(firstError);
      } else {
        error.value = '입력 내용을 확인해주세요.';
      }
    } else if (err.response?.status === 500) {
      error.value = '서버 오류가 발생했습니다. 마이그레이션이 필요할 수 있습니다.';
    } else if (err.message && err.message.includes('로그인')) {
      error.value = err.message;
      alert(err.message);
      router.push('/');
    } else {
      error.value = '게시글 등록에 실패했습니다. 네트워크 연결을 확인해주세요.';
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* MIA Cinema Style - Pure Black */
.create-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding-bottom: 4rem;
}

/* Header */
.create-header {
  padding: 3rem 0 2rem;
  max-width: 900px;
  margin: 0 auto;
  padding-left: 3rem;
  padding-right: 3rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.btn-back-minimal {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.625rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-back-minimal:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

.header-text {
  flex: 1;
}

.page-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #8b5cf6;
  margin-bottom: 0.75rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  margin: 0;
  color: #ffffff;
}

/* Content */
.create-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 3rem;
}

.create-form {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.01em;
}

.form-description {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
  margin: -0.5rem 0 0 0;
}

/* Selected Movie Card */
.selected-movie-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.selected-movie-card:hover {
  background: rgba(255, 255, 255, 0.05);
}

.selected-poster {
  width: 60px;
  height: 90px;
  border-radius: 4px;
  object-fit: cover;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.selected-info {
  flex: 1;
}

.selected-info h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.25rem 0;
}

.selected-info p {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.btn-clear-minimal {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.5);
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
}

.btn-clear-minimal:hover {
  background: rgba(245, 87, 108, 0.1);
  border-color: rgba(245, 87, 108, 0.3);
  color: #f5576c;
}

/* Search Section */
.search-input-container {
  position: relative;
}

.search-input-minimal {
  width: 100%;
  padding: 0.875rem 3rem 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.search-input-minimal:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.search-input-minimal::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.search-icon-minimal {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: rgba(255, 255, 255, 0.3);
  pointer-events: none;
}

.searching-state {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.8125rem;
}

.spinner-small {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Search Results */
.search-results-minimal {
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.02);
}

.result-item-minimal {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.875rem 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.result-item-minimal:last-child {
  border-bottom: none;
}

.result-item-minimal:hover {
  background: rgba(255, 255, 255, 0.05);
}

.result-poster-mini {
  width: 36px;
  height: 54px;
  border-radius: 3px;
  object-fit: cover;
}

.result-placeholder-mini {
  width: 36px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  font-size: 1.25rem;
  opacity: 0.3;
}

.result-details h5 {
  font-size: 0.875rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 0.25rem 0;
}

.result-details p {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.35);
  margin: 0;
}

/* Inputs */
.input-minimal,
.textarea-minimal {
  width: 100%;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 0.875rem 1rem;
  color: #ffffff;
  font-size: 0.9375rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.input-minimal:focus,
.textarea-minimal:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.input-minimal::placeholder,
.textarea-minimal::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.textarea-minimal {
  resize: vertical;
  line-height: 1.7;
  min-height: 300px;
}

.char-counter {
  text-align: right;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.3);
}

/* Error */
.error-minimal {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: rgba(245, 87, 108, 0.1);
  border: 1px solid rgba(245, 87, 108, 0.2);
  border-radius: 4px;
  color: #f5576c;
  font-size: 0.875rem;
}

/* Submit Button */
.btn-submit-minimal {
  width: 100%;
  padding: 1rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-submit-minimal:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-submit-minimal:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .create-header {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .create-content {
    padding: 2rem 1.5rem;
  }
}
</style>