<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl">평가 ({{ ratings.length }})</h2>
      
      <div class="flex gap-2">
        <button
          @click="sortBy = 'recent'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            sortBy === 'recent'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          최신순
        </button>
        <button
          @click="sortBy = 'high'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            sortBy === 'high'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          높은 평점
        </button>
        <button
          @click="sortBy = 'low'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            sortBy === 'low'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          낮은 평점
        </button>
      </div>
    </div>

    <div class="space-y-4">
      <div
        v-for="rating in sortedRatings"
        :key="rating.id"
        class="bg-gray-900 rounded-lg p-6 hover:bg-gray-850 transition-colors"
      >
        <div class="flex items-start gap-4">
          <img
            :src="rating.profile_image"
            :alt="rating.username"
            class="w-12 h-12 rounded-full bg-gray-800 object-cover"
          />
          
          <div class="flex-1">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-3">
                <span class="font-medium">{{ rating.username }}</span>
                <StarRating
                  :initial-rating="rating.rating"
                  :readonly="true"
                  size="sm"
                />
              </div>
              
              <span class="text-sm text-gray-500">
                {{ new Date(rating.watched_at).toLocaleDateString('ko-KR') }}
              </span>
            </div>

            <div v-if="rating.review_content" class="mt-3">
              <button
                v-if="rating.spoiler && !showSpoilers.has(rating.id)"
                @click="toggleSpoiler(rating.id)"
                class="flex items-center gap-2 text-orange-400 hover:text-orange-300 transition-colors"
              >
                <AlertCircle class="w-4 h-4" />
                <span class="text-sm">스포일러가 포함되어 있습니다 (클릭하여 보기)</span>
              </button>
              
              <div v-else>
                <div v-if="rating.spoiler" class="flex items-center gap-2 text-orange-400 text-sm mb-2">
                  <AlertCircle class="w-4 h-4" />
                  <span>스포일러 포함</span>
                </div>
                <p class="text-gray-300 leading-relaxed">
                  {{ rating.review_content }}
                </p>
              </div>
            </div>

            <div 
              v-if="rating.likes_count !== undefined && rating.likes_count > 0"
              class="flex items-center gap-2 mt-3 text-gray-400"
            >
              <Heart class="w-4 h-4" />
              <span class="text-sm">{{ rating.likes_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Heart, AlertCircle } from 'lucide-vue-next';
import StarRating from './StarRating.vue';

interface Rating {
  id: number;
  user_id: number;
  movie_id: number;
  rating: number;
  watched_at: string;
  username: string;
  profile_image: string;
  review_content?: string;
  spoiler?: boolean;
  likes_count?: number;
}

interface Props {
  ratings: Rating[];
}

const props = defineProps<Props>();

const sortBy = ref<'recent' | 'high' | 'low'>('recent');
const showSpoilers = ref(new Set<number>());

const sortedRatings = computed(() => {
  const ratings = [...props.ratings];
  
  return ratings.sort((a, b) => {
    if (sortBy.value === 'recent') {
      return new Date(b.watched_at).getTime() - new Date(a.watched_at).getTime();
    } else if (sortBy.value === 'high') {
      return b.rating - a.rating;
    } else {
      return a.rating - b.rating;
    }
  });
});

const toggleSpoiler = (id: number) => {
  const newSet = new Set(showSpoilers.value);
  if (newSet.has(id)) {
    newSet.delete(id);
  } else {
    newSet.add(id);
  }
  showSpoilers.value = newSet;
};
</script>
