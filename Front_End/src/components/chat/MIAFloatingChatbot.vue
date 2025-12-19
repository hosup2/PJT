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
      <div
        v-if="open"
        style="
          width: 300px;
          height: 320px;
          background: #111827;
          border: 1px solid rgba(147,51,234,0.3);
          border-radius: 12px;
          padding: 10px;
          font-size: 12px;
          box-shadow: 0 20px 25px rgba(0,0,0,0.5);
          position: relative;
          display: flex;
          flex-direction: column;
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
        ></div>

        <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
          <strong style="color:#c084fc;">MIA</strong>
          <button @click="open=false" style="color:#9ca3af;">✕</button>
        </div>

        <div
          style="
            flex: 1;
            overflow-y: auto;
            margin-bottom: 6px;
            padding-right: 4px;
          "
        >
          <div
            v-for="(msg,i) in messages"
            :key="i"
            :style="{
              textAlign: msg.role === 'assistant' ? 'left' : 'right',
              marginBottom: '4px'
            }"
          >
            <span
              :style="{
                display:'inline-block',
                padding:'6px 8px',
                borderRadius:'8px',
                background: msg.role==='assistant' ? '#1f2937' : '#7c3aed',
                color:'#fff',
                maxWidth: '90%'
              }"
            >
              {{ msg.content }}
            </span>
          </div>
        </div>

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
            :disabled="!isLoggedIn"
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
              opacity: 1;
            "
          />

          <button
            type="submit"
            :disabled="!isLoggedIn"
            style="
              background:#7c3aed;
              border-radius:8px;
              padding:6px 10px;
              font-size:11px;
              color:white;
              white-space: nowrap;
              opacity: 1;
            "
          >
            전송
          </button>
        </form>

      </div>

      <!-- 🤖 로봇 (사이즈 줄임) -->
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
import { ref, inject } from 'vue';
import axios from 'axios';

const isLoggedIn = inject<boolean>('isLoggedIn', false);
const openAuthModal = inject<() => void>('openAuthModal');

const SESSION_KEY = 'mia_chat_session_id';

const sessionId = ref<number | null>(
  localStorage.getItem('mia_chat_session_id')
    ? Number(localStorage.getItem('mia_chat_session_id'))
    : null
);

const loading = ref(false);


interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const handleLoginClick = () => {
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

  messages.value.push({
    role: 'user',
    content: userMessage,
  });

  loading.value = true;

  try {
    const res = await axios.post(
      'http://127.0.0.1:8000/recommend/chat/',
      {
        message: userMessage,
        session_id: sessionId.value,
      }
    );

    const data = res.data;

    // session_id 저장 (처음 응답 시)
    if (data.session_id && !sessionId.value) {
      sessionId.value = data.session_id;
      localStorage.setItem('mia_chat_session_id', String(data.session_id));
    }

    messages.value.push({
      role: 'assistant',
      content: data.answer,
    });

    // 🔜 다음 단계에서 movies 렌더링 예정

  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '추천 중 문제가 발생했어요 😥 잠시 후 다시 시도해주세요.',
    });
  } finally {
    loading.value = false;
  }
};


const open = ref(false);

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content: isLoggedIn
      ? '안녕하세요! 어떤 영화를 추천해드릴까요? 🎬'
      : '로그인 후 MIA의 영화 추천을 이용할 수 있어요 😊',
  },
]);


const input = ref('');

</script>

<style scoped>
@keyframes mia-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.mia-float {
  animation: mia-float 3s ease-in-out infinite;
}
</style>
