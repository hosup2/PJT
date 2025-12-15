<template>
  <div>
    <!-- User not found message -->
    <div v-if="!user" class="flex items-center justify-center min-h-[400px]">
      <div class="text-center">
        <p class="text-xl text-gray-400 mb-2">😥 사용자를 찾을 수 없습니다</p>
        <p class="text-sm text-gray-500 mb-6">프로필 정보를 불러올 수 없습니다.</p>
        <button
          @click="emit('goHome')"
          class="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
        >
          홈으로 돌아가기
        </button>
      </div>
    </div>

    <!-- Profile content -->
    <div v-if="user">
      <!-- Profile Header -->
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-6 md:p-8 mb-8 border border-gray-700/50">
        <!-- Profile Info Section -->
        <div class="flex flex-col items-center text-center mb-8">
          <!-- Profile Image -->
          <div class="relative mb-4">
            <img
              :src="user.profile_image"
              :alt="user.username"
              class="w-24 h-24 md:w-32 md:h-32 rounded-full bg-gray-800 object-cover ring-4 ring-purple-500/20"
            />
            <div class="absolute -bottom-2 -right-2 bg-purple-600 rounded-full p-2">
              <Star class="w-4 h-4 md:w-5 md:h-5 text-white fill-white" />
            </div>
          </div>
          
          <!-- Username & Follow Button -->
          <h1 class="text-4xl md:text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
            {{ user.username }}
          </h1>
          
          <p class="text-gray-400 mb-4">{{ user.email }}</p>
          
          <button
            v-if="!isOwnProfile"
            @click="toggleFollow"
            :class="[
              'px-6 py-2 rounded-full text-sm font-semibold transition-all duration-200 flex items-center gap-2 shadow-lg',
              user.follow_info.is_following
                ? 'bg-gray-700 text-gray-300 hover:bg-gray-600 hover:shadow-gray-600/50'
                : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 hover:shadow-purple-500/50'
            ]"
          >
            <UserCheck v-if="user.follow_info.is_following" class="w-4 h-4" />
            <UserPlus v-else class="w-4 h-4" />
            <span>{{ user.follow_info.is_following ? '팔로잉' : '팔로우' }}</span>
          </button>
        </div>
        
        <!-- Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 md:gap-4 max-w-5xl mx-auto">
          <!-- Followers -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-emerald-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-emerald-500/20">
                <Users class="w-5 h-5 text-emerald-400" />
              </div>
              <span class="text-2xl font-bold text-emerald-400">{{ user.follow_info.followers_count }}</span>
              <p class="text-xs text-gray-400">팔로워</p>
            </div>
          </div>
          
          <!-- Following -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-emerald-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-emerald-500/20">
                <UserCheck class="w-5 h-5 text-emerald-400" />
              </div>
              <span class="text-2xl font-bold text-emerald-400">{{ user.follow_info.following_count }}</span>
              <p class="text-xs text-gray-400">팔로잉</p>
            </div>
          </div>

          <!-- Rated Movies -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-purple-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-purple-500/20">
                <Film class="w-5 h-5 text-purple-400" />
              </div>
              <span class="text-2xl font-bold text-purple-400">{{ stats.total_ratings }}</span>
              <p class="text-xs text-gray-400">평가</p>
            </div>
          </div>
          
          <!-- Average Rating -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-yellow-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-yellow-500/20">
                <Star class="w-5 h-5 text-yellow-400 fill-yellow-400" />
              </div>
              <span class="text-2xl font-bold text-yellow-400">{{ stats.avg_rating.toFixed(1) }}</span>
              <p class="text-xs text-gray-400">평균</p>
            </div>
          </div>
          
          <!-- Likes -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-red-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-red-500/20">
                <Heart class="w-5 h-5 text-red-400" />
              </div>
              <span class="text-2xl font-bold text-red-400">{{ stats.liked_movies }}</span>
              <p class="text-xs text-gray-400">좋아요</p>
            </div>
          </div>
          
          <!-- Reviews -->
          <div class="bg-gray-800/50 rounded-xl p-4 backdrop-blur-sm border border-gray-700/30 hover:border-blue-500/50 transition-all duration-200 hover:scale-105">
            <div class="flex flex-col items-center gap-2">
              <div class="flex items-center justify-center w-10 h-10 rounded-full bg-blue-500/20">
                <MessageSquare class="w-5 h-5 text-blue-400" />
              </div>
              <span class="text-2xl font-bold text-blue-400">{{ stats.total_comments }}</span>
              <p class="text-xs text-gray-400">리뷰</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-2 mb-6 border-b border-gray-800">
        <button
          @click="activeTab = 'ratings'"
          :class="[
            'px-4 py-3 transition-colors relative',
            activeTab === 'ratings' ? 'text-purple-400' : 'text-gray-400 hover:text-gray-200'
          ]"
        >
          평가한 영화
          <div
            v-if="activeTab === 'ratings'"
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-400"
          />
        </button>
        
        <button
          @click="activeTab = 'likes'"
          :class="[
            'px-4 py-3 transition-colors relative',
            activeTab === 'likes' ? 'text-purple-400' : 'text-gray-400 hover:text-gray-200'
          ]"
        >
          좋아요한 영화
          <div
            v-if="activeTab === 'likes'"
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-400"
          />
        </button>
        
        <button
          @click="activeTab = 'comments'"
          :class="[
            'px-4 py-3 transition-colors relative',
            activeTab === 'comments' ? 'text-purple-400' : 'text-gray-400 hover:text-gray-200'
          ]"
        >
          작성한 리뷰
          <div
            v-if="activeTab === 'comments'"
            class="absolute bottom-0 left-0 right-0 h-0.5 bg-purple-400"
          />
        </button>
      </div>

      <!-- Ratings Tab -->
      <div v-if="activeTab === 'ratings'">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl">평가한 영화 ({{ filteredRatings.length }})</h2>
          
          <div class="flex gap-2">
            <button
              @click="ratingFilter = 'all'"
              :class="[
                'px-4 py-2 rounded-lg transition-colors',
                ratingFilter === 'all'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              ]"
            >
              전체
            </button>
            <button
              @click="ratingFilter = 'high'"
              :class="[
                'px-4 py-2 rounded-lg transition-colors',
                ratingFilter === 'high'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              ]"
            >
              4점 이상
            </button>
            <button
              @click="ratingFilter = 'low'"
              :class="[
                'px-4 py-2 rounded-lg transition-colors',
                ratingFilter === 'low'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              ]"
            >
              2점 이하
            </button>
          </div>
        </div>

        <div v-if="filteredRatings.length === 0" class="text-center py-12 text-gray-400">
          평가한 영화가 없습니다
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <div v-for="rating in filteredRatings" :key="rating.id" class="group">
            <button
              @click="handleMovieClick(rating.movie_id)"
              class="w-full text-left"
            >
              <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
                <img
                  :src="getFullImageUrl(rating.poster_path)"
                  :alt="rating.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform"
                  @error="handleImageError"
                />
              </div>
              
              <div class="flex items-center gap-2 mb-1">
                <StarRating
                  :initial-rating="rating.rating"
                  :readonly="true"
                  size="sm"
                />
              </div>
              
              <h3 class="line-clamp-2 text-sm group-hover:text-purple-400 transition-colors">
                {{ rating.title }}
              </h3>
            </button>
          </div>
        </div>
      </div>

      <!-- Likes Tab -->
      <div v-if="activeTab === 'likes'">
        <h2 class="text-2xl mb-6">좋아요한 영화 ({{ likedMovies.length }})</h2>
        
        <div v-if="likedMovies.length === 0" class="text-center py-12 text-gray-400">
          좋아요한 영화가 없습니다
        </div>

        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <div v-for="movie in likedMovies" :key="movie.id" class="group">
            <button
              @click="handleMovieClick(movie.id)"
              class="w-full text-left"
            >
              <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
                <img
                  :src="getFullImageUrl(movie.poster_path)"
                  :alt="movie.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform"
                  @error="handleImageError"
                />
                <div class="absolute top-3 right-3">
                  <Heart class="w-5 h-5 text-red-400 fill-current" />
                </div>
              </div>
              
              <h3 class="line-clamp-2 text-sm group-hover:text-purple-400 transition-colors">
                {{ movie.title }}
              </h3>
              
              <p class="text-xs text-gray-500 mt-1">
                {{ new Date(movie.release_date).getFullYear() }}
              </p>
            </button>
          </div>
        </div>
      </div>

      <!-- Comments Tab -->
      <div v-if="activeTab === 'comments'">
        <h2 class="text-2xl mb-6">작성한 리뷰 ({{ userComments.length }})</h2>
        
        <div v-if="userComments.length === 0" class="text-center py-12 text-gray-400">
          작성한 리뷰가 없습니다
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="comment in userComments"
            :key="comment.id"
            class="bg-gray-900/50 rounded-xl p-6 border border-gray-800 hover:border-purple-500/30 transition-all"
          >
            <!-- Header: Movie Title, Rating, Date, Delete Button -->
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <!-- Movie Title - Clickable -->
                <button
                  v-if="comment.movie_id"
                  @click="handleMovieClick(comment.movie_id)"
                  class="text-xl font-bold hover:text-purple-400 transition-colors mb-2 text-left block hover:underline"
                >
                  {{ comment.movie_title || '영화 제목' }}
                </button>
                
                <!-- Fallback if no movie info -->
                <div v-else class="text-xl font-bold text-gray-500 mb-2">
                  {{ comment.movie_title || '영화 정보 없음' }}
                </div>
                
                <!-- Rating if exists -->
                <div v-if="comment.rating && comment.rating > 0" class="flex items-center gap-2 mb-2">
                  <StarRating
                    :initial-rating="comment.rating"
                    :readonly="true"
                    size="sm"
                  />
                  <span class="text-sm text-yellow-400 font-semibold">{{ comment.rating.toFixed(1) }}점</span>
                </div>
              </div>
              
              <div class="flex items-center gap-3 ml-4">
                <span class="text-sm text-gray-500 whitespace-nowrap">
                  {{ formatDate(comment.created_at) }}
                </span>
                
                <!-- Delete Button - Only show for own profile -->
                <button
                  v-if="isOwnProfile"
                  @click="handleDeleteReview(comment.id, comment.movie_id)"
                  class="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                  title="리뷰 삭제"
                >
                  <Trash2 class="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <!-- Review Content -->
            <div v-if="getReviewContent(comment)" class="bg-gray-800/30 rounded-lg p-4 mb-4">
              <p class="text-gray-200 leading-relaxed whitespace-pre-wrap text-base">
                {{ getReviewContent(comment) }}
              </p>
            </div>
            <div v-else class="bg-gray-800/30 rounded-lg p-4 mb-4">
              <p class="text-gray-500 italic text-sm">
                리뷰 내용이 없습니다.
              </p>
            </div>
            
            <!-- Footer: Likes -->
            <div class="flex items-center gap-2 pt-2">
              <Heart 
                class="w-5 h-5 transition-colors" 
                :class="comment.likes_count > 0 ? 'fill-current text-red-500' : 'text-gray-600'" 
              />
              <span 
                class="text-sm font-medium" 
                :class="comment.likes_count > 0 ? 'text-red-500' : 'text-gray-600'"
              >
                좋아요 {{ comment.likes_count }}개
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Edit Modal -->
    <ProfileEditModal
      v-if="user"
      :is-open="showEditModal"
      :user="user"
      @close="showEditModal = false"
      @save="handleSaveProfile"
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

const router = useRouter();

// TMDB Image Base URL
const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500';

// Type definitions based on backend serializers
interface FollowInfo {
  followers_count: number;
  following_count: number;
  is_following: boolean;
}

interface UserProfile {
  id: number;
  username: string;
  email: string; // Note: email might not be public
  profile_image?: string;
  stats: any; // Define stats structure later
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
  // These fields should come from backend but might be missing
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
  emit('navigateToUser', userId);
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

const isOwnProfile = computed(() => Number(props.userId) === props.currentUserId);

// Helper function to get full image URL
const getFullImageUrl = (path: string | null | undefined): string => {
  if (!path) {
    return '/placeholder-movie.png'; // Fallback image
  }
  
  // If path already starts with http, return as is
  if (path.startsWith('http')) {
    return path;
  }
  
  // If path starts with /, it's already a TMDB path
  if (path.startsWith('/')) {
    return `${TMDB_IMAGE_BASE_URL}${path}`;
  }
  
  // Otherwise, assume it needs the base URL
  return `${TMDB_IMAGE_BASE_URL}/${path}`;
};

// Handle image loading errors
const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/placeholder-movie.png'; // Set fallback image
};

const fetchUserProfile = async () => {
  const numericUserId = Number(props.userId);
  console.log('Fetching profile for userId:', numericUserId);
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/users/${numericUserId}/profile/`);
    user.value = response.data;
    
    // Debug logging
    console.log('User profile data:', response.data);
    console.log('Reviews data:', response.data.reviews);
    console.log('Number of reviews:', response.data.reviews?.length || 0);
    
    // Debug each review to see structure
    if (response.data.reviews && response.data.reviews.length > 0) {
      const firstReview = response.data.reviews[0];
      console.log('First review structure:', firstReview);
      console.log('First review keys:', Object.keys(firstReview));
      console.log('Movie title attempt 1 (movie?.title):', firstReview.movie?.title);
      console.log('Movie title attempt 2 (movie_title):', firstReview.movie_title);
      console.log('Movie title attempt 3 (title):', firstReview.title);
      console.log('Content attempt 1 (content):', firstReview.content);
      console.log('Content attempt 2 (comment):', firstReview.comment);
      console.log('Content attempt 3 (review_content):', firstReview.review_content);
    }
  } catch (e: any) {
    console.error('Failed to fetch user profile:', e);
    error.value = '사용자 정보를 불러오는 데 실패했습니다.';
    user.value = null;
    if (e.response?.data) {
      console.log('Error response:', e.response.data);
    }
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
      alert("요청을 처리할 수 없습니다.");
    }
  }
};

watch(() => props.userId, () => {
  fetchUserProfile();
});


const handleSaveProfile = (username: string, profileImage: string) => {
  emit('updateProfile', username, profileImage);
  showEditModal.value = false;
};

const handleMovieClick = (movieId: number) => {
  router.push({ name: 'MovieDetail', params: { id: movieId } });
};

const handleDeleteReview = async (reviewId: number, movieId?: number) => {
  if (!confirm('이 리뷰를 삭제하시겠습니까?')) {
    return;
  }

  try {
    // rating_id를 body에 포함해서 전송
    await axios.delete(`http://127.0.0.1:8000/movies/${movieId}/rating/`, {
      data: { rating_id: reviewId }
    });
    
    // Refresh user profile data
    await fetchUserProfile();
    
    alert('리뷰가 삭제되었습니다.');
  } catch (error) {
    console.error('Failed to delete review:', error);
    alert('리뷰 삭제에 실패했습니다.');
  }
};

// This computed property will now be empty as we are not using mock data
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

// Filtered ratings based on selected filter
const filteredRatings = computed(() => {
  if (ratingFilter.value === 'all') return userRatings.value;
  if (ratingFilter.value === 'high') return userRatings.value.filter(r => r.rating >= 4.0);
  if (ratingFilter.value === 'low') return userRatings.value.filter(r => r.rating <= 2.0);
  return userRatings.value;
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR');
};

// Helper function to get review content - backend sends 'comment' and 'review_content' (they're the same)
const getReviewContent = (comment: UserComment): string => {
  return comment.comment || comment.review_content || '';
};
</script>