<template>
  <!-- 영화 캐러셀 히어로 섹션 - 화면 전체를 차지 -->
  <div class="hero-carousel-wrapper" style="position: relative; width: 100%; height: 100vh; overflow: hidden; background-color: #000; margin: 0; padding: 0;">
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
            <div style="position: relative; height: 100%; width: 100%; max-width: none;">
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
              <p
                style="font-size: 1.25rem; color: rgb(209, 213, 219);
                margin-bottom: 0.75rem; line-height: 1.75; max-width: 36rem;"
              >
                {{ getDisplayDescription(movie) }}
              </p>

              <!-- 더보기 / 접기 -->
              <button
                v-if="movie.description.length > MAX_DESC_LENGTH"
                @click="toggleExpand(movie.id)"
                style="color: rgb(147, 51, 234); font-size: 0.9rem; font-weight: 500;
                background: none; border: none; cursor: pointer; margin-bottom: 2rem;"
              >
                {{ isExpanded(movie.id) ? '접기' : '줄거리' }}
              </button>


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
import { useRouter } from 'vue-router';
import { Play, Star, ChevronLeft, ChevronRight } from 'lucide-vue-next';
import axios from 'axios';

interface HeroMovie {
  id: number;
  title: string;
  description: string;
  backdrop: string;
  badge: string;
  rating: string;
  year: string;
  genre: string;
  duration: string;
}

const featuredMovies = ref<HeroMovie[]>([]);

const fetchHeroMovies = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/movies/hero/');

    featuredMovies.value = res.data.map((item: any) => {
      const movie = item.movie;

      return {
        id: movie.id,
        title: movie.title,
        description: movie.overview,
        backdrop: movie.backdrops?.startsWith('http')
          ? movie.backdrops
          : `https://image.tmdb.org/t/p/original${movie.backdrops}`,
        badge: item.keyword || '',
        rating: movie.tmdb_rating?.toFixed(1) ?? '0.0',
        year: movie.release_date?.slice(0, 4) ?? '',
        genre: movie.genres.join(', '),
        duration: movie.runtime ? `${movie.runtime}분` : ''
      };
    });
  } catch (e) {
    console.error('Failed to fetch hero movies', e);
  }
};


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

const playMovie = async (movie: HeroMovie) => {
  try {
    const res = await axios.get(
      `https://api.themoviedb.org/3/movie/${movie.tmdb_id}/videos`,
      {
        params: {
          api_key: import.meta.env.VITE_TMDB_API_KEY,
          language: 'ko-KR'
        }
      }
    );

    const videos = res.data.results || [];

    // 유튜브 트레일러 우선
    const trailer = videos.find(
      (v: any) => v.site === 'YouTube' && v.type === 'Trailer'
    );

    if (trailer) {
      window.open(
        `https://www.youtube.com/watch?v=${trailer.key}`,
        '_blank'
      );
    } else {
      // 트레일러 없으면 상세 페이지로
      showDetails(movie);
    }
  } catch (e) {
    console.error('트레일러 로드 실패', e);
    showDetails(movie);
  }
};

const showDetails = (movie: HeroMovie) => {
  router.push({
    name: 'MovieDetail',
    params: { id: movie.id }
  });
};


onMounted(async () => {
  await fetchHeroMovies();

  if (featuredMovies.value.length > 0) {
    currentSlide.value = 1;
    startAutoSlide();
  }
});


onUnmounted(() => {
  stopAutoSlide();
});

const MAX_DESC_LENGTH = 120;

const expandedSet = ref<Set<number>>(new Set());

const isExpanded = (movieId: number) => {
  return expandedSet.value.has(movieId);
};

const toggleExpand = (movieId: number) => {
  if (expandedSet.value.has(movieId)) {
    expandedSet.value.delete(movieId);
  } else {
    expandedSet.value.add(movieId);
  }
};

const getDisplayDescription = (movie: HeroMovie) => {
  if (movie.description.length <= MAX_DESC_LENGTH) {
    return movie.description;
  }

  if (isExpanded(movie.id)) {
    return movie.description;
  }

  return movie.description.slice(0, MAX_DESC_LENGTH) + '...';
};

const router = useRouter();

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