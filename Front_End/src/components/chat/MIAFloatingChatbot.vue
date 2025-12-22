<template>
  <div
    style="
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 9999;
      pointer-events: auto;
    "
  >
    <div style="display: flex; align-items: flex-end; gap: 8px;">
      <!-- 💬 말풍선 -->
      <transition name="chat-pop">
        <div
          v-if="open"
          style="
            width: 400px;
            height: 400px;
            background: #111827;
            border: 1px solid rgba(147,51,234,0.3);
            border-radius: 12px;
            padding: 10px;
            font-size: 12px;
            box-shadow: 0 20px 25px rgba(0,0,0,0.5);
            position: relative;
            display: flex;
            flex-direction: column;
            transform-origin: bottom right;
          "
        >
          <!-- 꼬리 -->
          <div
            style="
              position: absolute;
              right: -6px;
              bottom: 18px;
              width: 10px;
              height: 10px;
              background: #111827;
              border-right: 1px solid rgba(147,51,234,0.3);
              border-bottom: 1px solid rgba(147,51,234,0.3);
              transform: rotate(45deg);
            "
          />

          <!-- 헤더 -->
          <div
            style="
              display: flex;
              justify-content: space-between;
              align-items: center;
              padding: 2px 8px;
              margin-bottom: 4px;
            "
          >
            <!-- 타이틀 -->
            <strong
              style="
                color: #c084fc;
                font-size: 14px;
                letter-spacing: 0.5px;
              "
            >
              MIA
            </strong>

            <!-- 버튼 영역 -->
            <div style="display:flex; gap:8px;">
              <!-- 새 대화 -->
              <button
                @click="startNewChat"
                title="새 대화"
                style="
                  width: 32px;
                  height: 32px;
                  border-radius: 8px;
                  background: #1f2937;
                  color: #22c55e;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  font-size: 16px;
                  cursor: pointer;
                "
              >
                ＋
              </button>

              <!-- 세션 목록 -->
              <button
                @click="() => {
                  showSessions = !showSessions
                  if (showSessions) fetchSessions()
                }"
                title="대화 목록"
                style="
                  width: 32px;
                  height: 32px;
                  border-radius: 8px;
                  background: #1f2937;
                  color: #e5e7eb;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  font-size: 14px;
                  cursor: pointer;
                "
              >
                ☰
              </button>

              <!-- 세션 삭제 -->
              <button
                v-if="sessionId"
                @click="deleteSession"
                title="대화 삭제"
                style="
                  width: 32px;
                  height: 32px;
                  border-radius: 8px;
                  background: #1f2937;
                  color: #ef4444;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  font-size: 14px;
                  cursor: pointer;
                "
              >
                🗑
              </button>
            </div>
          </div>


          <!-- ✅ 세션 목록 패널 (여기!!) -->
          <div
            v-if="showSessions"
            style="
              position: absolute;
              top: 40px;
              left: -180px;
              width: 170px;
              height: calc(100% - 50px);
              background: #020617;
              border: 1px solid rgba(147,51,234,0.3);
              border-radius: 12px;
              padding: 6px;
              overflow-y: auto;
              z-index: 20;
            "
          >
            <div
              v-for="s in sessions"
              :key="s.id"
              @click="loadSession(s.id)"
              style="
                padding: 6px;
                font-size: 11px;
                cursor: pointer;
                border-radius: 6px;
                margin-bottom: 4px;
                color: #e5e7eb;
              "
              @mouseover="($event.currentTarget as HTMLElement).style.background='#1f2937'"
              @mouseleave="($event.currentTarget as HTMLElement).style.background='transparent'"
            >
              {{ s.title || '대화 ' + s.id }}
            </div>
          </div>

          <!-- 메시지 영역 -->
          <div
            ref="messageArea"
            style="
              flex: 1;
              overflow-y: auto;
              margin-bottom: 6px;
              padding-right: 4px;
            "
          >
            <div
              v-for="(msg, i) in messages"
              :key="i"
              style="margin-bottom: 8px;"
            >
              <!-- 💬 말풍선 -->
              <div
                :style="{
                  textAlign: msg.role === 'assistant' ? 'left' : 'right'
                }"
              >
                <span
                  :style="{
                    display: 'inline-block',
                    padding: '6px 8px',
                    borderRadius: '8px',
                    background: msg.role === 'assistant' ? '#1f2937' : '#7c3aed',
                    color: '#fff',
                    maxWidth: '90%'
                  }"
                >
                  {{ msg.content }}
                </span>
              </div>

              <!-- 🎬 추천 영화 카드 (assistant일 때만) -->
              <div
                v-if="msg.role === 'assistant' && msg.movies && msg.movies.length"
                style="margin-top: 6px;"
              >
                <div
                  v-for="movie in msg.movies"
                  :key="movie.movie_id"
                  style="
                    background: #111827;
                    border: 1px solid rgba(147,51,234,0.3);
                    border-radius: 8px;
                    padding: 8px;
                    margin-bottom: 6px;
                  "
                >
                  <!-- 카드 클릭 영역 -->
                  <div @click="goToMovie(movie.movie_id)" style="cursor:pointer;">
                    <div style="font-weight: 600; color: #c084fc;">
                      🎬 {{ movie.title }}
                    </div>

                    <div
                      v-if="movie.reason"
                      style="font-size: 11px; color: #9ca3af; margin-top: 2px;"
                    >
                      {{ movie.reason }}
                    </div>

                    <div style="font-size: 10px; color: #7c3aed; margin-top: 4px;">
                      상세 페이지로 이동 →
                    </div>
                  </div>

                  <!-- 👍 👎 피드백 버튼 -->
                  <div
                    style="
                      display: flex;
                      gap: 8px;
                      margin-top: 6px;
                      justify-content: flex-end;
                    "
                  >
                    <button
                      @click.stop="sendFeedback(movie.movie_id, 'like')"
                      style="
                        background: #1f2937;
                        border-radius: 6px;
                        padding: 4px 8px;
                        font-size: 11px;
                        color: #22c55e;
                        cursor: pointer;
                      "
                    >
                      👍 좋아요
                    </button>

                    <button
                      @click.stop="sendFeedback(movie.movie_id, 'dislike')"
                      style="
                        background: #1f2937;
                        border-radius: 6px;
                        padding: 4px 8px;
                        font-size: 11px;
                        color: #ef4444;
                        cursor: pointer;
                      "
                    >
                      👎 싫어요
                    </button>
                  </div>
                </div>

              </div>
            </div>


            <!-- 로딩 표시 -->
            <div v-if="loading" style="text-align:left;">
              <span
                style="
                  display:inline-block;
                  padding:6px 8px;
                  border-radius:8px;
                  background:#1f2937;
                  color:#9ca3af;
                "
              >
                MIA가 생각 중{{ loadingDots }}
              </span>
            </div>
          </div>

          <!-- 입력 영역 -->
          <form
            @submit.prevent="send"
            style="
              display:flex;
              gap:6px;
              border-top: 1px solid rgba(147,51,234,0.2);
              padding-top: 6px;
            "
          >
            <input
              v-model="input"
              :disabled="!isLoggedIn || loading"
              :placeholder="isLoggedIn ? '영화 추천…' : '로그인 후 이용해주세요'"
              @click="!isLoggedIn && handleLoginClick()"
              style="
                flex:1;
                background:#1f2937;
                border-radius:8px;
                padding:6px 8px;
                font-size:12px;
                outline:none;
                color:white;
              "
            />

            <button
              type="submit"
              :disabled="!isLoggedIn || loading"
              :style="{
                background:'#7c3aed',
                borderRadius:'8px',
                padding:'6px 10px',
                fontSize:'11px',
                color:'white',
                whiteSpace:'nowrap',
                opacity: (!isLoggedIn || loading) ? 0.5 : 1,
                cursor: (!isLoggedIn || loading) ? 'not-allowed' : 'pointer'
              }"
            >
              전송
            </button>
          </form>
        </div>
      </transition>

      <!-- 🤖 로봇 -->
      <img
        src="/mia.png"
        alt="MIA"
        class="mia-float"
        style="
          height: 120px;
          width: auto;
          cursor: pointer;
          filter: drop-shadow(0 8px 12px rgba(0,0,0,0.6));
        "
        @click="open = !open"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, nextTick, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import type { Ref } from 'vue';
const router = useRouter();

const goToMovie = (movieId: number) => {
  router.push({
    name: 'MovieDetail',
    params: { id: movieId },
  });
};


const isLoggedIn = inject<Ref<boolean>>('isLoggedIn', ref(false));
const openAuthModal = inject<() => void>('openAuthModal');

const SESSION_KEY = 'mia_chat_session_id';

const sessionId = ref<number | null>(
  localStorage.getItem(SESSION_KEY)
    ? Number(localStorage.getItem(SESSION_KEY))
    : null
);

const open = ref(false);
const loading = ref(false);
const input = ref('');
const messageArea = ref<HTMLElement | null>(null);
const loadingDots = ref('');

interface MovieRecommendation {
  movie_id: number;
  title: string;
  reason?: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  movies?: MovieRecommendation[];
}

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: isLoggedIn
      ? '안녕하세요! 어떤 영화를 추천해드릴까요? 🎬'
      : '로그인 후 MIA의 영화 추천을 이용할 수 있어요 😊',
  },
]);

const scrollToBottom = async () => {
  await nextTick();
  if (messageArea.value) {
    messageArea.value.scrollTop = messageArea.value.scrollHeight;
  }
};

watch(messages, scrollToBottom, { deep: true });

let dotTimer: number | null = null;
watch(loading, (val) => {
  if (val) {
    dotTimer = window.setInterval(() => {
      loadingDots.value =
        loadingDots.value.length >= 3 ? '' : loadingDots.value + '.';
    }, 400);
  } else {
    if (dotTimer) clearInterval(dotTimer);
    loadingDots.value = '';
  }
});

const handleLoginClick = () => {
  if (messages.value.at(-1)?.content.includes('로그인')) return;

  messages.value.push({
    role: 'assistant',
    content: '로그인이 필요해요! 로그인 후 다시 말씀해 주세요 🔐',
  });

  openAuthModal && openAuthModal();
};

const send = async () => {

  if (!isLoggedIn) {
    handleLoginClick();
    return;
  }

  if (!input.value.trim() || loading.value) return;

  const userMessage = input.value;
  input.value = '';

  messages.value.push({ role: 'user', content: userMessage });
  loading.value = true;

  const token = localStorage.getItem('accessToken');

  try {
    const res = await axios.post(
      'http://127.0.0.1:8000/recommend/chat/',
      {
        message: userMessage.trim(),
        session_id: sessionId.value ?? null,
      },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
    );

    const data = res.data;

    if (data.session_id && !sessionId.value) {
      sessionId.value = data.session_id;
      localStorage.setItem(SESSION_KEY, String(data.session_id));
    }

    messages.value.push({
      role: 'assistant',
      content: data.answer,
      movies: data.movies || [],
    });

  } catch {
    messages.value.push({
      role: 'assistant',
      content: '추천 중 문제가 발생했어요 😥 잠시 후 다시 시도해주세요.',
    });
  } finally {
    loading.value = false;
  }
};

const sessions = ref<any[]>([]);
const showSessions = ref(false);

const fetchSessions = async () => {
  const res = await axios.get(
    'http://127.0.0.1:8000/recommend/sessions/',
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    }
  );
  sessions.value = res.data;
};

const loadSession = async (id: number) => {
  const res = await axios.get(
    `http://127.0.0.1:8000/recommend/sessions/${id}/`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    }
  );

  sessionId.value = id;
  messages.value = res.data.messages.map((m: any) => ({
    role: m.role,
    content: m.content,
  }));

  // showSessions.value = false;
};

const deleteSession = async () => {
  if (!sessionId.value) return;

  await axios.delete(
    `http://127.0.0.1:8000/recommend/sessions/${sessionId.value}/`,
    {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      },
    }
  );

  sessionId.value = null;
  messages.value = [
    { role: 'assistant', content: '새 대화를 시작해볼까요? 😊' },
  ];

  fetchSessions();
};

watch(open, (v) => {
  if (v) fetchSessions();
});

const startNewChat = () => {
  // 현재 세션 초기화
  sessionId.value = null;
  localStorage.removeItem(SESSION_KEY);

  // 메시지 초기화
  messages.value = [
    {
      role: 'assistant',
      content: '새 대화를 시작했어요 😊 무엇을 도와드릴까요?',
    },
  ];

  showSessions.value = false;
};

const sendFeedback = async (
  movieId: number,
  feedback: 'like' | 'dislike'
) => {
  try {
    await axios.post(
      'http://127.0.0.1:8000/recommend/feedback/',
      {
        movie_id: movieId,
        feedback,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        },
      }
    );

    // 🔥 여기서 바로 UI 반영
    if (feedback === 'dislike') {
      removeMovieFromUI(movieId);
    }

    messages.value.push({
      role: 'assistant',
      content:
        feedback === 'like'
          ? '👍 반영했어요! 비슷한 취향으로 추천할게요.'
          : '👎 알겠어요! 이 영화는 추천에서 제외할게요.',
    });

  } catch {
    messages.value.push({
      role: 'assistant',
      content: '피드백 저장 중 문제가 생겼어요 😥',
    });
  }
};

const removeMovieFromUI = (movieId: number) => {
  // 마지막 assistant 메시지 기준으로 제거
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const msg = messages.value[i];

    if (msg.role === 'assistant' && msg.movies) {
      msg.movies = msg.movies.filter(
        (m) => m.movie_id !== movieId
      );
      break;
    }
  }
};


const resetChatbot = () => {
  sessionId.value = null;
  localStorage.removeItem(SESSION_KEY);

  messages.value = [
    {
      role: 'assistant',
      content: isLoggedIn
        ? '안녕하세요! 어떤 영화를 추천해드릴까요? 🎬'
        : '로그인 후 MIA의 영화 추천을 이용할 수 있어요 😊',
    },
  ];

  showSessions.value = false;
};

watch(isLoggedIn!, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    resetChatbot();
  }
});


const logout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');

  resetChatbot(); // ⭐ 반드시 호출
};


</script>

<style scoped>
@keyframes mia-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.mia-float {
  animation: mia-float 3s ease-in-out infinite;
}

.chat-pop-enter-active,
.chat-pop-leave-active {
  transition: all 0.2s ease;
}

.chat-pop-enter-from,
.chat-pop-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(8px);
}
</style>
