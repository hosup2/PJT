<template>
  <div v-if="user">
    <!-- Profile Header -->
    <div class="bg-gray-900 rounded-lg p-8 mb-8">
      <div class="flex items-start gap-6">
        <img
          :src="user.profile_image"
          :alt="user.username"
          class="w-24 h-24 rounded-full bg-gray-800 object-cover"
        />
        
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
              <div class="flex items-center gap-2 text-green-400 mb-1">
                <TrendingUp class="w-5 h-5" />
                <span class="text-2xl">{{ stats.high_ratings }}</span>
              </div>
              <p class="text-sm text-gray-400">4점 이상</p>
            </div>
            
            <div>
              <div class="flex items-center gap-2 text-red-400 mb-1">
                <Heart class="w-5 h-5" />
                <span class="text-2xl">{{ stats.low_ratings }}</span>
              </div>
              <p class="text-sm text-gray-400">2점 이하</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Taste Analysis -->
    <div class="bg-gray-900 rounded-lg p-6 mb-8">
      <h2 class="text-xl mb-4">취향 분석</h2>
      
      <div class="mb-6">
        <h3 class="text-sm text-gray-400 mb-3">선호하는 장르</h3>
        <div class="flex flex-wrap gap-2">
          <div
            v-for="genre in taste.favoriteGenres"
            :key="genre.genre"
            class="px-4 py-2 bg-purple-900/30 border border-purple-700 rounded-full"
          >
            <span class="mr-2">{{ genre.genre }}</span>
            <span class="text-sm text-gray-400">
              {{ genre.count }}편 · ⭐{{ genre.avg_rating.toFixed(1) }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-6 border-t border-gray-800 pt-6">
        <div>
          <p class="text-sm text-gray-400 mb-1">평가 성향</p>
          <p class="text-lg">
            {{ taste.tendency.isStrict ? '까다로운 편' : '관대한 편' }}
          </p>
        </div>
        
        <div>
          <p class="text-sm text-gray-400 mb-1">긍정 평가 비율</p>
          <p class="text-lg">{{ (taste.tendency.positiveRatio * 100).toFixed(0) }}%</p>
        </div>
        
        <div>
          <p class="text-sm text-gray-400 mb-1">평균 평점</p>
          <div class="flex items-center gap-2">
            <Star class="w-5 h-5 text-yellow-400 fill-yellow-400" />
            <span class="text-lg">{{ taste.tendency.avgRating.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Ratings Filter -->
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl">평가한 영화</h2>
      
      <div class="flex gap-2">
        <button
          @click="filter = 'all'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            filter === 'all'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          전체
        </button>
        <button
          @click="filter = 'high'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            filter === 'high'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          4점 이상
        </button>
        <button
          @click="filter = 'low'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            filter === 'low'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          2점 이하
        </button>
        <button
          @click="filter = 'recent'"
          :class="[
            'px-4 py-2 rounded-lg transition-colors',
            filter === 'recent'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
          ]"
        >
          최근 30일
        </button>
      </div>
    </div>

    <!-- User Ratings Grid -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      <div v-for="rating in filteredRatings" :key="rating.id" class="group">
        <div class="relative aspect-[2/3] rounded-lg overflow-hidden mb-3 bg-gray-800">
          <img
            :src="rating.poster_path"
            :alt="rating.title"
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
            <div class="absolute bottom-3 left-3 right-3">
              <StarRating
                :initial-rating="rating.rating"
                :readonly="true"
                size="sm"
              />
              <p class="text-xs text-gray-300 mt-2">
                {{ new Date(rating.watched_at).toLocaleDateString('ko-KR') }}
              </p>
            </div>
          </div>
        </div>
        
        <div class="flex items-center gap-2 mb-1">
          <StarRating
            :initial-rating="rating.rating"
            :readonly="true"
            size="sm"
          />
        </div>
        
        <h3 class="line-clamp-2 text-sm">{{ rating.title }}</h3>
        
        <p v-if="rating.review_content" class="text-xs text-gray-500 mt-1 line-clamp-2">
          {{ rating.review_content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Star, Film, Heart, TrendingUp } from 'lucide-vue-next';
import { mockUsers, mockUserRatings, mockUserStats, mockUserTaste } from '../data/mockData';
import StarRating from './StarRating.vue';

interface Props {
  userId: number;
}

const props = defineProps<Props>();

const filter = ref<'all' | 'high' | 'low' | 'recent'>('all');

const user = computed(() => mockUsers.find(u => u.id === props.userId));
const stats = mockUserStats;
const taste = mockUserTaste;

const filteredRatings = computed(() => {
  return mockUserRatings.filter(rating => {
    if (filter.value === 'all') return true;
    if (filter.value === 'high') return rating.rating >= 4.0;
    if (filter.value === 'low') return rating.rating <= 2.0;
    if (filter.value === 'recent') {
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      return new Date(rating.watched_at) >= thirtyDaysAgo;
    }
    return true;
  });
});
</script>
