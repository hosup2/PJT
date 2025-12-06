<template>
  <!-- 로봇 애니메이션 - 오른쪽 하단 (전체 화면 기준)
  <div class="animate-float" style="position: fixed; bottom: 32px; right: 32px; z-index: 50;">
    <img src="/mia.png" alt="MIA 로봇" style="height: 100px; width: auto;" class="drop-shadow-2xl cursor-pointer hover:scale-110 transition-transform" />
  </div> -->

  <div class="hero-section relative overflow-hidden">
    <!-- 배경 그라데이션 -->
    <div class="absolute inset-0 bg-gradient-to-br from-purple-900/50 via-gray-900 to-blue-900/50"></div>
    
    <!-- 애니메이션 배경 -->
    <div class="absolute inset-0 opacity-20">
      <div class="absolute top-20 left-20 w-72 h-72 bg-purple-500 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-20 right-20 w-96 h-96 bg-blue-500 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>
    </div>

    <!-- 컨텐츠 -->
    <div class="relative container mx-auto px-6 py-20 max-w-7xl">
      <div class="text-center max-w-4xl mx-auto">
        <!-- 메인 헤딩 -->
        <h1 class="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent">
          당신만을 위한<br />영화 추천
        </h1>

        <!-- 서브 헤딩 -->
        <p class="text-xl md:text-2xl text-gray-300 mb-12 leading-relaxed">
          AI가 분석하는 개인화된 영화 경험<br />
          <span class="text-purple-400">취향 저격 영화</span>를 지금 바로 만나보세요
        </p>

        <!-- CTA 버튼들 -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <button 
            class="px-8 py-4 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 text-white rounded-full text-lg font-semibold shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 hover:scale-105 transition-all duration-200 flex items-center gap-2"
          >
            <Play class="w-6 h-6" />
            영화 탐색 시작하기
          </button>
          
          <button 
            class="px-8 py-4 bg-white/10 backdrop-blur-sm hover:bg-white/20 text-white rounded-full text-lg font-semibold border border-white/20 hover:border-white/40 transition-all duration-200 flex items-center gap-2"
          >
            <Sparkles class="w-6 h-6" />
            AI 추천받기
          </button>
        </div>

        <!-- 통계 카드 -->
        <!-- <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all duration-200 hover:scale-105">
            <div class="text-4xl font-bold text-purple-400 mb-2">10,000+</div>
            <div class="text-gray-300">등록된 영화</div>
          </div>
          
          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all duration-200 hover:scale-105">
            <div class="text-4xl font-bold text-blue-400 mb-2">50,000+</div>
            <div class="text-gray-300">사용자 리뷰</div>
          </div>
          
          <div class="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all duration-200 hover:scale-105">
            <div class="text-4xl font-bold text-yellow-400 mb-2 flex items-center justify-center gap-2">
              <Star class="w-8 h-8 fill-yellow-400" />
              4.8
            </div>
            <div class="text-gray-300">평균 평점</div>
          </div>
        </div> -->
        <br>
      </br>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Play, Sparkles, Star } from 'lucide-vue-next';
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>