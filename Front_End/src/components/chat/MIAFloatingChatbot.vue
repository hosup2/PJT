<template>
  <div class="chatbot-wrapper">
    <div class="chatbot-layout">
      
      <transition name="chat-pop">
        <div v-if="open" ref="chatWindow" class="chat-window">
          
          <div class="chat-tail"></div>

          <header class="chat-header">
            <div class="header-title">
              <span class="logo-text">MIA AI</span>
              <span class="status-dot"></span>
            </div>

            <div class="header-actions">
              <button @click="startNewChat" class="action-btn" title="새 대화">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
              </button>

              <button 
                @click="() => { showSessions = !showSessions; if (showSessions) fetchSessions(); }"
                class="action-btn" 
                title="대화 목록"
              >
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
              </button>

              <button v-if="sessionId" @click="deleteSession" class="action-btn delete" title="대화 삭제">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </header>

          <transition name="slide-fade">
            <div v-if="showSessions" class="session-panel">
              <div class="session-header">지난 대화</div>
              <div class="session-list-scroll">
                <div
                  v-for="s in sessions"
                  :key="s.id"
                  @click="loadSession(s.id)"
                  class="session-item"
                >
                  
                  <span class="session-title">{{ s.title || '대화 ' + s.id }}</span>
                </div>
              </div>
            </div>
          </transition>

          <div ref="messageArea" class="messages-area">
            <div v-for="(msg, i) in messages" :key="i" class="message-row" :class="msg.role">
              
              <div class="bubble">
                {{ msg.content }}
              </div>

              <div v-if="msg.role === 'assistant' && msg.movies && msg.movies.length" class="cards-container">
                <div 
                  v-for="movie in msg.movies" 
                  :key="movie.movie_id" 
                  class="movie-card"
                >
                  <div @click="goToMovie(movie.movie_id)" class="card-content">
                    <div class="card-header">
                      <span class="movie-icon">🎬</span>
                      <span class="movie-title">{{ movie.title }}</span>
                    </div>
                    <p v-if="movie.reason" class="movie-reason">{{ movie.reason }}</p>
                    <div class="link-text">상세 페이지로 이동 →</div>
                  </div>

                  <div class="card-actions">
                    <button @click.stop="sendFeedback(movie.movie_id, 'like')" class="card-btn like">
                      👍 좋아요
                    </button>
                    <button @click.stop="sendFeedback(movie.movie_id, 'dislike')" class="card-btn dislike">
                      👎 싫어요
                    </button>
                  </div>
                </div>
              </div>

            </div>

            <div v-if="loading" class="message-row assistant">
              <div class="bubble loading">
                <span class="dot"></span><span class="dot"></span><span class="dot"></span>
              </div>
            </div>
          </div>

          <form @submit.prevent="send" class="input-area">
            <input
              v-model="input"
              :disabled="!isLoggedIn || loading"
              :placeholder="isLoggedIn ? '영화 추천을 부탁해보세요...' : '로그인이 필요합니다'"
              @click="!isLoggedIn && handleLoginClick()"
              class="chat-input"
            />
            <button 
              type="submit" 
              :disabled="!isLoggedIn || loading"
              class="send-btn"
            >
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7"/>
              </svg>
            </button>
          </form>

        </div>
      </transition>

      <img
        ref="robotButton"
        src="/mia.png"
        alt="MIA"
        class="mia-float"
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
import { onMounted, onBeforeUnmount } from 'vue'

// 챗봇 화면 밖 클릭시 닫힘 + ESC로 닫기
const chatWindow = ref<HTMLElement | null>(null);
const robotButton = ref<HTMLElement | null>(null);

const toggleChat = () => {
  open.value = !open.value;
};

const handleClickOutside = (event: MouseEvent) => {
  if (!open.value) return;

  const target = event.target as Node;

  // 1️⃣ 채팅창 내부 클릭 → 무시
  if (chatWindow.value?.contains(target)) return;

  // 2️⃣ 로봇 버튼 클릭 → 무시
  if (robotButton.value?.contains(target)) return;

  // 3️⃣ 그 외 → 닫기
  open.value = false;
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    open.value = false;
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleKeydown);
});


// --- Logic Preserved Completely ---
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
  sessionId.value = null;
  localStorage.removeItem(SESSION_KEY);

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
</script>

<style scoped>
/* 🎨 MIA Cinema Chat Style */
.chatbot-wrapper {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: auto;
}

.chatbot-layout {
  display: flex;
  align-items: flex-end;
  gap: 8px; /* Robot and Window gap */
}

/* Chat Window - SIZE & POSITION FIXED AS REQUESTED */
.chat-window {
  width: 400px;  /* ❗️ FIXED SIZE */
  height: 400px; /* ❗️ FIXED SIZE */
  background: #0a0b0f;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
  position: relative;
  overflow: visible;
  transform-origin: bottom right;
}

/* Tail (Speech Bubble Effect) */
.chat-tail {
  position: absolute;
  bottom: 18px;
  right: -6px;
  width: 10px;
  height: 10px;
  background: #0a0b0f;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transform: rotate(-45deg);
  z-index: 10;
}

/* Header */
.chat-header {
  padding: 8px 12px;
  background: rgba(139, 92, 246, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-text {
  font-family: 'Pretendard', sans-serif;
  font-weight: 700;
  color: #c084fc;
  font-size: 14px;
  letter-spacing: 0.05em;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  box-shadow: 0 0 5px #22c55e;
}

.header-actions {
  display: flex;
  gap: 6px;
}

.action-btn {
  background: rgba(255, 255, 255, 0.05);
  border: none;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

/* Session Panel */
.session-panel {
  position: absolute;
  top: 40px;
  left: -180px; /* 원래 코드의 위치 유지 */
  width: 170px;
  height: calc(100% - 50px);
  background: #020617;
  border: 1px solid rgba(147, 51, 234, 0.3);
  border-radius: 12px;
  z-index: 20;
  display: flex;
  flex-direction: column;
  padding: 6px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.session-header {
  padding: 6px;
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.4);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.session-list-scroll {
  flex: 1;
  overflow-y: auto;
  padding-top: 4px;
}

.session-item {
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
  font-size: 11px;
  color: #e5e7eb;
}

.session-item:hover {
  background: rgba(255, 255, 255, 0.05);
}

.session-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Messages Area */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Custom Scrollbar */
.messages-area::-webkit-scrollbar, .session-list-scroll::-webkit-scrollbar {
  width: 4px;
}
.messages-area::-webkit-scrollbar-thumb, .session-list-scroll::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.message-row {
  display: flex;
  flex-direction: column;
  max-width: 90%;
}

.message-row.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message-row.assistant {
  align-self: flex-start;
  align-items: flex-start;
}

.bubble {
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 12px;
  line-height: 1.5;
  word-break: break-word;
}

.user .bubble {
  background: #7c3aed;
  color: white;
}

.assistant .bubble {
  background: #1f2937;
  color: #fff;
}

/* Loading Dots */
.bubble.loading {
  display: flex;
  gap: 4px;
}

.dot {
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Movie Cards */
.cards-container {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.movie-card {
  background: #111827;
  border: 1px solid rgba(147, 51, 234, 0.3);
  border-radius: 8px;
  overflow: hidden;
  padding: 8px;
}

.card-content {
  cursor: pointer;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 2px;
}

.movie-title {
  font-weight: 600;
  color: #c084fc;
  font-size: 12px;
}

.movie-reason {
  font-size: 11px;
  color: #9ca3af;
  margin-bottom: 4px;
  line-height: 1.3;
}

.link-text {
  font-size: 10px;
  color: #7c3aed;
  font-weight: 500;
}

.card-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 6px;
}

.card-btn {
  background: #1f2937;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 11px;
  cursor: pointer;
  border: none;
}

.card-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.card-btn.like { color: #22c55e; }
.card-btn.dislike { color: #ef4444; }

/* Input Area */
.input-area {
  padding: 6px;
  border-top: 1px solid rgba(147, 51, 234, 0.2);
  display: flex;
  gap: 6px;
}

.chat-input {
  flex: 1;
  background: #1f2937;
  border-radius: 8px;
  padding: 6px 8px;
  font-size: 12px;
  color: white;
  border: none;
  outline: none;
}

.chat-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-btn {
  background: #7c3aed;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 11px;
  color: white;
  border: none;
  cursor: pointer;
  white-space: nowrap;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Robot Icon */
.mia-float {
  height: 120px;
  width: auto;
  cursor: pointer;
  filter: drop-shadow(0 8px 12px rgba(0, 0, 0, 0.6));
  animation: mia-float 2s ease-in-out infinite;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}


/* 커서 올라갈 때 볼록하게 확대 */
.mia-float:hover {
  animation: none;
  transform: scale(1.04) translateY(0); /* 확대 + 위치 고정 */
}

/* Animations */
@keyframes mia-float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-10px) scale(1); }
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

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.2s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-10px);
  opacity: 0;
}
</style>