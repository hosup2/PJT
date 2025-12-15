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
      <div class="bg-gray-900 rounded-lg p-8 mb-8">
        <div class="flex items-start gap-6">
          <div class="relative">
            <img
              :src="user.profile_image"
              :alt="user.username"
              class="w-24 h-24 rounded-full bg-gray-800 object-cover"
            />
          </div>
          
          <div class="flex-1">
            <div class="flex items-center gap-4 mb-4">
              <h1 class="text-3xl">{{ user.username }}</h1>
              <button
                v-if="!isOwnProfile"
                @click="toggleFollow"
                :class="[
                  'px-4 py-1.5 rounded-lg text-sm font-semibold transition-all duration-200 flex items-center gap-2',
                  user.follow_info.is_following
                    ? 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    : 'bg-purple-600 text-white hover:bg-purple-500'
                ]"
              >
                <UserCheck v-if="user.follow_info.is_following" class="w-4 h-4" />
                <UserPlus v-else class="w-4 h-4" />
                <span>{{ user.follow_info.is_following ? '팔로잉' : '팔로우' }}</span>
              </button>
            </div>
            <p class="text-gray-400 mb-6">{{ user.email }}</p>
            
            <div class="grid grid-cols-3 md:grid-cols-6 gap-6">
              <!-- Follower/Following Stats -->
              <div>
                <div class="flex items-center gap-2 text-green-400 mb-1">
                  <Users class="w-5 h-5" />
                  <span class="text-2xl">{{ user.follow_info.followers_count }}</span>
                </div>
                <p class="text-sm text-gray-400">팔로워</p>
              </div>
              <div>
                <div class="flex items-center gap-2 text-green-400 mb-1">
                  <UserCheck class="w-5 h-5" />
                  <span class="text-2xl">{{ user.follow_info.following_count }}</span>
                </div>
                <p class="text-sm text-gray-400">팔로잉</p>
              </div>

              <!-- Other Stats -->
              <div>
                <div class="flex items-center gap-2 text-purple-400 mb-1">
                  <Film class="w-5 h-5" />
                  <span class="text-2xl">{{ stats.total_ratings }}</span>
                </div>
                <p class="text-sm text-gray-400">평가한 영화</p>
              </div>
              
              <div>
                <div class="flex items-center gap-2 text-yellow-400 mb-1">
                  <Star class="w-5 h-5" />
                  <span class="text-2xl">{{ stats.avg_rating.toFixed(1) }}</span>
                </div>
                <p class="text-sm text-gray-400">평균 평점</p>
              </div>
              
              <div>
                <div class="flex items-center gap-2 text-red-400 mb-1">
                  <Heart class="w-5 h-5" />
                  <span class="text-2xl">{{ stats.liked_movies }}</span>
                </div>
                <p class="text-sm text-gray-400">좋아요</p>
              </div>
              
              <div>
                <div class="flex items-center gap-2 text-blue-400 mb-1">
                  <MessageSquare class="w-5 h-5" />
                  <span class="text-2xl">{{ stats.total_comments }}</span>
                </div>
                <p class="text-sm text-gray-400">리뷰</p>
              </div>
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
              @click="emit('movieClick', rating.movie_id)"
              class="w-full text-left"
            >
              <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
                <img
                  :src="rating.poster_path"
                  :alt="rating.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform"
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
              @click="emit('movieClick', movie.id)"
              class="w-full text-left"
            >
              <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
                <img
                  :src="movie.poster_path"
                  :alt="movie.title"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform"
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
            class="bg-gray-900 rounded-lg p-6"
          >
            <div class="flex items-start gap-4 mb-4">
              <button
                @click="emit('movieClick', comment.movie_id)"
                class="flex-shrink-0"
              >
                <img
                  :src="comment.movie_poster"
                  :alt="comment.movie_title"
                  class="w-16 h-24 rounded object-cover hover:ring-2 hover:ring-purple-500 transition-all"
                />
              </button>
              
              <div class="flex-1">
                <button
                  @click="emit('movieClick', comment.movie_id)"
                  class="text-lg hover:text-purple-400 transition-colors mb-2"
                >
                  {{ comment.movie_title }}
                </button>
                
                <div class="flex items-center gap-3 mb-3">
                  <StarRating
                    v-if="comment.rating"
                    :initial-rating="comment.rating"
                    :readonly="true"
                    size="sm"
                  />
                  <span class="text-sm text-gray-500">
                    {{ formatDate(comment.created_at) }}
                  </span>
                </div>
                
                <p class="text-gray-300 leading-relaxed">
                  {{ comment.content }}
                </p>
                
                <div class="flex items-center gap-2 mt-3 text-gray-400">
                  <Heart class="w-4 h-4" />
                  <span class="text-sm">{{ comment.likes_count }}</span>
                </div>
              </div>
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
import axios from 'axios';
import { Star, Film, Heart, MessageSquare, UserPlus, UserCheck, Users } from 'lucide-vue-next';
import StarRating from './StarRating.vue';
import ProfileEditModal from './ProfileEditModal.vue';

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
  movie_id: number;
  movie_title: string;
  movie_poster: string;
  rating: number | null;
  content: string;
  created_at: string;
  likes_count: number;
}

interface Props {
  userId: number;
  currentUserId?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  movieClick: [movieId: number];
  goHome: [];
  updateProfile: [username: string, profileImage: string];
}>();

const user = ref<UserProfile | null>(null);
const userRatings = ref<UserRating[]>([]);
const likedMovies = ref<LikedMovie[]>([]);
const userComments = ref<UserComment[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

const activeTab = ref<'ratings' | 'likes' | 'comments'>('ratings');
const ratingFilter = ref<'all' | 'high' | 'low'>('all');
const showEditModal = ref(false);

const isOwnProfile = computed(() => Number(props.userId) === props.currentUserId);

const fetchUserProfile = async () => {
  console.log('Fetching profile for userId:', props.userId); // Diagnostic log
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/users/${props.userId}/profile/`);
    user.value = response.data;
  } catch (e) {
    console.error('Failed to fetch user profile:', e);
    error.value = '사용자 정보를 불러오는 데 실패했습니다.';
    user.value = null;
  } finally {
    isLoading.value = false;
  }
};

// Fetch other user data (ratings, comments, etc.)
const fetchUserActivity = async () => {
  // Placeholder for fetching other data - implement later
  // For now, clear mock data
  userRatings.value = [];
  likedMovies.value = [];
  userComments.value = [];
};

onMounted(() => {
  fetchUserProfile();
  fetchUserActivity();
});

const toggleFollow = async () => {
  if (!isOwnProfile.value && user.value) {
    try {
      const response = await axios.post(`http://127.0.0.1:8000/users/${props.userId}/follow/`);
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
  fetchUserActivity();
});


const handleSaveProfile = (username: string, profileImage: string) => {
  emit('updateProfile', username, profileImage);
  showEditModal.value = false;
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
</script>