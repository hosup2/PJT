<template>
  <div>
    <!-- Comment Input (only for logged in users) -->
    <div v-if="isLoggedIn" class="bg-gray-900 rounded-lg p-6 mb-6">
      <h3 class="text-lg mb-4">리뷰 작성</h3>
      
      <form @submit.prevent="handleSubmitComment">
        <div class="mb-4">
          <StarRating :initial-rating="rating" @change="handleRatingChange" />
        </div>
        <textarea
          v-model="newComment"
          placeholder="이 영화에 대한 리뷰를 작성해주세요..."
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 resize-none focus:outline-none focus:border-purple-500 transition-colors mb-3"
          rows="4"
          required
        />
        
        <div class="flex items-center justify-between">
          <label class="flex items-center gap-2 text-sm text-gray-400 cursor-pointer">
            <input
              v-model="includeSpoiler"
              type="checkbox"
              class="w-4 h-4 rounded border-gray-700 bg-gray-800 text-purple-600 focus:ring-purple-500"
            />
            <span>스포일러 포함</span>
          </label>
          
          <button
            type="submit"
            :disabled="!newComment.trim()"
            class="px-6 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg transition-colors"
          >
            등록
          </button>
        </div>
      </form>
    </div>

    <!-- Login Prompt -->
    <div v-else class="bg-gray-900 rounded-lg p-6 mb-6 text-center">
      <p class="text-gray-400 mb-4">리뷰를 작성하려면 로그인이 필요합니다</p>
      <button
        @click="emit('openAuth')"
        class="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
      >
        로그인
      </button>
    </div>

    <!-- Comments List -->
    <div class="space-y-4">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="bg-gray-900 rounded-lg p-6 hover:bg-gray-850 transition-colors"
      >
        <div class="flex items-start gap-4">
          <button
            @click="emit('navigateToUser', comment.user_id)"
            class="flex-shrink-0"
          >
            <img
              :src="getProfileImage(comment.profile_image)"
              :alt="comment.username"
              class="w-12 h-12 rounded-full bg-gray-800 object-cover hover:ring-2 hover:ring-purple-500 transition-all"
              @error="handleImageError"
            />
          </button>
          
          <div class="flex-1">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-3">
                <button
                  @click="emit('navigateToUser', comment.user_id)"
                  class="font-medium hover:text-purple-400 transition-colors"
                >
                  {{ comment.username }}
                </button>
                <StarRating
                  v-if="comment.rating"
                  :initial-rating="comment.rating"
                  :readonly="true"
                  size="sm"
                />
              </div>
              
              <span class="text-sm text-gray-500">
                {{ formatDate(comment.created_at) }}
              </span>
            </div>

            <div v-if="comment.review_content">
              <button
                v-if="comment.spoiler && !showSpoilers.has(comment.id)"
                @click="toggleSpoiler(comment.id)"
                class="flex items-center gap-2 text-orange-400 hover:text-orange-300 transition-colors"
              >
                <AlertCircle class="w-4 h-4" />
                <span class="text-sm">스포일러가 포함되어 있습니다 (클릭하여 보기)</span>
              </button>
              
              <div v-else>
                <div v-if="comment.spoiler" class="flex items-center gap-2 text-orange-400 text-sm mb-2">
                  <AlertCircle class="w-4 h-4" />
                  <span>스포일러 포함</span>
                </div>
                <p class="text-gray-300 leading-relaxed">
                  {{ comment.review_content }}
                </p>
              </div>
            </div>

            <div class="flex items-center gap-4 mt-3">
              <button
                @click="handleLike(comment.id)"
                :disabled="!isLoggedIn"
                :class="[
                  'flex items-center gap-2 transition-colors',
                  comment.isLiked ? 'text-red-400' : 'text-gray-400',
                  isLoggedIn ? 'hover:text-red-400 cursor-pointer' : 'cursor-not-allowed'
                ]"
              >
                <Heart :class="['w-4 h-4', comment.isLiked && 'fill-current']" />
                <span class="text-sm">{{ comment.likes_count || 0 }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Heart, AlertCircle } from 'lucide-vue-next';
import StarRating from './StarRating.vue';

interface Comment {
  id: number;
  user_id: number;
  movie_id: number;
  rating?: number;
  review_content: string;
  spoiler: boolean;
  created_at: string;
  username: string;
  profile_image: string;
  likes_count: number;
  isLiked: boolean;
}

interface Props {
  comments: Comment[];
  isLoggedIn: boolean;
  rating: number;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  submitComment: [content: string, spoiler: boolean];
  likeComment: [commentId: number];
  navigateToUser: [userId: number];
  openAuth: [];
  ratingChange: [rating: number];
}>();

const newComment = ref('');
const includeSpoiler = ref(false);
const showSpoilers = ref(new Set<number>());

// 👇 프로필 이미지 처리 함수 추가
const getProfileImage = (profileImage: string | null | undefined): string => {
  if (!profileImage) {
    return '/mia5.png'; // 기본 프로필 이미지
  }
  
  // 이미 전체 URL인 경우
  if (profileImage.startsWith('http')) {
    return profileImage;
  }
  
  // 상대 경로인 경우 (/)
  if (profileImage.startsWith('/')) {
    return profileImage;
  }
  
  // 그 외의 경우 (혹시 모를 상황 대비)
  return `/mia5.png`;
};

// 👇 이미지 로딩 에러 처리 함수 추가
const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/mia5.png'; // 에러 발생 시 기본 이미지로 대체
};

const handleRatingChange = (rating: number) => {
  emit('ratingChange', rating);
};

const handleSubmitComment = () => {
  if (newComment.value.trim()) {
    emit('submitComment', newComment.value, includeSpoiler.value);
    newComment.value = '';
    includeSpoiler.value = false;
  }
};

const handleLike = (commentId: number) => {
  emit('likeComment', commentId);
};

const toggleSpoiler = (id: number) => {
  const newSet = new Set(showSpoilers.value);
  if (newSet.has(id)) {
    newSet.delete(id);
  } else {
    newSet.add(id);
  }
  showSpoilers.value = newSet;
};

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffInMs = now.getTime() - date.getTime();
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24));
  
  if (diffInDays === 0) return '오늘';
  if (diffInDays === 1) return '어제';
  if (diffInDays < 7) return `${diffInDays}일 전`;
  if (diffInDays < 30) return `${Math.floor(diffInDays / 7)}주 전`;
  if (diffInDays < 365) return `${Math.floor(diffInDays / 30)}개월 전`;
  return date.toLocaleDateString('ko-KR');
};
</script>