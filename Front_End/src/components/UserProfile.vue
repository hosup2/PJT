<template>
  <div class="profile-container">
    
    <div v-if="!user" class="loading-minimal">
      <div class="spinner-minimal"></div>
      <p class="error-text">사용자 정보를 불러오는 중입니다...</p>
      <button @click="emit('goHome')" class="btn-action-minimal mt-4">
        홈으로 돌아가기
      </button>
    </div>

    <div v-if="user" class="profile-inner">
      
      <header class="profile-header">
        <div class="header-content">
          <div class="profile-avatar-wrapper">
            <img
              :src="user.profile_image || '/mia5.png'"
              :alt="user.username"
              class="profile-avatar"
            />
            <div class="avatar-badge">
              <Star class="icon-sm" />
            </div>
          </div>

          <div class="user-info">
            <span class="user-label">MEMBER PROFILE</span>
            <h1 class="user-name">{{ user.username }}</h1>
            <p class="user-email">{{ user.email }}</p>

            <div class="action-buttons">
              <button
                v-if="!isOwnProfile"
                @click="toggleFollow"
                :class="['btn-follow', { 'active': user.follow_info.is_following }]"
              >
                <UserCheck v-if="user.follow_info.is_following" class="icon-sm" />
                <UserPlus v-else class="icon-sm" />
                <span>{{ user.follow_info.is_following ? '팔로잉' : '팔로우' }}</span>
              </button>

              <button 
                v-if="isOwnProfile" 
                @click="showEditModal = true"
                class="btn-edit"
              >
                프로필 수정
              </button>
            </div>
          </div>
        </div>
      </header>

      <section class="stats-section">
        <div class="stats-grid">
          <button @click="openFollowModal('followers')" class="stat-item clickable">
            <span class="stat-value">{{ user.follow_info.followers_count }}</span>
            <span class="stat-label">
              <Users class="icon-xs" /> 팔로워
            </span>
          </button>
          
          <button @click="openFollowModal('following')" class="stat-item clickable">
            <span class="stat-value">{{ user.follow_info.following_count }}</span>
            <span class="stat-label">
              <UserCheck class="icon-xs" /> 팔로잉
            </span>
          </button>

          <div class="stat-item">
            <span class="stat-value purple">{{ stats.total_ratings }}</span>
            <span class="stat-label">
              <Film class="icon-xs" /> 평가
            </span>
          </div>

          <div class="stat-item">
            <span class="stat-value yellow">{{ stats.avg_rating.toFixed(1) }}</span>
            <span class="stat-label">
              <Star class="icon-xs" /> 평균 별점
            </span>
          </div>

          <div class="stat-item">
            <span class="stat-value red">{{ stats.liked_movies }}</span>
            <span class="stat-label">
              <Heart class="icon-xs" /> 좋아요
            </span>
          </div>

          <div class="stat-item">
            <span class="stat-value blue">{{ stats.total_comments }}</span>
            <span class="stat-label">
              <MessageSquare class="icon-xs" /> 리뷰
            </span>
          </div>
        </div>
      </section>

      <div class="filter-bar">
        <div class="filter-inner">
          <div class="filter-buttons">
            <button
              @click="activeTab = 'ratings'"
              :class="['filter-btn', { active: activeTab === 'ratings' }]"
            >
              평가한 영화
            </button>
            <button
              @click="activeTab = 'likes'"
              :class="['filter-btn', { active: activeTab === 'likes' }]"
            >
              좋아요한 영화
            </button>
            <button
              @click="activeTab = 'comments'"
              :class="['filter-btn', { active: activeTab === 'comments' }]"
            >
              작성한 리뷰
            </button>
          </div>
        </div>
      </div>

      <main class="content-main">
        
        <div v-if="activeTab === 'ratings'" class="tab-content">
          <div class="content-header">
            <h2 class="content-title">평가한 영화 <span class="count">{{ filteredRatings.length }}</span></h2>
            <div class="sub-filters">
              <button @click="ratingFilter = 'all'" :class="['sub-filter-btn', { active: ratingFilter === 'all' }]">전체</button>
              <button @click="ratingFilter = 'high'" :class="['sub-filter-btn', { active: ratingFilter === 'high' }]">4점 이상</button>
              <button @click="ratingFilter = 'low'" :class="['sub-filter-btn', { active: ratingFilter === 'low' }]">2점 이하</button>
            </div>
          </div>

          <div v-if="filteredRatings.length === 0" class="empty-minimal">
            <span class="empty-icon-minimal">🎬</span>
            <h3>평가한 영화가 없습니다</h3>
          </div>

          <div v-else class="movie-grid">
            <article 
              v-for="rating in filteredRatings" 
              :key="rating.movie_id" 
              class="movie-card"
              @click="handleMovieClick(rating.movie_id)"
            >
              <div class="poster-wrapper">
                <img
                  :src="getFullImageUrl(rating.poster_path)"
                  :alt="rating.title"
                  @error="handleImageError"
                />
                <div class="rating-badge">
                  <Star class="icon-xs fill-current" /> {{ rating.rating }}
                </div>
              </div>
              <h3 class="movie-title">{{ rating.title }}</h3>
            </article>
          </div>
        </div>

        <div v-if="activeTab === 'likes'" class="tab-content">
          <div class="content-header">
            <h2 class="content-title">좋아요한 영화 <span class="count">{{ likedMovies.length }}</span></h2>
          </div>

          <div v-if="likedMovies.length === 0" class="empty-minimal">
            <span class="empty-icon-minimal">💔</span>
            <h3>좋아요한 영화가 없습니다</h3>
          </div>

          <div v-else class="movie-grid">
            <article 
              v-for="movie in likedMovies" 
              :key="movie.id" 
              class="movie-card"
              @click="handleMovieClick(movie.id)"
            >
              <div class="poster-wrapper">
                <img
                  :src="getFullImageUrl(movie.poster_path)"
                  :alt="movie.title"
                  @error="handleImageError"
                />
                <div class="like-badge">
                  <Heart class="icon-xs fill-current" />
                </div>
              </div>
              <h3 class="movie-title">{{ movie.title }}</h3>
              <p class="movie-year">{{ new Date(movie.release_date).getFullYear() }}</p>
            </article>
          </div>
        </div>

        <div v-if="activeTab === 'comments'" class="tab-content">
          <div class="content-header">
            <h2 class="content-title">작성한 리뷰 <span class="count">{{ userComments.length }}</span></h2>
          </div>

          <div v-if="userComments.length === 0" class="empty-minimal">
            <span class="empty-icon-minimal">✍️</span>
            <h3>작성한 리뷰가 없습니다</h3>
          </div>

          <div v-else>
            <div class="compact-header">
              <div class="th-movie">영화</div>
              <div class="th-rating">평점</div>
              <div class="th-content">내용</div>
              <div class="th-date">작성일</div>
              <div class="th-action" v-if="isOwnProfile">관리</div>
            </div>

            <div class="compact-list">
              <article 
                v-for="comment in userComments" 
                :key="comment.id" 
                class="compact-item"
              >
                <div class="td-movie">
                  <button 
                    v-if="comment.movie_id" 
                    @click="handleMovieClick(comment.movie_id)"
                    class="compact-movie-link"
                  >
                    {{ comment.movie_title || '영화 제목' }}
                  </button>
                  <span v-else class="text-gray-500">정보 없음</span>
                </div>

                <div class="td-rating">
                  <div v-if="comment.rating && comment.rating > 0" class="rating-pill">
                    <Star class="icon-xs text-yellow-400 fill-current" />
                    <span>{{ comment.rating }}</span>
                  </div>
                  <span v-else class="text-gray-600">-</span>
                </div>

                <div class="td-content">
                  <p class="compact-text">
                    {{ getReviewContent(comment) || '내용 없음' }}
                  </p>
                  <div v-if="comment.likes_count > 0" class="compact-likes">
                    <Heart class="icon-xs text-red-500 fill-current" />
                    <span>{{ comment.likes_count }}</span>
                  </div>
                </div>

                <div class="td-date">
                  {{ formatDate(comment.created_at) }}
                </div>

                <div class="td-action" v-if="isOwnProfile">
                  <button 
                    @click="handleDeleteReview(comment.id, comment.movie_id)"
                    class="btn-icon-delete"
                    title="리뷰 삭제"
                  >
                    <Trash2 class="icon-sm" />
                  </button>
                </div>
              </article>
            </div>
          </div>
        </div>

      </main>
    </div>

    <ProfileEditModal
      v-if="user"
      :is-open="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @save="handleProfileEdit"
    />

    <FollowListModal
      v-if="user"
      :is-open="showFollowModal"
      :user-id="Number(userId)"
      :type="followModalType"
      :current-user-id="currentUserId"
      @close="handleFollowModalClose"
      @navigate-to-user="handleNavigateToUser"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Star, Film, Heart, MessageSquare, UserPlus, UserCheck, Users, Trash2 } from 'lucide-vue-next';
import StarRating from './StarRating.vue';
import ProfileEditModal from './ProfileEditModal.vue';
import FollowListModal from './FollowListModal.vue';

const router = useRouter();
const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';

interface FollowInfo {
  followers_count: number;
  following_count: number;
  is_following: boolean;
}

interface UserProfile {
  id: number;
  username: string;
  email: string;
  profile_image?: string;
  stats: any;
  follow_info: FollowInfo;
  rated_movies: UserRating[];
  liked_movies: LikedMovie[];
  reviews: UserComment[];
}

interface UserRating {
  id: number;
  movie_id: number;
  title: string;
  poster_path: string;
  rating: number;
}

interface LikedMovie {
  id: number;
  title: string;
  poster_path: string;
  release_date: string;
}

interface UserComment {
  id: number;
  user_id: number;
  username: string;
  rating: number | null;
  comment: string;
  review_content: string;
  created_at: string;
  likes_count: number;
  is_liked: boolean;
  movie_id?: number;
  movie_title?: string;
  movie?: {
    id: number;
    title: string;
  };
}

interface Props {
  userId: number | string;
  currentUserId?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  movieClick: [movieId: number];
  goHome: [];
  updateProfile: [username: string, profileImage: string];
  navigateToUser: [userId: number];
}>();

const handleNavigateToUser = (userId: number) => {
  showFollowModal.value = false;
  router.push({ name: 'UserProfile', params: { userId: userId.toString() } });
};

const handleFollowModalClose = () => {
  showFollowModal.value = false;
  fetchUserProfile();
};

const user = ref<UserProfile | null>(null);
const userRatings = computed(() => user.value?.rated_movies || []);
const likedMovies = computed(() => user.value?.liked_movies || []);
const userComments = computed(() => user.value?.reviews || []);
const isLoading = ref(true);
const error = ref<string | null>(null);

const activeTab = ref<'ratings' | 'likes' | 'comments'>('ratings');
const ratingFilter = ref<'all' | 'high' | 'low'>('all');
const showEditModal = ref(false);

const showFollowModal = ref(false);
const followModalType = ref<'followers' | 'following'>('followers');

const openFollowModal = (type: 'followers' | 'following') => {
  followModalType.value = type;
  showFollowModal.value = true;
};

const isOwnProfile = computed(() => Number(props.userId) === props.currentUserId);

const getFullImageUrl = (path: string | null | undefined): string => {
  if (!path) return '/placeholder-movie.png';
  if (path.startsWith('http')) return path;
  if (path.startsWith('/')) return `${TMDB_IMAGE_BASE_URL}${path}`;
  return `${TMDB_IMAGE_BASE_URL}/${path}`;
};

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/placeholder-movie.png';
};

const fetchUserProfile = async () => {
  const numericUserId = Number(props.userId);
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/users/${numericUserId}/profile/`);
    user.value = response.data;
    if (user.value && !user.value.profile_image) {
      user.value.profile_image = '/mia5.png';  
    }
  } catch (e: any) {
    console.error('Failed to fetch user profile:', e);
    error.value = '사용자 정보를 불러오는 데 실패했습니다.';
    user.value = null;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchUserProfile();
});

const toggleFollow = async () => {
  if (!isOwnProfile.value && user.value) {
    const numericUserId = Number(props.userId);
    try {
      const response = await axios.post(`http://127.0.0.1:8000/users/${numericUserId}/follow/`);
      const { followed } = response.data;
      if (user.value.follow_info) {
        user.value.follow_info.is_following = followed;
        if (followed) {
          user.value.follow_info.followers_count++;
        } else {
          user.value.follow_info.followers_count--;
        }
      }
    } catch (err) {
      console.error("Follow/unfollow failed:", err);
      alert("로그인이 필요합니다.");
    }
  }
};

watch(() => props.userId, () => {
  fetchUserProfile();
});

const handleSaveProfile = (username: string, profileImage: string) => {

  // 2️⃣ 🔥 현재 페이지 즉시 반영
  if (user.value) {
    user.value.username = username;
    user.value.profile_image = profileImage && profileImage.trim()
      ? profileImage
      : '/mia5.png';
  }

  showEditModal.value = false;
};


const handleMovieClick = (movieId: number) => {
  router.push({ name: 'MovieDetail', params: { id: movieId } });
};

const handleDeleteReview = async (reviewId: number, movieId?: number) => {
  if (!confirm('이 리뷰를 삭제하시겠습니까?')) return;
  try {
    await axios.delete(`http://127.0.0.1:8000/movies/${movieId}/rating/`, {
      data: { rating_id: reviewId }
    });
    await fetchUserProfile();
    alert('리뷰가 삭제되었습니다.');
  } catch (error) {
    console.error('Failed to delete review:', error);
    alert('리뷰 삭제에 실패했습니다.');
  }
};

const stats = computed(() => {
  if (user.value && user.value.stats) {
    return {
      total_ratings: user.value.stats.total_ratings || 0,
      avg_rating: user.value.stats.avg_rating || 0,
      liked_movies: user.value.stats.liked_movies || 0,
      total_comments: user.value.stats.total_comments || 0,
    };
  }
  return {
    total_ratings: 0,
    avg_rating: 0,
    liked_movies: 0,
    total_comments: 0,
  };
});

const filteredRatings = computed(() => {
  const ratingsMap = new Map<number, UserRating>();
  userRatings.value.forEach(rating => {
    const existing = ratingsMap.get(rating.movie_id);
    if (!existing || rating.id > existing.id) {
      ratingsMap.set(rating.movie_id, rating);
    }
  });
  const uniqueRatings = Array.from(ratingsMap.values());
  if (ratingFilter.value === 'all') return uniqueRatings;
  if (ratingFilter.value === 'high') return uniqueRatings.filter(r => r.rating >= 4.0);
  if (ratingFilter.value === 'low') return uniqueRatings.filter(r => r.rating <= 2.0);
  return uniqueRatings;
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: '2-digit', month: '2-digit', day: '2-digit'
  });
};

const getReviewContent = (comment: UserComment): string => {
  return comment.comment || comment.review_content || '';
};

const handleProfileEdit = async (username: string, profileImage: string) => {
  try {
    const payload = {
      username,
      profile_image: profileImage && profileImage.trim()
        ? profileImage
        : '/mia5.png',
    };

    const { data } = await axios.patch(
      'http://127.0.0.1:8000/users/me/update/',
      payload
    );

    // 🔥 DB 응답 기준으로 화면 갱신
    if (user.value) {
      user.value.username = data.username;
      user.value.profile_image = data.profile_image || '/mia5.png';
    }

    alert('프로필이 업데이트되었습니다!');
  } catch (error) {
    console.error('Profile update failed', error);
    alert('프로필 업데이트에 실패했습니다.');
  } finally {
    showEditModal.value = false;
  }
};


</script>

<style scoped>
/* 🎨 MIA Design System - Pure Black Cinema Profile */
.profile-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  padding-bottom: 5rem;
}

/* ============ HEADER (UNCHANGED) ============ */
.profile-header {
  padding: 4rem 0 3rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: radial-gradient(circle at 50% 0%, rgba(139, 92, 246, 0.08) 0%, rgba(10, 11, 15, 0) 70%);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  align-items: center;
  gap: 3rem;
}

.profile-avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.profile-avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
}

.avatar-badge {
  position: absolute;
  bottom: 0.5rem;
  right: 0.5rem;
  background: #8b5cf6;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border: 4px solid #0a0b0f;
}

.user-info {
  flex: 1;
}

.user-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: #8b5cf6;
  margin-bottom: 0.5rem;
}

.user-name {
  font-size: 3.5rem;
  font-weight: 300;
  letter-spacing: -0.02em;
  margin: 0 0 0.5rem 0;
  color: #ffffff;
  line-height: 1.1;
}

.user-email {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.4);
  margin-bottom: 2rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.btn-follow {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #8b5cf6;
  color: white;
  border: 1px solid #8b5cf6;
  padding: 0.625rem 1.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-follow:hover {
  background: #7c3aed;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
}

.btn-follow.active {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.8);
  box-shadow: none;
}

.btn-follow.active:hover {
  background: rgba(255, 255, 255, 0.05);
}

.btn-edit {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.625rem 1.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  border-color: rgba(255, 255, 255, 0.4);
  background: rgba(255, 255, 255, 0.03);
}

/* ============ STATS SECTION (UNCHANGED) ============ */
.stats-section {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(10, 11, 15, 0.5);
}

.stats-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  padding: 1.5rem 0;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  position: relative;
  background: none;
  border: none;
  cursor: default;
}

.stat-item.clickable {
  cursor: pointer;
  transition: opacity 0.2s;
}

.stat-item.clickable:hover {
  opacity: 0.8;
}

.stat-item:not(:last-child)::after {
  content: '';
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 50%;
  width: 1px;
  background: rgba(255, 255, 255, 0.06);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 300;
  color: #ffffff;
}

.stat-value.purple { color: #8b5cf6; }
.stat-value.yellow { color: #fbbf24; }
.stat-value.red { color: #f87171; }
.stat-value.blue { color: #60a5fa; }

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

/* ============ FILTER BAR (UNCHANGED) ============ */
.filter-bar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(10, 11, 15, 0.95);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  padding: 1rem 0;
}

.filter-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  justify-content: center;
}

.filter-buttons {
  display: flex;
  gap: 2rem;
}

.filter-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9375rem;
  font-weight: 500;
  padding: 0.5rem 0;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  color: rgba(255, 255, 255, 0.7);
}

.filter-btn.active {
  color: #ffffff;
}

.filter-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1rem;
  left: 0;
  width: 100%;
  height: 2px;
  background: #8b5cf6;
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}

/* ============ MAIN CONTENT ============ */
.content-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 3rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.content-title {
  font-size: 1.5rem;
  font-weight: 300;
  color: #ffffff;
  margin: 0;
}

.content-title .count {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.4);
  margin-left: 0.5rem;
  font-weight: 400;
}

.sub-filters {
  display: flex;
  gap: 0.5rem;
}

.sub-filter-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.375rem 1rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sub-filter-btn.active {
  background: #271a44;
  border-color: #8b5cf6;
  color: white;
}

.sub-filter-btn:hover:not(.active) {
  background: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.8);
}

/* MOVIE GRID (UNCHANGED) */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 2rem;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.poster-wrapper {
  position: relative;
  aspect-ratio: 2/3;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.poster-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.movie-card:hover .poster-wrapper img {
  transform: scale(1.05);
}

.rating-badge, .like-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: #fbbf24;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.like-badge {
  color: #f87171;
}

.movie-title {
  font-size: 0.9375rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 0.25rem 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.movie-card:hover .movie-title {
  color: #8b5cf6;
}

.movie-year {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0;
}

/* ================= COMPACT REVIEW LIST (NEW STYLE) ================= */
.compact-header {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.th-movie { width: 180px; padding-left: 0.5rem; }
.th-rating { width: 60px; text-align: center; }
.th-content { flex: 1; padding-left: 1rem; }
.th-date { width: 100px; text-align: center; }
.th-action { width: 50px; text-align: center; }

.compact-list {
  display: flex;
  flex-direction: column;
}

.compact-item {
  display: flex;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  transition: background 0.2s;
}

.compact-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.td-movie {
  width: 180px;
  padding-left: 0.5rem;
}

.compact-movie-link {
  background: transparent;
  border: none;
  padding: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #8b5cf6;
  cursor: pointer;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  max-width: 100%;
}

.compact-movie-link:hover {
  text-decoration: underline;
}

.td-rating {
  width: 60px;
  display: flex;
  justify-content: center;
}

.rating-pill {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fbbf24;
}

.td-content {
  flex: 1;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  overflow: hidden;
}

.compact-text {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.8);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
  flex: 1;
}

.compact-likes {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #f87171;
  background: rgba(248, 113, 113, 0.1);
  padding: 0.125rem 0.375rem;
  border-radius: 100px;
  flex-shrink: 0;
}

.td-date {
  width: 100px;
  text-align: center;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
}

.td-action {
  width: 50px;
  display: flex;
  justify-content: center;
}

.btn-icon-delete {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  padding: 0.25rem;
  transition: color 0.2s;
}

.btn-icon-delete:hover {
  color: #f87171;
}

/* UTILS (UNCHANGED) */
.icon-xs { width: 14px; height: 14px; }
.icon-sm { width: 18px; height: 18px; }

.loading-minimal, .empty-minimal {
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

.empty-icon-minimal {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  opacity: 0.3;
}

.btn-action-minimal {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* RESPONSIVE */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
  
  .action-buttons {
    justify-content: center;
  }

  .stats-grid {
    flex-wrap: wrap;
    gap: 1.5rem;
  }

  .stat-item {
    min-width: 33%;
  }
  
  .stat-item::after {
    display: none;
  }

  .filter-inner {
    padding: 0 1rem;
    overflow-x: auto;
  }
  
  .filter-buttons {
    gap: 1.5rem;
  }

  .content-main {
    padding: 2rem 1.5rem;
  }

  .movie-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  /* Compact List Mobile */
  .compact-header {
    display: none;
  }

  .compact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 1rem;
  }

  .td-movie, .td-content, .td-date, .td-rating, .td-action {
    width: 100%;
    padding: 0;
    text-align: left;
    justify-content: flex-start;
  }

  .td-content {
    flex-direction: column;
    align-items: flex-start;
    overflow: visible;
  }

  .compact-text {
    white-space: normal;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
}
</style>