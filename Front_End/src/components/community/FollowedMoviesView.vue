<template>
  <div class="community-container">
    
    <header class="cinema-header">
      <div class="header-inner">
        <button @click="router.back()" class="btn-back-minimal">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
          </svg>
          <span>뒤로가기</span>
        </button>

        <div class="header-content">
          <span class="section-label">CURATION</span>
          <h1 class="page-title">친구들의 인생영화</h1>
          <p class="page-subtitle">내가 팔로우한 친구들이 선택한 최고의 작품들</p>
        </div>
      </div>
    </header>

    <main class="content-main">
      
      <section v-if="followingUsers.length > 0" class="following-section">
        <h2 class="section-title">
          {{ selectedUserId ? '선택된 친구의 영화' : '팔로우 중인 친구들' }}
          <span v-if="selectedUserId" @click="clearFilter" class="reset-filter"></span>
        </h2>
        
        <div class="following-list">
          <div 
            v-for="user in followingUsers" 
            :key="user.id" 
            class="following-item"
            @click="filterByFriend(user.id)"
          >
            <div :class="['avatar-wrapper', { active: selectedUserId === user.id }]">
              <img 
                :src="getProfileImage(user.profile_image)" 
                :alt="user.username"
                class="avatar-circle"
                @error="handleImageError" 
              />
            </div>
            <span :class="['following-name', { active: selectedUserId === user.id }]">
              {{ user.username }}
            </span>
          </div>
        </div>
      </section>
      
      <div v-if="loading" class="state-minimal">
        <div class="spinner-minimal"></div>
      </div>

      <div v-else-if="displayedMovies.length === 0" class="empty-minimal">
        <span class="empty-icon">🎬</span>
        <h3>영화가 없습니다</h3>
        <p v-if="selectedUserId">이 친구가 아직 인생영화를 선택하지 않았습니다.</p>
        <p v-else>친구들이 선택한 인생영화를 기다려보세요.</p>
        <button v-if="selectedUserId" @click="clearFilter" class="btn-action">
          전체 목록 보기
        </button>
        <button v-else @click="router.push('/explore')" class="btn-action">
          친구 찾으러 가기
        </button>
      </div>

      <div v-else class="movie-grid">
        <article 
          v-for="movie in displayedMovies" 
          :key="movie.id" 
          class="movie-card"
          @click="goToMovieDetail(movie.movie_id)"
        >
          <div class="poster-wrapper">
            <img 
              :src="getImageUrl(movie.movie_poster)" 
              :alt="movie.movie_title"
              class="poster-img"
              @error="handlePosterError"
            />
            <div class="overlay">
              <span class="view-text">상세보기</span>
            </div>
          </div>

          <div class="card-info">
            <h3 class="movie-title">{{ movie.movie_title }}</h3>
            
            <div class="user-profile" @click.stop="goToUserProfile(movie.user_id)">
              <img 
                :src="getProfileImage(movie.profile_image)" 
                class="avatar-mini"
                @error="handleImageError"
              />
              <div class="user-text">
                <span class="username">{{ movie.username }}</span>
                <span class="pick-label">'s Pick</span>
              </div>
            </div>
          </div>
        </article>
      </div>

    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

interface FollowedMovie {
  id: number;
  user_id: number;
  username: string;
  profile_image: string | null;
  movie_id: number;
  movie_title: string;
  movie_poster: string;
}

interface User {
  id: number;
  username: string;
  profile_image: string | null;
}

const router = useRouter();
const allMovies = ref<FollowedMovie[]>([]); // 전체 데이터 원본
const followingUsers = ref<User[]>([]);
const loading = ref(true);
const selectedUserId = ref<number | null>(null); // 선택된 친구 ID

// ✅ 필터링된 영화 목록 (Computed)
const displayedMovies = computed(() => {
  if (!selectedUserId.value) {
    return allMovies.value;
  }
  return allMovies.value.filter(movie => movie.user_id === selectedUserId.value);
});

// ✅ 이미지 URL 처리 (에러 방지 강화)
const getImageUrl = (path: string | null) => {
  if (!path) return 'https://via.placeholder.com/500x750?text=No+Image';
  return path.startsWith('http') ? path : `https://image.tmdb.org/t/p/w500${path}`;
};

const getProfileImage = (path: string | null) => {
  if (!path) return '/mia5.png'; // 기본 이미지
  return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`;
};

// ✅ 이미지 로딩 에러 핸들러
const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/mia5.png'; // 프로필 기본 이미지로 교체
};

const handlePosterError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = 'https://via.placeholder.com/500x750?text=No+Image';
};

const goToMovieDetail = (id: number) => {
  router.push(`/movie/${id}`);
};

const goToUserProfile = (userId: number) => {
  if (userId) router.push(`/profile/${userId}`);
};

// ✅ 친구 필터링 함수
const filterByFriend = (userId: number) => {
  if (selectedUserId.value === userId) {
    selectedUserId.value = null; // 이미 선택된 친구면 해제
  } else {
    selectedUserId.value = userId; // 선택
  }
};

const clearFilter = () => {
  selectedUserId.value = null;
};

onMounted(async () => {
  const token = localStorage.getItem('accessToken');

  if (!token) {
    alert('로그인이 필요한 서비스입니다.');
    router.push('/'); 
    return;
  }

  try {
    const meResponse = await axios.get('http://127.0.0.1:8000/users/me/', {
        headers: { Authorization: `Bearer ${token}` }
    });
    const myId = meResponse.data.id;

    const followingResponse = await axios.get(`http://127.0.0.1:8000/users/${myId}/following/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    followingUsers.value = followingResponse.data;

    const response = await axios.get('http://127.0.0.1:8000/users/followed-life-movies/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    allMovies.value = response.data; // 원본 데이터 저장
    
  } catch (error) {
    console.error('Failed to fetch data:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* 🎨 MIA Cinema System - Pure Black */
.community-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', sans-serif;
  padding-top: 5rem;
  padding-bottom: 4rem;
  display: flex;
  flex-direction: column;
}

/* Header */
.cinema-header {
  padding: 2rem 3rem 1rem;
  background: rgba(10, 11, 15, 0.95);
  backdrop-filter: blur(20px);
  position: static;
  top: 4rem; 
  z-index: 40;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
}

.btn-back-minimal {
  position: absolute;
  top: -2.5rem; /* 2rem → 1rem (더 위로) */
  left: 2rem;
  z-index: 50;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.5rem 1rem;
  border-radius: 100px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0;
}

.btn-back-minimal:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-color: rgba(255, 255, 255, 0.3);
}

.section-label {
  font-size: 0.6875rem;
  font-weight: 700;
  color: #8b5cf6;
  letter-spacing: 0.1em;
  display: block;
  margin-bottom: 0.25rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 300;
  margin: 0;
  color: white;
  line-height: 1.1;
}

.page-subtitle {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 0.5rem;
}

/* Main Content */
.content-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem;
  width: 100%;
  flex: 1;
}

/* Following Section */
.following-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reset-filter {
  font-size: 0.875rem;
  color: #8b5cf6;
  cursor: pointer;
  font-weight: 400;
}

.reset-filter:hover {
  text-decoration: underline;
}

.following-list {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding-bottom: 1rem;
  scrollbar-width: none;
}
.following-list::-webkit-scrollbar {
    display: none;
}

.following-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  min-width: 80px;
}

.avatar-wrapper {
  padding: 3px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
}

.following-item:hover .avatar-wrapper {
  border-color: rgba(139, 92, 246, 0.5);
}

/* 🔥 Active State (선택됨) */
.avatar-wrapper.active {
  border-color: #8b5cf6; /* Strong Purple */
  box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
}

.avatar-circle {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  display: block;
  background-color: #1f1f1f; /* 이미지 로딩 전 배경 */
}

.following-name {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.2s;
  max-width: 80px;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.following-item:hover .following-name {
  color: white;
}

.following-name.active {
  color: #8b5cf6;
  font-weight: 600;
}


/* Grid Layout */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 2rem;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
}

.movie-card:hover {
  transform: translateY(-8px);
}

/* Poster */
.poster-wrapper {
  position: relative;
  aspect-ratio: 2/3;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 1rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: #1f1f1f;
}

.poster-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-card:hover .poster-img {
  transform: scale(1.05);
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.movie-card:hover .overlay {
  opacity: 1;
}

.view-text {
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 100px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

/* Card Info */
.card-info {
  padding: 0 0.25rem;
}

.movie-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.75rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  transition: background 0.2s;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.08);
}

.avatar-mini {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background-color: #2d2d2d;
}

.user-text {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8125rem;
}

.username {
  color: #c084fc; /* MIA Purple */
  font-weight: 600;
}

.pick-label {
  color: rgba(255, 255, 255, 0.4);
}

/* States */
.state-minimal, .empty-minimal {
  padding: 6rem 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.4);
}

.spinner-minimal {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  margin: 0 auto;
  animation: spin 1s linear infinite;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  opacity: 0.5;
  filter: grayscale(1);
}

.btn-action {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: #8b5cf6;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-action:hover {
  background: #7c3aed;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Responsive */
@media (max-width: 768px) {
  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .cinema-header {
    padding: 1.5rem;
  }
  
  .content-main {
    padding: 1.5rem;
  }
}
</style>