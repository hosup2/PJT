<template>
  <div class="community-container">
    <!-- Minimal Header -->
    <header class="cinema-header">
      <div class="header-inner">
        <div class="header-left">
          <span class="section-label">COMMUNITY</span>
          <h1 class="page-title">영화 수다</h1>
          <p class="page-subtitle">영화를 사랑하는 사람들의 이야기</p>
        </div>
        <button v-if="isLoggedIn" @click="goToCreate" class="btn-write-minimal">
          <span>새 글 작성</span>
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
      </div>
    </header>

    <!-- Trending Section (영화별 대형 카드) -->
    <section v-if="trendingPosts.length > 0" class="trending-section">
      <div class="section-head">
        <span class="section-label">TRENDING NOW</span>
        <h2 class="section-title">지금 뜨거운 수다</h2>
      </div>

      <div class="trending-grid">
        <article
          v-for="post in trendingPosts"
          :key="'trending-' + post.id"
          class="trending-card"
          @click="goToDetail(post.id)"
        >
          <!-- 대형 포스터 -->
          <div class="trending-poster">
            <img
              v-if="post.movie_poster"
              :src="`https://image.tmdb.org/t/p/w500${post.movie_poster}`"
              :alt="post.movie_title"
            />
            <div v-else class="poster-placeholder-large">
              <span>🎬</span>
            </div>
          </div>

          <!-- 간결한 정보 -->
          <div class="trending-info">
            <h3 class="trending-movie">{{ post.movie_title || '자유 수다' }}</h3>
            <p class="trending-title">{{ post.title }}</p>
            <div class="trending-meta">
              <span>{{ post.author.username }}</span>
              <span class="meta-dot">·</span>
              <span>💬 {{ post.comment_count }}</span>
            </div>
          </div>
        </article>
      </div>
    </section>

    <!-- Filter Bar - 심플하게 -->
    <div class="filter-bar">
      <div class="filter-inner">
        <div class="filter-buttons">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            :class="['filter-btn', { active: filter === tab.value }]"
            @click="filter = tab.value"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="search-minimal">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="검색..."
          />
          <svg class="search-icon-minimal" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- Main Feed - 포스터 중심 리스트 -->
    <main class="feed-main">
      <!-- Loading -->
      <div v-if="loading" class="loading-minimal">
        <div class="spinner-minimal"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-minimal">
        <p>{{ error }}</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredPosts.length === 0" class="empty-minimal">
        <span class="empty-icon-minimal">🎭</span>
        <h3>아직 이야기가 없습니다</h3>
        <p>첫 번째 이야기를 시작해보세요</p>
        <button v-if="isLoggedIn" @click="goToCreate" class="btn-start">시작하기</button>
      </div>

      <!-- Posts List -->
      <div v-else class="feed-list">
        <article
          v-for="post in filteredPosts"
          :key="post.id"
          class="feed-item"
          @click="goToDetail(post.id)"
        >
          <!-- Left: Poster -->
          <div class="item-poster">
            <img
              v-if="post.movie_poster"
              :src="`https://image.tmdb.org/t/p/w185${post.movie_poster}`"
              :alt="post.movie_title"
            />
            <div v-else class="poster-placeholder">
              <span>🎬</span>
            </div>
          </div>

          <!-- Right: Content -->
          <div class="item-content">
            <!-- Movie Badge -->
            <span v-if="post.movie_title" class="movie-label">
              {{ post.movie_title }}
            </span>

            <!-- Title -->
            <h3 class="item-title">{{ post.title }}</h3>

            <!-- Meta -->
            <div class="item-meta">
              <span class="meta-author">{{ post.author.username }}</span>
              <span class="meta-dot">·</span>
              <span class="meta-time">{{ formatRelativeTime(post.created_at) }}</span>
              <span class="meta-dot">·</span>
              <span class="meta-stats">💬 {{ post.comment_count }}</span>
              <span class="meta-dot">·</span>
              <span class="meta-stats">👁 {{ post.view_count }}</span>
            </div>
          </div>
        </article>
      </div>
    </main>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import type { Ref } from 'vue';

interface Author {
  id: number;
  username: string;
}

interface Post {
  id: number;
  author: Author;
  title: string;
  movie_id?: number;
  movie_title?: string;
  movie_poster?: string;
  created_at: string;
  comment_count: number;
  view_count: number;
}

const router = useRouter();
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');

const posts = ref<Post[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);
const filter = ref('all');
const searchQuery = ref('');

const tabs = [
  { label: '전체', value: 'all' },
  { label: '영화별', value: 'movie' },
  { label: '인기글', value: 'popular' },
];

// Trending: 영화 포스터 있는 인기글 (상단 대형 카드)
const trendingPosts = computed(() => {
  return posts.value
    .filter(post => post.movie_poster && (post.comment_count >= 3 || post.view_count >= 15))
    .slice(0, 4);
});

// 필터링된 일반 게시글
const filteredPosts = computed(() => {
  let result = posts.value;

  if (filter.value === 'movie') {
    result = result.filter(post => post.movie_id);
  } else if (filter.value === 'popular') {
    result = result.filter(post => post.comment_count > 5 || post.view_count > 20);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(post =>
      post.title.toLowerCase().includes(query) ||
      post.movie_title?.toLowerCase().includes(query)
    );
  }

  return result;
});

onMounted(async () => {
  await fetchPosts();
});

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/posts/');
    posts.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to fetch posts:', err);
    error.value = '게시글을 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
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

const goToCreate = () => {
  if (!isLoggedIn?.value) {
    alert('로그인이 필요합니다.');
    router.push('/');
    return;
  }
  router.push('/community/create');
};

const goToDetail = (id: number) => {
  router.push(`/community/post/${id}`);
};
</script>

<style scoped>
/* 🎨 MIA Design System - Pure Black Cinema */
.community-container {
  min-height: 100vh;
  background: #0a0b0f; /* MIA 순수 검정 */
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding-bottom: 5rem;
}

/* ============ HEADER ============ */
.cinema-header {
  padding: 4rem 0 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.header-left {
  flex: 1;
}

.section-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #8b5cf6; /* MIA 보라색 */
  margin-bottom: 1rem;
}

.page-title {
  font-size: 3rem;
  font-weight: 300; /* 얇은 폰트 - MIA 스타일 */
  letter-spacing: -0.02em;
  margin: 0 0 0.75rem 0;
  color: #ffffff;
}

.page-subtitle {
  font-size: 1rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.01em;
}

.btn-write-minimal {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-write-minimal:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

/* ============ TRENDING SECTION ============ */
.trending-section {
  padding: 4rem 0;
  max-width: 1400px;
  margin: 0 auto;
  padding-left: 3rem;
  padding-right: 3rem;
}

.section-head {
  margin-bottom: 2.5rem;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 300;
  letter-spacing: -0.01em;
  margin: 0.5rem 0 0 0;
  color: #ffffff;
}

.trending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 2.5rem;
}

.trending-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.trending-card:hover {
  transform: translateY(-8px);
}

.trending-poster {
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 1.25rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6); /* MIA 포스터 그림자 */
}

.trending-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder-large {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1b20 0%, #0f1014 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  opacity: 0.3;
}

.trending-info {
  padding: 0 0.25rem;
}

.trending-movie {
  font-size: 0.8125rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 0.5rem 0;
  letter-spacing: 0.01em;
}

.trending-title {
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.trending-meta {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.35);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-dot {
  opacity: 0.5;
}

/* ============ FILTER BAR ============ */
.filter-bar {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  background: rgba(10, 11, 15, 0.95);
  backdrop-filter: blur(20px);
  z-index: 10;
}

.filter-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.filter-buttons {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1.25rem;
  background: transparent;
  border: 1px solid transparent;
  color: rgba(255, 255, 255, 0.4);
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-btn:hover {
  color: rgba(255, 255, 255, 0.7);
}

.filter-btn.active {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.03);
}

.search-minimal {
  position: relative;
  width: 300px;
}

.search-minimal input {
  width: 100%;
  padding: 0.625rem 2.5rem 0.625rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  color: #ffffff;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.search-minimal input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.15);
}

.search-minimal input::placeholder {
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

/* ============ MAIN FEED ============ */
.feed-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 3rem;
}

.feed-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.feed-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 2rem;
  padding: 2.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
}

.feed-item:hover {
  background: rgba(255, 255, 255, 0.01);
}

.feed-item:hover .item-poster {
  transform: scale(1.05);
}

.item-poster {
  width: 120px;
  aspect-ratio: 2/3;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease;
}

.item-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1b20 0%, #0f1014 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  opacity: 0.3;
}

.item-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
}

.movie-label {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  color: #8b5cf6;
  text-transform: uppercase;
}

.item-title {
  font-size: 1.5rem;
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #ffffff;
  margin: 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.35);
}

.meta-author {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
}

/* ============ STATES ============ */
.loading-minimal,
.error-minimal,
.empty-minimal {
  text-align: center;
  padding: 6rem 2rem;
  color: rgba(255, 255, 255, 0.4);
}

.spinner-minimal {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0 auto 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon-minimal {
  font-size: 3rem;
  display: block;
  margin-bottom: 1.5rem;
  opacity: 0.3;
}

.empty-minimal h3 {
  font-size: 1.5rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
}

.btn-start {
  margin-top: 2rem;
  padding: 0.875rem 2rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-start:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.3);
}

/* ============ FAB ============ */
.fab-minimal {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  width: 3.5rem;
  height: 3.5rem;
  background: #8b5cf6;
  border: none;
  border-radius: 50%;
  color: white;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab-minimal:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 30px rgba(139, 92, 246, 0.5);
}

.fab-badge-minimal {
  position: absolute;
  top: -0.25rem;
  right: -0.25rem;
  background: #ef4444;
  color: white;
  font-size: 0.6875rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 10px;
  min-width: 1.25rem;
  text-align: center;
}

/* ============ RESPONSIVE ============ */
@media (max-width: 1024px) {
  .header-inner,
  .trending-section,
  .filter-inner,
  .feed-main {
    padding-left: 2rem;
    padding-right: 2rem;
  }

  .trending-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 2rem;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .header-inner {
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
  }

  .trending-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .filter-inner {
    flex-direction: column;
    align-items: stretch;
  }

  .search-minimal {
    width: 100%;
  }

  .feed-item {
    grid-template-columns: 80px 1fr;
    gap: 1.5rem;
    padding: 2rem 0;
  }

  .item-poster {
    width: 80px;
  }

  .item-title {
    font-size: 1.125rem;
  }
}
</style>