<template>
  <div class="detail-container">
    
    <div v-if="loading" class="state-minimal">
      <div class="spinner-minimal"></div>
      <p>영화 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else-if="error" class="state-minimal error">
      <p>{{ error }}</p>
    </div>

    <div v-else-if="movie" class="content-wrapper">
      
      <section class="hero-section">
        <div class="hero-backdrop">
          <img :src="backdropUrl" :alt="movie.title" />
          <div class="hero-overlay"></div>
        </div>

        <div class="hero-inner">
          <button @click="router.back()" class="btn-back-minimal">
            <ArrowLeft class="icon-sm" />
            <span>뒤로가기</span>
          </button>

          <div class="hero-content">
            <div class="hero-text">
              <div class="title-row">
                <h1 class="movie-title">{{ movie.title }}</h1>
                <button
                  @click="handleLikeMovie"
                  :disabled="!isLoggedIn"
                  :class="['btn-like-hero', { active: isMovieLiked, disabled: !isLoggedIn }]"
                  :title="isMovieLiked ? '찜 취소' : '찜하기'"
                >
                  <svg 
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    class="icon-like"
                    stroke-width="2"
                  >
                    <path 
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                      stroke-linecap="round" 
                      stroke-linejoin="round"
                    />
                  </svg>
                </button>
              </div>

              <p v-if="movie.original_title !== movie.title" class="original-title">
                {{ movie.original_title }}
              </p>

              <div class="meta-row">
                <div v-if="movie.director" class="director-info">
                  <span class="label">DIRECTOR</span>
                  <span class="value">{{ movie.director.name }}</span>
                </div>
                
                <div class="info-divider"></div>

                <div class="basic-info">
                  <div class="info-item">
                    <Calendar class="icon-xs" />
                    <span>{{ formatDate(movie.release_date) }}</span>
                  </div>
                  <div class="info-item">
                    <Clock class="icon-xs" />
                    <span>{{ movie.runtime }}분</span>
                  </div>
                </div>
              </div>

              <div class="genre-list">
                <span
                  v-for="genre in movie.genres"
                  :key="genre"
                  class="genre-tag"
                >
                  {{ genre }}
                </span>
              </div>

              <div class="rating-row">
                <div class="main-rating">
                  <Star class="icon-lg star-filled" />
                  <span class="score">{{ movieStats.avg_rating.toFixed(1) }}</span>
                </div>
                
                <div v-if="movie.tmdb_rating" class="sub-rating">
                  <span class="label">TMDb</span>
                  <span class="value">{{ movie.tmdb_rating.toFixed(1) }}</span>
                </div>
              </div>
            </div>

            <div class="hero-poster">
              <div class="poster-frame">
                <img :src="posterUrl" :alt="movie.title" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <main class="detail-grid">
        
        <div class="left-column">
          
          <section class="section-box">
            <h2 class="section-title">SYNOPSIS</h2>
            <p class="plot-text">{{ movie.overview }}</p>
          </section>

          <section class="section-box">
            <h2 class="section-title">CAST</h2>
            <div v-if="movie.casts && movie.casts.length" class="cast-grid">
              <div
                v-for="cast in movie.casts"
                :key="cast.actor.tmdb_id"
                @click="openPersonDetail(cast.actor)"
                class="cast-card"
              >
                <div class="cast-photo">
                  <img
                    :src="getProfileUrl(cast.actor.profile_path)"
                    :alt="cast.actor.name"
                  />
                </div>
                <div class="cast-info">
                  <p class="actor-name">{{ cast.actor.name }}</p>
                  <p class="character-name">{{ cast.character ? cast.character : '출연' }}</p>
                </div>
              </div>
            </div>
          </section>

          <section class="section-box">
            <h2 class="section-title">RATING DISTRIBUTION</h2>
            <div class="chart-container">
              <RatingDistributionChart 
                :movie-id="parseInt(id)"
                :distribution="movieStats.rating_distribution"
                :total-count="movieStats.rating_count"
              />
            </div>
          </section>

          <section class="section-box">
            <h2 class="section-title">REVIEWS <span class="count">({{ comments.length }})</span></h2>
            <CommentSection
              :key="refreshKey"
              :comments="comments"
              :is-logged-in="isLoggedIn"
              :rating="userRating"
              @submit-comment="handleSubmitComment"
              @edit-comment="handleEditComment"
              @delete-comment="handleDeleteComment"
              @like-comment="handleLikeComment"
              @navigate-to-user="handleNavigateToUser"
              @open-auth="emit('openAuth')"
              @rating-change="handleRatingChange"
            />
          </section>
        </div>

        <aside class="right-column">
          <div class="sticky-sidebar">
            <div class="rating-summary">
              <div class="summary-header">
                <div class="summary-score">
                  <Star class="icon-md star-filled" />
                  <span class="score-text">{{ movieStats.avg_rating.toFixed(1) }}</span>
                </div>
                <p class="summary-count">{{ movieStats.rating_count.toLocaleString() }}명 참여</p>
              </div>

              <div class="summary-action">
                <p class="action-label">이 영화를 평가해주세요</p>
                <div v-if="!isLoggedIn">
                  <button
                    @click="emit('openAuth')"
                    class="btn-primary-full"
                  >
                    로그인하고 평가하기
                  </button>
                </div>
                </div>
            </div>
          </div>
        </aside>

      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ArrowLeft, Calendar, Clock, Star } from 'lucide-vue-next';
import StarRating from './StarRating.vue';
import RatingDistributionChart from './RatingDistributionChart.vue';
import CommentSection from './CommentSection.vue';

// --- Interfaces (Preserved) ---
interface Actor {
  tmdb_id: number;
  name: string;
  profile_path?: string | null;
}

interface Cast {
  actor: Actor;
  character: string;
  order: number;
}

interface Movie {
  id: number;
  title: string;
  original_title: string;
  poster_path: string;
  backdrops: string;
  release_date: string;
  runtime: number;
  genres: string[];
  overview: string;
  stats: {
    avg_rating: number;
    rating_count: number;
    rating_distribution: Record<string, number>;
  };
  tmdb_rating: number;
  imdb_rating: number;
  comments: Comment[];
  director?: Actor | null;
  casts?: Cast[];
  user_data?: {
    rating: number;
    comment: string;
    is_liked: boolean;
  };
}

interface Comment {
  id: number;
  user_id: number;
  username: string;
  rating?: number;
  comment: string;
  created_at: string;
  profile_image?: string;
  spoiler?: boolean;
  likesCount?: number;
  isLiked?: boolean;
}

interface User {
  id: number;
  username: string;
}

// --- Props & Emits ---
const props = defineProps<{
  id: string;
}>();

const emit = defineEmits<{
  openAuth: [];
  'activity-updated': [];
}>();

// --- State ---
const router = useRouter();
const movie = ref<Movie | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const refreshKey = ref(0);

const isLoggedIn = inject<Ref<boolean>>('isLoggedIn', ref(false));
const currentUser = inject<Ref<User | null>>('currentUser', ref(null));

// --- Data Fetching ---
const fetchMovieData = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/${props.id}/`, {
      params: { _: new Date().getTime() },
    });
    movie.value = JSON.parse(JSON.stringify(response.data));

    if (movie.value?.user_data) {
      userRating.value = movie.value.user_data.rating || 0;
      commentText.value = movie.value.user_data.comment || '';
      isMovieLiked.value = movie.value.user_data.is_liked;
    }
    refreshKey.value++;
  } catch (err) {
    console.error(`Failed to fetch movie ${props.id}:`, err);
    error.value = '영화 정보를 불러오는 데 실패했습니다.';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await fetchMovieData();
});

// --- Computed ---
const comments = computed(() => {
  const _ = refreshKey.value;
  return movie.value?.comments || [];
});

const posterUrl = computed(() => {
  if (movie.value?.poster_path && !movie.value.poster_path.startsWith('http')) {
    return `https://image.tmdb.org/t/p/w500${movie.value.poster_path}`;
  }
  return movie.value?.poster_path || 'https://via.placeholder.com/500x750?text=No+Image';
});

const backdropUrl = computed(() => {
  if (movie.value?.backdrops && !movie.value.backdrops.startsWith('http')) {
    return `https://image.tmdb.org/t/p/original${movie.value.backdrops}`;
  }
  return movie.value?.backdrops || posterUrl.value;
});

// --- Logic ---
const userRating = ref(0);
const commentText = ref('');
const isMovieLiked = ref(false);
const movieLikesCount = ref(0);

const saveActivity = async () => {
  if (!isLoggedIn.value) return;
  try {
    const payload = {
      rating: userRating.value || null,
      comment: commentText.value,
    };
    await axios.post(`http://127.0.0.1:8000/movies/${props.id}/rating/`, payload);
    alert('리뷰가 저장되었습니다.');
    await fetchMovieData();
    commentText.value = '';
    userRating.value = 0;
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to save activity:', err);
    alert('리뷰 저장에 실패했습니다.');
  }
};

const handleRatingChange = (rating: number) => {
  if (!isLoggedIn.value) return emit('openAuth');
  userRating.value = rating;
};

const handleLikeMovie = async () => {
  if (!isLoggedIn.value) return emit('openAuth');
  const originalLikedStatus = isMovieLiked.value;
  isMovieLiked.value = !isMovieLiked.value;
  movieLikesCount.value += isMovieLiked.value ? 1 : -1;

  try {
    if (originalLikedStatus) {
      await axios.delete(`http://127.0.0.1:8000/users/favorites/${props.id}/`);
    } else {
      await axios.post(`http://127.0.0.1:8000/users/favorites/${props.id}/`);
    }
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to update like status:', err);
    alert('좋아요 상태를 업데이트하는 데 실패했습니다.');
    isMovieLiked.value = originalLikedStatus;
    movieLikesCount.value += originalLikedStatus ? 1 : -1;
  }
};

const handleSubmitComment = (content: string, spoiler: boolean) => {
  commentText.value = content;
  saveActivity();
};

const handleEditComment = async (commentId: number, content: string, rating: number, spoiler: boolean) => {
  if (!isLoggedIn.value) return;
  try {
    const payload = { rating, comment: content, spoiler };
    await axios.put(`http://127.0.0.1:8000/movies/${props.id}/ratings/${commentId}/`, payload);
    alert('리뷰가 수정되었습니다.');
    await fetchMovieData();
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to edit comment:', err);
    alert('리뷰 수정에 실패했습니다.');
  }
};

const handleDeleteComment = async (commentId: number) => {
  if (!isLoggedIn.value) return;
  try {
    await axios.delete(`http://127.0.0.1:8000/movies/${props.id}/ratings/${commentId}/`);
    alert('리뷰가 삭제되었습니다.');
    await fetchMovieData();
    emit('activity-updated');
  } catch (err) {
    console.error('Failed to delete comment:', err);
    alert('리뷰 삭제에 실패했습니다.');
  }
};

const handleLikeComment = async (commentId: number) => {
  if (!isLoggedIn.value) {
    emit('openAuth');
    return;
  }

  if (!movie.value) return;

  try {
    // 백엔드 호출
    const response = await axios.post(
      `http://127.0.0.1:8000/movies/${props.id}/ratings/${commentId}/like/`,
      {},
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      }
    );
    
    // 🔥 조용히 영화 데이터 다시 불러오기 (로딩 없이)
    const movieResponse = await axios.get(
      `http://127.0.0.1:8000/movies/${props.id}/`,
      { 
        params: { _: new Date().getTime() },
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      }
    );
    
    movie.value = JSON.parse(JSON.stringify(movieResponse.data));
    
    if (movie.value?.user_data) {
      userRating.value = movie.value.user_data.rating || 0;
      commentText.value = movie.value.user_data.comment || '';
      isMovieLiked.value = movie.value.user_data.is_liked;
    }
    
    refreshKey.value++;

  } catch (err: any) {
    console.error(`Failed to like comment ${commentId}:`, err);
    
    if (err.response?.status === 401) {
      alert('로그인이 만료되었습니다.');
      emit('openAuth');
    } else {
      alert('리뷰 좋아요 처리에 실패했습니다.');
    }
  }
};

const handleNavigateToUser = (userId: number) => {
  router.push({ name: 'UserProfile', params: { userId } });
};

const formatDate = (dateStr: string) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const yy = String(date.getFullYear());
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  return `${yy}.${mm}.${dd}`;
};

const getProfileUrl = (path?: string | null) => {
  if (!path) return 'https://via.placeholder.com/185x278?text=No+Image';
  if (path.startsWith('http')) return path;
  return `https://image.tmdb.org/t/p/w185${path}`;
};

const movieStats = computed(() => {
  const _ = refreshKey.value;
  return movie.value?.stats ?? {
    avg_rating: 0,
    rating_count: 0,
    rating_distribution: {},
  };
});

const openPersonDetail = (person: Cast['actor']) => {
  if (!person || !person.tmdb_id) return;
  const url = `https://www.themoviedb.org/person/${person.tmdb_id}?language=ko-KR`;
  window.open(url, '_blank');
};
</script>

<style scoped>
/* 🎨 MIA Cinema - Detail Page */
.detail-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding-bottom: 5rem;
}

/* ============ STATE ============ */
.state-minimal {
  padding: 8rem 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.4);
}

.state-minimal.error {
  color: #f87171;
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

@keyframes spin { to { transform: rotate(360deg); } }

/* ============ HERO SECTION ============ */
.hero-section {
  position: relative;
  width: 100%;
  height: 80vh; /* Cinematic Height */
  min-height: 600px;
  max-height: 900px;
  overflow: hidden;
}

.hero-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.hero-backdrop img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.6;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(10, 11, 15, 0.2) 0%,
    rgba(10, 11, 15, 0.8) 60%,
    #0a0b0f 100%
  );
}

.hero-inner {
  position: relative;
  height: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding-bottom: 4rem;
}

.btn-back-minimal {
  position: absolute;
  top: 2rem;
  left: 3rem;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.625rem 1.25rem;
  border-radius: 100px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  z-index: 10;
}

.btn-back-minimal:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.hero-content {
  display: flex;
  align-items: flex-end;
  gap: 4rem;
}

.hero-text {
  flex: 1;
  margin-bottom: 1rem;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 0.5rem;
}

.movie-title {
  font-size: 4rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1.1;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.btn-like-hero {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-like-hero:hover:not(.disabled) {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.5);
}

.btn-like-hero.active {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.btn-like-hero.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon-like {
  width: 1.5rem;
  height: 1.5rem;
  fill: none;
  stroke: #ffffff;
  transition: all 0.3s ease;
}

.btn-like-hero.active .icon-like {
  fill: #ef4444;
  stroke: #ef4444;
}

.original-title {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.5);
  margin: 0 0 2rem 0;
  font-weight: 300;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.9375rem;
}

.director-info {
  display: flex;
  flex-direction: column;
}

.director-info .label {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #8b5cf6;
  margin-bottom: 0.25rem;
}

.director-info .value {
  color: #ffffff;
  font-weight: 500;
}

.info-divider {
  width: 1px;
  height: 2rem;
  background: rgba(255, 255, 255, 0.1);
}

.basic-info {
  display: flex;
  gap: 1.5rem;
  color: rgba(255, 255, 255, 0.7);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.genre-list {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2.5rem;
}

.genre-tag {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  padding: 0.4rem 1rem;
  border-radius: 100px;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.rating-row {
  display: flex;
  align-items: flex-end;
  gap: 2rem;
}

.main-rating {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.star-filled {
  color: #fbbf24;
  fill: #fbbf24;
}

.main-rating .score {
  font-size: 3.5rem;
  font-weight: 600;
  line-height: 1;
  color: #ffffff;
}

.sub-rating {
  padding-bottom: 0.5rem;
  padding-left: 2rem;
  border-left: 1px solid rgba(255, 255, 255, 0.1);
}

.sub-rating .label {
  display: block;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 0.25rem;
}

.sub-rating .value {
  font-size: 1.5rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
}

/* Hero Poster */
.hero-poster {
  width: 300px;
  flex-shrink: 0;
  display: none; /* Mobile hidden */
}

@media (min-width: 1024px) {
  .hero-poster {
    display: block;
  }
}

.poster-frame {
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transform: translateY(4rem); /* Float effect */
}

.poster-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ============ MAIN GRID ============ */
.detail-grid {
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 3rem;
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 4rem;
}

.section-box {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #8b5cf6;
  margin: 0 0 1.5rem 0;
  text-transform: uppercase;
}

.section-title .count {
  color: rgba(255, 255, 255, 0.4);
  font-weight: 400;
  margin-left: 0.25rem;
}

.plot-text {
  font-size: 1.0625rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 300;
}

/* Cast Grid */
.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 1.25rem;
}

.cast-card {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.cast-card:hover {
  transform: translateY(-4px);
}

.cast-photo {
  width: 100%;
  aspect-ratio: 2/3;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
}

.cast-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.actor-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.125rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.character-name {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Sidebar */
.right-column {
  position: relative;
}

.sticky-sidebar {
  position: sticky;
  top: 2rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 2rem;
}

.summary-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.summary-score {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.score-text {
  font-size: 2.5rem;
  font-weight: 700;
  color: #ffffff;
}

.summary-count {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

.action-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 1rem;
  text-align: center;
}

.btn-primary-full {
  width: 100%;
  padding: 0.875rem;
  background: #8b5cf6;
  border: none;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-primary-full:hover {
  background: #7c3aed;
}

/* Chart Container */
.chart-container {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  padding: 1.5rem;
}

/* Icons */
.icon-xs { width: 14px; height: 14px; }
.icon-sm { width: 18px; height: 18px; }
.icon-md { width: 24px; height: 24px; }
.icon-lg { width: 32px; height: 32px; }

/* Responsive */
@media (max-width: 1024px) {
  .detail-grid {
    grid-template-columns: 1fr;
    padding: 3rem 2rem;
  }
  
  .hero-poster {
    display: none;
  }
  
  .hero-inner {
    padding: 0 2rem 3rem;
  }
  
  .movie-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .title-row {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .rating-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .sub-rating {
    border-left: none;
    padding-left: 0;
  }
}
</style>