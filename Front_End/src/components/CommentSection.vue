<template>
  <div>
    <div v-if="isLoggedIn" class="comment-input-box" ref="commentFormRef">
      <h3 class="text-lg font-semibold text-white mb-4">{{ editingCommentId ? '리뷰 수정' : '리뷰 작성' }}</h3>
      
      <form @submit.prevent="handleSubmitComment">
        <div class="mb-4">
          <StarRating :initial-rating="currentRating" @change="handleRatingChange" />
        </div>
        <textarea
          v-model="newComment"
          placeholder="이 영화에 대한 리뷰를 작성해주세요..."
          class="custom-textarea"
          rows="4"
          required
        />
        
        <div class="form-footer">
          <label class="spoiler-checkbox">
            <input
              v-model="includeSpoiler"
              type="checkbox"
            />
            <span class="checkbox-label">스포일러 포함</span>
          </label>
          
          <div class="btn-group">
            <button
              v-if="editingCommentId"
              @click="cancelEdit"
              type="button"
              class="btn-cancel"
            >
              취소
            </button>
            <button
              type="submit"
              :disabled="!newComment.trim() || currentRating === 0"
              class="btn-submit"
            >
              {{ editingCommentId ? '수정' : '등록' }}
            </button>   
          </div>
        </div>
      </form>
    </div>

    <div v-else class="comment-input-box text-center">
      <p class="text-gray-400 mb-4">리뷰를 작성하려면 로그인이 필요합니다</p>
      <button
        @click="emit('openAuth')"
        class="btn-submit"
      >
        로그인
      </button>
    </div>

    <!-- 🔥 개별 댓글 - 와이어프레임 스타일로 변경 -->
    <div class="comments-list">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-card"
      >
        <div class="comment-inner">
          <button
            @click="emit('navigateToUser', comment.user_id)"
            class="profile-btn"
          >
            <img
              :src="getProfileImage(comment.profile_image)"
              :alt="comment.username"
              class="profile-image"
              @error="handleImageError"
            />
          </button>
          
          <div class="comment-content">
            <div class="comment-header">
              <div class="user-info">
                <button
                  @click="emit('navigateToUser', comment.user_id)"
                  class="username"
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
              
              <span class="comment-date">
                {{ formatDate(comment.created_at) }}
              </span>
            </div>

            <div v-if="comment.comment" class="comment-body">
              <button
                v-if="comment.spoiler && !showSpoilers.has(comment.id)"
                @click="toggleSpoiler(comment.id)"
                class="spoiler-warning"
              >
                <AlertCircle class="w-4 h-4" />
                <span class="text-sm">스포일러가 포함되어 있습니다 (클릭하여 보기)</span>
              </button>
              
              <div v-else>
                <div v-if="comment.spoiler" class="spoiler-badge">
                  <AlertCircle class="w-4 h-4" />
                  <span>스포일러 포함</span>
                </div>
                <p class="comment-text">
                  {{ comment.comment }}
                </p>
              </div>
            </div>

            <div class="comment-actions">
              <button
                @click="handleLike(comment.id)"
                :disabled="!isLoggedIn"
                :class="[
                  'like-btn',
                  comment.isLiked ? 'liked' : '',
                  !isLoggedIn ? 'disabled' : ''
                ]"
              >
                <Heart :class="['w-4 h-4', comment.isLiked && 'fill-current']" />
                <span class="text-sm">{{ comment.likesCount || 0 }}</span>
              </button>
              
              <div v-if="isOwner(comment.user_id)" class="edit-delete-btns">
                <button
                  @click="startEdit(comment)"
                  class="edit-btn"
                >
                  수정
                </button>
                <button
                  @click="handleDelete(comment.id)"
                  class="delete-btn"
                >
                  삭제
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, inject, type Ref } from 'vue';
import { Heart, AlertCircle } from 'lucide-vue-next';
import StarRating from './StarRating.vue';

interface Comment {
  id: number;
  user_id: number;
  movie_id?: number;
  rating?: number;
  comment: string;
  spoiler?: boolean;
  created_at: string;
  username: string;
  profile_image?: string;
  likesCount?: number;
  isLiked?: boolean;
}

interface Props {
  comments: Comment[];
  isLoggedIn: boolean;
  rating: number;
}

interface User {
  id: number;
  username: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  submitComment: [content: string, rating: number, spoiler: boolean];
  editComment: [commentId: number, content: string, rating: number, spoiler: boolean];
  deleteComment: [commentId: number];
  likeComment: [commentId: number];
  navigateToUser: [userId: number];
  openAuth: [];
  ratingChange: [rating: number];
}>();

const currentUser = inject<Ref<User | null>>('currentUser', ref(null));

const newComment = ref('');
const includeSpoiler = ref(false);
const showSpoilers = ref(new Set<number>());
const currentRating = ref(props.rating);
const editingCommentId = ref<number | null>(null);
const commentFormRef = ref<HTMLElement | null>(null);

watch(() => props.rating, (newVal) => {
  if (!editingCommentId.value) {
    currentRating.value = newVal;
  }
});

const isOwner = (commentUserId: number) => {
  return currentUser.value && currentUser.value.id === commentUserId;
};

const getProfileImage = (profileImage: string | null | undefined): string => {
  if (!profileImage) {
    return '/mia5.png';
  }
  
  if (profileImage.startsWith('http')) {
    return profileImage;
  }
  
  if (profileImage.startsWith('/')) {
    return profileImage;
  }
  
  return `/mia5.png`;
};

const handleImageError = (event: Event) => {
  const target = event.target as HTMLImageElement;
  target.src = '/mia5.png';
};

const handleRatingChange = (rating: number) => {
  console.log('Rating changed in CommentSection:', rating);
  currentRating.value = rating;
  emit('ratingChange', rating);
};

const handleSubmitComment = () => {
  if (!newComment.value.trim()) {
    alert('리뷰 내용을 입력해주세요!');
    return;
  }
  
  if (currentRating.value === 0) {
    alert('평점을 선택해주세요!');
    return;
  }
  
  if (editingCommentId.value) {
    emit('editComment', editingCommentId.value, newComment.value, currentRating.value, includeSpoiler.value);
  } else {
    emit('submitComment', newComment.value, currentRating.value, includeSpoiler.value);
  }
  
  newComment.value = '';
  includeSpoiler.value = false;
  editingCommentId.value = null;
  currentRating.value = props.rating;
};

const startEdit = (comment: Comment) => {
  editingCommentId.value = comment.id;
  newComment.value = comment.comment;
  currentRating.value = comment.rating || 0;
  includeSpoiler.value = comment.spoiler || false;
  commentFormRef.value?.scrollIntoView({
    behavior: 'smooth',
    block: 'center'
  });
};

const cancelEdit = () => {
  editingCommentId.value = null;
  newComment.value = '';
  currentRating.value = props.rating;
  includeSpoiler.value = false;
};

const handleDelete = (commentId: number) => {
  if (confirm('정말 이 리뷰를 삭제하시겠습니까?')) {
    emit('deleteComment', commentId);
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

<style scoped>
/* ✅ Comment Input Box (Wireframe Style) */
.comment-input-box {
  background: transparent;
  border: 3px solid rgba(139, 92, 246, 0.15);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: border-color 0.3s ease;
}

/* ✅ Custom Textarea */
.custom-textarea {
  width: 100%;
  background: transparent;
  border: 1px solid rgba(218, 201, 243, 0.15);
  border-radius: 8px;
  padding: 1rem;
  color: white;
  font-size: 0.95rem;
  resize: none;
  transition: all 0.3s ease;
  margin-bottom: 1rem;
}

.custom-textarea:focus {
  outline: none;
  border-color: rgba(139, 92, 246, 0.5);
  background: rgba(255, 255, 255, 0.02);
}

.custom-textarea::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

/* ✅ Footer Area */
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ✅ Spoiler Checkbox */
.spoiler-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.spoiler-checkbox input {
  appearance: none;
  width: 1rem;
  height: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  background: transparent;
  cursor: pointer;
  position: relative;
  transition: all 0.2s ease;
}

.spoiler-checkbox input:checked {
  background: #8b5cf6;
  border-color: #8b5cf6;
}

.spoiler-checkbox input:checked::after {
  content: '✔';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 0.7rem;
}

.checkbox-label {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

/* ✅ Button Group */
.btn-group {
  display: flex;
  gap: 0.75rem;
}

/* ✅ Cancel Button */
.btn-cancel {
  padding: 0.3rem 1rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
  border-color: rgba(255, 255, 255, 0.4);
}

/* ✅ Submit Button */
.btn-submit {
  padding: 0.3rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
  letter-spacing: 0.02em;
  transition: all 0.2s ease;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-0.5px);
  filter: brightness(1.1);
  background: rgba(139, 92, 246, 0.1);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
}

.btn-submit:disabled {
  background: rgba(55, 65, 81, 0.5);
  color: #9ca3af;
  border-color: rgba(55, 65, 81, 0.5);
  cursor: not-allowed;
  box-shadow: none;
}

/* 🔥 개별 댓글 카드 - 와이어프레임 스타일 */
.comments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-card {
  background: transparent;
  border: 2px solid rgba(139, 92, 246, 0.12);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.comment-inner {
  display: flex;
  gap: 1rem;
}

/* 프로필 이미지 */
.profile-btn {
  flex-shrink: 0;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.profile-image {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  object-fit: cover;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.2);
  transition: all 0.2s ease;
}

.profile-image:hover {
  border-color: rgba(139, 92, 246, 0.5);
  box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
}

/* 댓글 내용 */
.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.username {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: color 0.2s ease;
}

.username:hover {
  color: #a78bfa;
}

.comment-date {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

/* 댓글 본문 */
.comment-body {
  margin-bottom: 0.75rem;
}

.spoiler-warning {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  padding: 0;
  color: #fb923c;
  cursor: pointer;
  transition: color 0.2s ease;
  font-size: 0.875rem;
}

.spoiler-warning:hover {
  color: #fdba74;
}

.spoiler-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #fb923c;
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
}

.comment-text {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
  font-size: 0.95rem;
  margin: 0;
}

/* 댓글 액션 (좋아요, 수정, 삭제) */
.comment-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  padding: 0;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: color 0.2s ease;
}

.like-btn:hover:not(.disabled) {
  color: #ef4444;
}

.like-btn.liked {
  color: #ef4444;
}

.like-btn.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* 수정/삭제 버튼 */
.edit-delete-btns {
  display: flex;
  gap: 0.75rem;
  margin-left: auto;
}

.edit-btn,
.delete-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: color 0.2s ease;
}

.edit-btn:hover {
  color: #a78bfa;
}

.delete-btn:hover {
  color: #ef4444;
}
</style>