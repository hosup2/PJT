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
            <h1 class="text-3xl mb-2">{{ user.username }}</h1>
            <p class="text-gray-400 mb-4">{{ user.email }}</p>
            
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
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
import { ref, computed } from 'vue';
import { Star, Film, Heart, MessageSquare, Edit } from 'lucide-vue-next';
import { mockUsers, mockUserRatings, mockLikedMovies, mockUserComments } from '../data/mockData';
import StarRating from './StarRating.vue';
import ProfileEditModal from './ProfileEditModal.vue';

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

const activeTab = ref<'ratings' | 'likes' | 'comments'>('ratings');
const ratingFilter = ref<'all' | 'high' | 'low'>('all');
const showEditModal = ref(false);

// Find user
const user = computed(() => {
  const foundUser = mockUsers.find(u => u.id === props.userId);
  console.log('UserProfile - Looking for user with ID:', props.userId);
  console.log('UserProfile - Found user:', foundUser);
  console.log('UserProfile - All users:', mockUsers);
  return foundUser;
});

const isOwnProfile = computed(() => props.userId === props.currentUserId);

const handleSaveProfile = (username: string, profileImage: string) => {
  emit('updateProfile', username, profileImage);
  showEditModal.value = false;
};

// Calculate stats
const stats = computed(() => {
  const ratings = mockUserRatings.length;
  const avgRating = ratings > 0 
    ? mockUserRatings.reduce((sum, r) => sum + r.rating, 0) / ratings 
    : 0;

  return {
    total_ratings: ratings,
    avg_rating: avgRating,
    high_ratings: mockUserRatings.filter(r => r.rating >= 4.0).length,
    low_ratings: mockUserRatings.filter(r => r.rating <= 2.0).length,
    liked_movies: mockLikedMovies.length,
    total_comments: mockUserComments.length
  };
});

// Filtered ratings based on selected filter
const filteredRatings = computed(() => {
  if (ratingFilter.value === 'all') return mockUserRatings;
  if (ratingFilter.value === 'high') return mockUserRatings.filter(r => r.rating >= 4.0);
  if (ratingFilter.value === 'low') return mockUserRatings.filter(r => r.rating <= 2.0);
  return mockUserRatings;
});

const likedMovies = mockLikedMovies;
const userComments = mockUserComments;

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ko-KR');
};
</script>