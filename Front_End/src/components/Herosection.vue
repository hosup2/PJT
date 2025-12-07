<template>
  <!-- 영화 캐러셀 히어로 섹션 - 화면 전체를 차지 -->
  <div class="hero-carousel-wrapper" style="position: relative; width: 100vw; height: 100vh; overflow: hidden; background-color: #000; margin: 0; padding: 0;">
    <div class="hero-carousel group" style="position: relative; width: 100%; height: 100%; overflow: hidden;">
      <!-- 캐러셀 컨테이너 -->
      <div 
        ref="carouselTrack"
        class="carousel-track"
        :style="{ 
          display: 'flex',
          height: '100%',
          transform: `translateX(-${currentSlide * 100}%)`,
          transition: isTransitioning ? 'transform 0.7s ease-out' : 'none',
          willChange: 'transform'
        }"
        @transitionend="handleTransitionEnd"
      >
        <!-- 각 영화 슬라이드 -->
        <div 
          v-for="(movie, index) in displayMovies" 
          :key="`movie-${index}`"
          class="carousel-slide"
          style="min-width: 100%; width: 100%; height: 100%; flex-shrink: 0; position: relative;"
        >
          <!-- 영화 배경 이미지 -->
          <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; overflow: hidden;">
            <div style="position: relative; height: 100%; width: 250%; max-width: none;">
              <img 
                :src="movie.backdrop" 
                :alt="movie.title"
                style="width: 100%; height: 100%; object-fit: cover;"
              />
              <!-- 그라데이션 오버레이 -->
              <div style="position: absolute; inset: 0; background: linear-gradient(to right, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.5) 50%, transparent 100%);"></div>
              <div style="position: absolute; inset: 0; background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 50%, transparent 100%);"></div>
            </div>
          </div>

          <!-- 영화 정보 -->
          <div style="position: relative; height: 100%; max-width: 1280px; margin: 0 auto; padding: 0 3rem; display: flex; align-items: center;">
            <div style="max-width: 42rem;">
              <!-- 배지 -->
              <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <span style="padding: 0.25rem 0.75rem; background-color: rgb(147, 51, 234); color: white; font-size: 0.875rem; font-weight: 600; border-radius: 9999px;">
                  {{ movie.badge }}
                </span>
                <div style="display: flex; align-items: center; gap: 0.25rem; color: rgb(250, 204, 21);">
                  <Star class="w-5 h-5 fill-yellow-400" style="width: 1.25rem; height: 1.25rem; fill: currentColor;" />
                  <span style="color: white; font-weight: 600;">{{ movie.rating }}</span>
                </div>
              </div>

              <!-- 제목 -->
              <h2 style="font-size: 4.5rem; font-weight: 700; color: white; margin-bottom: 1rem; line-height: 1.1; text-shadow: 0 10px 15px rgba(0,0,0,0.5);">
                {{ movie.title }}
              </h2>

              <!-- 설명 -->
              <p style="font-size: 1.25rem; color: rgb(209, 213, 219); margin-bottom: 2rem; line-height: 1.75; max-width: 36rem;">
                {{ movie.description }}
              </p>

              <!-- 메타 정보 -->
              <div style="display: flex; align-items: center; gap: 1rem; color: rgb(156, 163, 175); margin-bottom: 2rem;">
                <span>{{ movie.year }}</span>
                <span>•</span>
                <span>{{ movie.genre }}</span>
                <span>•</span>
                <span>{{ movie.duration }}</span>
              </div>

              <!-- 버튼들 -->
              <div style="display: flex; gap: 1rem;">
                <button 
                  @click="playMovie(movie)"
                  style="padding: 1rem 2rem; background-color: white; color: black; border-radius: 9999px; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 10px 15px rgba(0,0,0,0.3); cursor: pointer; border: none; transition: all 0.2s;"
                  @mouseover="$event.target.style.backgroundColor = 'rgb(229, 231, 235)'"
                  @mouseout="$event.target.style.backgroundColor = 'white'"
                >
                  <Play style="width: 1.25rem; height: 1.25rem; fill: black;" />
                  재생하기
                </button>
                
                <button 
                  @click="showDetails(movie)"
                  style="padding: 1rem 2rem; background-color: rgba(255,255,255,0.2); backdrop-filter: blur(8px); color: white; border-radius: 9999px; font-weight: 600; border: 1px solid rgba(255,255,255,0.3); display: flex; align-items: center; gap: 0.5rem; cursor: pointer; transition: all 0.2s;"
                  @mouseover="$event.target.style.backgroundColor = 'rgba(255,255,255,0.3)'"
                  @mouseout="$event.target.style.backgroundColor = 'rgba(255,255,255,0.2)'"
                >
                  상세정보
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 네비게이션 버튼 -->
      <button 
        @click="manualPrev"
        class="nav-btn-left"
        style="position: absolute; left: 2rem; top: 50%; transform: translateY(-50%); width: 3rem; height: 3rem; background-color: rgba(0,0,0,0.5); backdrop-filter: blur(8px); border-radius: 9999px; display: flex; align-items: center; justify-content: center; color: white; z-index: 10; opacity: 0; cursor: pointer; border: none; transition: all 0.2s;"
      >
        <ChevronLeft style="width: 1.5rem; height: 1.5rem;" />
      </button>
      
      <button 
        @click="manualNext"
        class="nav-btn-right"
        style="position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); width: 3rem; height: 3rem; background-color: rgba(0,0,0,0.5); backdrop-filter: blur(8px); border-radius: 9999px; display: flex; align-items: center; justify-content: center; color: white; z-index: 10; opacity: 0; cursor: pointer; border: none; transition: all 0.2s;"
      >
        <ChevronRight style="width: 1.5rem; height: 1.5rem;" />
      </button>

      <!-- 인디케이터 -->
      <div style="position: absolute; bottom: 2rem; left: 50%; transform: translateX(-50%); display: flex; gap: 0.5rem; z-index: 10;">
        <button
          v-for="(_, index) in featuredMovies"
          :key="`indicator-${index}`"
          @click="goToSlide(index)"
          :style="{
            transition: 'all 0.2s',
            width: getActualIndex() === index ? '2rem' : '0.5rem',
            height: '0.5rem',
            backgroundColor: getActualIndex() === index ? 'white' : 'rgba(255,255,255,0.5)',
            borderRadius: '9999px',
            cursor: 'pointer',
            border: 'none'
          }"
        ></button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { Play, Star, ChevronLeft, ChevronRight } from 'lucide-vue-next';

const featuredMovies = ref([
  { id: 1, title: '인터스텔라', description: '우주를 가로지르는 장대한 모험. 인류의 생존을 위해 새로운 행성을 찾아 떠나는 우주비행사들의 이야기', backdrop: 'https://image.tmdb.org/t/p/original/vgnoBSVzWAV9sNQUORaDGvDp7wx.jpg', badge: '지금 인기', rating: '8.6', year: '2014', genre: 'SF, 드라마', duration: '169분' },
  { id: 2, title: '기생충', description: '전원 백수인 기택 가족이 IT기업 CEO 박사장의 가족에게 접근하면서 벌어지는 이야기', backdrop: 'https://image.tmdb.org/t/p/w1280/ApiBzeaa95TNYliSbQ8pJv4Fje7.jpg', badge: '오스카 수상', rating: '8.5', year: '2019', genre: '드라마, 스릴러', duration: '132분' },
  { id: 3, title: '덩케르크', description: '제2차 세계대전 당시 덩케르크 해변에서 벌어진 역사상 가장 위대한 구출 작전', backdrop: 'https://image.tmdb.org/t/p/original/ddIkmH3TpR6XSc47jj0BrGK5Rbz.jpg', badge: '화제의 작품', rating: '7.9', year: '2017', genre: '전쟁, 액션', duration: '106분' },
  { id: 4, title: '조커', description: '1980년대 고담시를 배경으로 한 아서 플렉의 광기 어린 변신', backdrop: 'https://image.tmdb.org/t/p/original/hO7KbdvGOtDdeg0W4Y5nKEHeDDh.jpg', badge: '평론가 극찬', rating: '8.4', year: '2019', genre: '범죄, 드라마', duration: '122분' },
  { id: 5, title: '블레이드 러너 2049', description: '2049년, 새로운 블레이드 러너 K가 30년 전 사라진 릭 데커드를 찾아 나서는 이야기', backdrop: 'https://image.tmdb.org/t/p/original/mVr0UiqyltcfqxbAUcLl9zWL8ah.jpg', badge: '시각적 걸작', rating: '8.0', year: '2017', genre: 'SF, 스릴러', duration: '164분' }
]);

const carouselTrack = ref<HTMLElement | null>(null);
const isTransitioning = ref(false);
const totalMovies = computed(() => featuredMovies.value.length);

const displayMovies = computed(() => {
  if (totalMovies.value === 0) return [];
  const first = featuredMovies.value[0];
  const last = featuredMovies.value[totalMovies.value - 1];
  return [last, ...featuredMovies.value, first];
});

const currentSlide = ref(1);
let autoSlideInterval: number | null = null;

const getActualIndex = () => {
  if (currentSlide.value === 0) return totalMovies.value - 1;
  if (currentSlide.value === totalMovies.value + 1) return 0;
  return currentSlide.value - 1;
};

const slideTo = (index: number) => {
  isTransitioning.value = true;
  currentSlide.value = index;
};

const nextSlide = () => {
  slideTo(currentSlide.value + 1);
};

const prevSlide = () => {
  slideTo(currentSlide.value - 1);
};

const handleTransitionEnd = () => {
  isTransitioning.value = false;
  if (currentSlide.value === 0) {
    currentSlide.value = totalMovies.value;
  } else if (currentSlide.value === totalMovies.value + 1) {
    currentSlide.value = 1;
  }
};

const manualNext = () => {
  if (isTransitioning.value) return;
  stopAutoSlide();
  nextSlide();
  startAutoSlide();
};

const manualPrev = () => {
  if (isTransitioning.value) return;
  stopAutoSlide();
  prevSlide();
  startAutoSlide();
};

const goToSlide = (index: number) => {
  if (isTransitioning.value) return;
  stopAutoSlide();
  slideTo(index + 1);
  startAutoSlide();
};

const startAutoSlide = () => {
  stopAutoSlide();
  autoSlideInterval = window.setInterval(() => {
    nextSlide();
  }, 5000);
};

const stopAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval);
    autoSlideInterval = null;
  }
};

const playMovie = (movie: any) => console.log('재생:', movie.title);
const showDetails = (movie: any) => console.log('상세정보:', movie.title);

onMounted(() => {
  currentSlide.value = 1;
  startAutoSlide();
});

onUnmounted(() => {
  stopAutoSlide();
});
</script>

<style scoped>
.hero-carousel:hover .nav-btn-left,
.hero-carousel:hover .nav-btn-right {
  opacity: 1 !important;
}

.nav-btn-left:hover,
.nav-btn-right:hover {
  background-color: rgba(0,0,0,0.7) !important;
}

@media (max-width: 768px) {
  .hero-carousel-wrapper h2 {
    font-size: 3rem !important;
  }
}
</style>