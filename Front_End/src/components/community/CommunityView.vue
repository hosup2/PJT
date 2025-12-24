<template>
  <div class="community-container">
    
    <header class="cinema-header">
      <div class="header-inner">
        
        <button @click="goBack" class="btn-back-minimal">
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 19l-7-7 7-7"/>
          </svg>
          <span>뒤로가기</span>
        </button>

        <div class="header-left">
          <span class="section-label">COMMUNITY</span>
          <h1 class="page-title">라운지</h1>
          <p class="page-subtitle">영화인들의 깊이 있는 대화 공간</p>
        </div>
        
        <div class="mode-switcher">
          <button 
            @click="currentMode = 'board'" 
            :class="['switch-btn', { active: currentMode === 'board' }]"
          >
            자유 게시판
          </button>
          <button 
            @click="currentMode = 'chat'" 
            :class="['switch-btn', { active: currentMode === 'chat' }]"
          >
            무비 톡 (LIVE)
          </button>
        </div>

        <button v-if="isLoggedIn && currentMode === 'board'" @click="goToCreate" class="btn-write-minimal">
          <span>새 글 작성</span>
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
        </button>
      </div>
    </header>

    <main v-if="currentMode === 'board'" class="board-view">
      
      <div class="filter-bar">
        <div class="filter-left">
          <button 
            v-for="tab in tabs" :key="tab.value"
            @click="filter = tab.value"
            :class="['filter-text-btn', { active: filter === tab.value }]"
          >
            {{ tab.label }}
          </button>
        </div>
        <div class="search-minimal">
          <input v-model="searchQuery" type="text" placeholder="제목, 내용 검색..." />
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </div>
      </div>

      <div class="compact-list-header">
        <span class="col-title">제목</span>
        <div class="col-meta-group">
          <span class="col-author">작성자</span>
          <span class="col-date">날짜</span>
          <span class="col-views">조회</span>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner-small"></div>
      </div>

      <div v-else-if="filteredPosts.length === 0" class="empty-state">
        <p>게시글이 없습니다.</p>
      </div>

      <div v-else class="compact-list">
        <article
          v-for="post in filteredPosts"
          :key="post.id"
          class="compact-item"
          @click="goToDetail(post.id)"
        >
          <div class="item-main">
            <div class="title-row">
              <span v-if="post.movie_title" class="movie-tag">{{ post.movie_title }}</span>
              <h3 class="post-subject">{{ post.title }}</h3>
              <span v-if="post.comment_count > 0" class="comment-badge">[{{ post.comment_count }}]</span>
            </div>
          </div>

          <div class="item-meta">
            <span class="meta-author">{{ post.author.username }}</span>
            <span class="meta-date">{{ formatSimpleDate(post.created_at) }}</span>
            <span class="meta-view">{{ post.view_count }}</span>
          </div>
        </article>
      </div>
    </main>


    <main v-if="currentMode === 'chat'" class="chat-view">
      
      <aside class="chat-sidebar">
        <h3 class="sidebar-title">ON AIR</h3>
        <div class="movie-channel-list">
          <button 
            v-for="room in chatRooms" 
            :key="room.id"
            @click="selectChatRoom(room)"
            :class="['channel-item', { active: selectedChatRoom?.id === room.id }]"
          >
            <img :src="`https://image.tmdb.org/t/p/w92${room.movie_poster}`" class="channel-poster" />
            <div class="channel-info">
              <span class="channel-name">{{ room.movie_title }}</span>
              <span class="channel-users">● {{ room.message_count }} msg</span>
            </div>
          </button>
          
          <!-- 새 채팅방 만들기 버튼 -->
          <button @click="openCreateModal" class="add-room-btn">
            + 새로운 영화 채팅방 만들기
          </button>
        </div>
      </aside>

      <section class="chat-interface">
        <div v-if="selectedChatRoom" class="chat-room">
          
          <div class="room-header">
            <div class="room-info">
              <h2>{{ selectedChatRoom.movie_title }}</h2>
              <span class="live-badge">LIVE</span>
            </div>
          </div>

          <div class="messages-container" ref="messagesContainer">
            <div 
              v-for="msg in chatMessages" 
              :key="msg.id"
              :class="['message-bubble', { 'me': msg.isMe }]"
            >
              <div v-if="!msg.isMe" class="msg-avatar">
                {{ msg.username[0] }}
              </div>
              <div class="msg-content-wrapper">
                <span v-if="!msg.isMe" class="msg-username">{{ msg.username }}</span>
                <div class="msg-text">{{ msg.text }}</div>
                <span class="msg-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>

          <div class="chat-input-area">
            <input 
              v-model="chatInput" 
              @keyup.enter="sendChatMessage"
              type="text" 
              placeholder="이 영화에 대한 생각을 나눠보세요..." 
            />
            <button @click="sendChatMessage" class="btn-send">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </div>

        </div>

        <div v-else class="chat-placeholder">
          <div class="placeholder-content">
            <span class="icon">💬</span>
            <h3>영화를 선택하여 대화를 시작하세요</h3>
            <p>실시간으로 영화에 대한 감상을 나눌 수 있습니다.</p>
          </div>
        </div>

      </section>

    </main>

    <!-- Create Room Modal (Moved to Root) -->
    <div v-if="isCreateModalOpen" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-content">
        <h3 class="modal-title">영화 채팅방 만들기</h3>
        
        <div class="search-input-group">
          <input 
            v-model="movieSearchQuery" 
            @keyup.enter="searchMovies"
            placeholder="영화 제목을 검색하세요"
            autoFocus
          />
          <button @click="searchMovies" class="search-btn">검색</button>
        </div>

        <div class="search-results">
          <button 
            v-for="movie in movieSearchResults" 
            :key="movie.id" 
            class="search-item"
            @click="createAndJoinRoom(movie)"
          >
            <img :src="`https://image.tmdb.org/t/p/w92${movie.poster_path}`" class="search-poster" v-if="movie.poster_path" />
            <div class="search-info">
              <span class="search-title">{{ movie.title }}</span>
              <span class="search-year">{{ movie.release_date?.split('-')[0] }}</span>
            </div>
          </button>
          <div v-if="movieSearchResults.length === 0 && movieSearchQuery" class="no-results">
            검색 결과가 없습니다.
          </div>
        </div>

        <button @click="closeCreateModal" class="close-btn">닫기</button>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, inject, nextTick, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// --- Types ---
interface Author { id: number; username: string; }
interface Post {
  id: number; author: Author; title: string;
  movie_id?: number; movie_title?: string; movie_poster?: string;
  created_at: string; comment_count: number; view_count: number;
}
interface ChatMessage {
  id: number; username: string; text: string; time: string; isMe: boolean;
}

const router = useRouter();
const isLoggedIn = inject<Ref<boolean>>('isLoggedIn');
const currentUser = inject<Ref<any>>('currentUser');

// --- State ---
const currentMode = ref<'board' | 'chat'>('board'); // Tab State
const posts = ref<Post[]>([]);
const loading = ref(true);
const filter = ref('all');
const searchQuery = ref('');

// --- Board Logic ---
const tabs = [
  { label: '전체글', value: 'all' },
  { label: '영화수다', value: 'movie' },
  { label: '인기글', value: 'popular' },
];

const filteredPosts = computed(() => {
  let result = posts.value;
  if (filter.value === 'movie') result = result.filter(post => post.movie_id);
  else if (filter.value === 'popular') result = result.filter(post => post.comment_count > 5 || post.view_count > 20);

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(post => post.title.toLowerCase().includes(query));
  }
  return result;
});

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/posts/');
    posts.value = response.data.results || response.data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const formatSimpleDate = (dateString: string) => {
  const date = new Date(dateString);
  const now = new Date();
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false });
  }
  return date.toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' });
};

// --- Chat Logic ---
const chatRooms = ref<any[]>([]);
const selectedChatRoom = ref<any>(null);
const chatMessages = ref<ChatMessage[]>([]);
const chatInput = ref('');
const messagesContainer = ref<HTMLElement | null>(null);
let chatSocket: WebSocket | null = null;

// --- Modal & Search State ---
const isCreateModalOpen = ref(false);
const movieSearchQuery = ref('');
const movieSearchResults = ref<any[]>([]);

const openCreateModal = () => {
  isCreateModalOpen.value = true;
  movieSearchQuery.value = '';
  movieSearchResults.value = [];
};

const closeCreateModal = () => {
  isCreateModalOpen.value = false;
};

const searchMovies = async () => {
  if (!movieSearchQuery.value.trim()) return;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/movies/search/?q=${movieSearchQuery.value}`);
    movieSearchResults.value = response.data.results || response.data;
  } catch (err) {
    console.error('Failed to search movies:', err);
  }
};

const createAndJoinRoom = async (movie: any) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/community/chatrooms/', {
      movie_id: movie.id
    });
    
    const room = response.data;
    await selectChatRoom(room);
    closeCreateModal();
    await loadChatRooms();
  } catch (err) {
    console.error('Failed to create room:', err);
    alert('채팅방 생성 실패');
  }
};

const loadChatRooms = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/community/chatrooms/active_rooms/');
    chatRooms.value = response.data;
  } catch (err) {
    console.error('Failed to load chat rooms:', err);
  }
};

const selectChatRoom = async (room: any) => {
  selectedChatRoom.value = room;
  
  if (chatSocket) {
    chatSocket.close();
  }

  // Load previous messages
  try {
    const response = await axios.get(`http://127.0.0.1:8000/community/chatrooms/${room.id}/messages/`);
    chatMessages.value = response.data.map((msg: any) => ({
      id: msg.id,
      username: msg.username,
      text: msg.message,
      time: new Date(msg.created_at).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false }),
      isMe: msg.username === currentUser.value?.username
    }));
  } catch (err) {
    console.error('Failed to load messages:', err);
  }

  connectWebSocket(room.id);
  scrollToBottom();
};

const connectWebSocket = (roomId: number) => {
  const wsUrl = `ws://127.0.0.1:8000/ws/chat/${roomId}/`;
  chatSocket = new WebSocket(wsUrl);

  chatSocket.onopen = () => {
    console.log('WebSocket connected');
  };

  chatSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    chatMessages.value.push({
      id: Date.now(),
      username: data.username,
      text: data.message,
      time: new Date(data.timestamp || Date.now()).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', hour12: false }),
      isMe: data.username === currentUser.value?.username
    });
    scrollToBottom();
  };

  chatSocket.onclose = () => {
    console.log('WebSocket disconnected');
  };
};

const sendChatMessage = () => {
  console.log('Attempting to send message...');
  if (!chatInput.value.trim()) {
    console.log('Chat input is empty');
    return;
  }
  if (!chatSocket) {
    console.error('Chat socket is not connected');
    alert('채팅 서버에 연결되지 않았습니다.');
    return;
  }
  if (!currentUser.value) {
    console.error('Current user is missing');
    alert('로그인 정보가 없습니다. 다시 로그인해주세요.');
    return;
  }

  const messageData = {
    message: chatInput.value,
    username: currentUser.value.username,
    user_id: currentUser.value.id,
    timestamp: new Date().toISOString()
  };
  
  console.log('Sending message:', messageData);
  chatSocket.send(JSON.stringify(messageData));
  chatInput.value = '';
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

// Load initial data
onMounted(async () => {
  await fetchPosts();
  await loadChatRooms();
});

const goToCreate = () => {
  if (!isLoggedIn?.value) { alert('로그인 필요'); return; }
  router.push('/community/create');
};
const goToDetail = (id: number) => router.push(`/community/post/${id}`);
const goBack = () => router.back();

</script>

<style scoped>
/* 🎨 MIA Cinema System - Pure Black */
.community-container {
  min-height: 100vh;
  background: #0a0b0f;
  color: #ffffff;
  font-family: 'Pretendard', sans-serif;
  padding-top: 5rem;
  padding-bottom: 0;
  display: flex;
  flex-direction: column;
}

/* Header */
.cinema-header {
  padding: 2rem 3rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(10, 11, 15, 0.95);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 4rem; /* 네비게이션바 아래 */
  z-index: 40;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  /* 🔥 position: relative를 추가하여 절대 위치의 기준점 역할 */
  position: relative; 
}

/* 🔥 뒤로가기 버튼 스타일 (Absolute Position) */
.btn-back-minimal {
  position: absolute;
  top: -6rem; /* 타이틀보다 위로 */
  left: -1rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.7);
  padding: 0.5rem 1rem;
  border-radius: 100px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-back-minimal:hover {
 /* 배경이 살짝 밝아지며 보라색 기운이 돔 */
  background: rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2); /* 은은한 보라색 빛 */
}

/* 타이틀과 겹치지 않게 여백 추가 */
.header-left {
  padding-top: 0rem; /* 뒤로가기 버튼 공간 확보 */
}

.section-label {
  font-size: 0.6875rem;
  font-weight: 700;
  color: #8b5cf6;
  letter-spacing: 0.1em;
  display: block;
  margin-bottom: 0.25rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 300;
  margin: 0;
  color: white;
}

.page-subtitle {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  margin: 0.25rem 0 0;
}

/* Mode Switcher (Tabs) */
.mode-switcher {
  display: flex;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.25rem;
  border-radius: 8px;
  gap: 0.25rem;
}

.switch-btn {
  padding: 0.5rem 1.25rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.5);
  background: transparent;
  transition: all 0.2s ease;
}

.switch-btn.active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-weight: 600;
}

.btn-write-minimal {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  transition: all 0.2s;
}

.btn-write-minimal:hover {
  
  background: rgba(139, 92, 246, 0.15);
  border-color: #8b5cf6;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2); /* 은은한 보라색 빛 */
}

/* ================= BOARD VIEW (Compact) ================= */
.board-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 3rem;
  width: 100%;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filter-left {
  display: flex;
  gap: 1.5rem;
}

.filter-text-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9375rem;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.filter-text-btn.active {
  color: #ffffff;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 6px;
  text-decoration-color: #8b5cf6;
}

.search-minimal {
  position: relative;
  width: 240px;
}

.search-minimal input {
  width: 100%;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  padding: 0.5rem 0 0.5rem 0;
  color: white;
  font-size: 0.875rem;
  padding-right: 1.5rem;
  transition: border-color 0.2s;
}

.search-minimal input:focus {
  outline: none;
  border-color: #8b5cf6;
}

.search-icon {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: rgba(255, 255, 255, 0.4);
}

/* Compact List Header */
.compact-list-header {
  display: flex;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 600;
}

.col-title { flex: 1; padding-left: 0.5rem; }
.col-meta-group { display: flex; width: 200px; text-align: center; }
.col-author { width: 80px; }
.col-date { width: 70px; }
.col-views { width: 50px; }

/* Compact Item */
.compact-list {
  display: flex;
  flex-direction: column;
}

.compact-item {
  display: flex;
  align-items: center;
  padding: 1rem 0.5rem; /* Compact Padding */
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  cursor: pointer;
  transition: background 0.2s;
}

.compact-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.item-main {
  flex: 1;
  min-width: 0;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.movie-tag {
  background: rgba(139, 92, 246, 0.15);
  color: #a78bfa;
  font-size: 0.6875rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  white-space: nowrap;
}

.post-subject {
  font-size: 0.9375rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.comment-badge {
  color: #8b5cf6;
  font-size: 0.75rem;
  font-weight: 600;
}

.item-meta {
  display: flex;
  width: 200px;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
  text-align: center;
  flex-shrink: 0;
}

.meta-author { width: 80px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.meta-date { width: 70px; }
.meta-view { width: 50px; }


/* ================= CHAT VIEW ================= */
.chat-view {
  flex: 1;
  display: flex;
  height: calc(100vh - 200px);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

/* Chat Sidebar */
.chat-sidebar {
  width: 280px;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(15, 16, 20, 0.5);
  display: flex;
  flex-direction: column;
}

.sidebar-title {
  padding: 1.5rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.4);
  letter-spacing: 0.05em;
  margin: 0;
}

.movie-channel-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 0.5rem;
}

.channel-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 0.25rem;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.channel-item:hover {
  background: rgba(255, 255, 255, 0.03);
}

.channel-item.active {
  background: rgba(139, 92, 246, 0.15);
}

.channel-poster {
  width: 32px;
  height: 48px;
  border-radius: 4px;
  object-fit: cover;
  margin-right: 0.75rem;
}

.channel-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.channel-name {
  font-size: 0.875rem;
  color: white;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.channel-users {
  font-size: 0.75rem;
  color: #34d399; /* Online Green */
  margin-top: 0.125rem;
}

/* Chat Interface */
.chat-interface {
  flex: 1;
  background: #0f1014; /* Slightly lighter than main bg */
  position: relative;
}

.chat-room {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.room-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(15, 16, 20, 0.8);
}

.room-info h2 {
  font-size: 1.125rem;
  color: white;
  margin: 0 0 0.25rem 0;
}

.live-badge {
  background: #ef4444;
  color: white;
  font-size: 0.625rem;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  font-weight: 700;
}

/* Messages */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-bubble {
  display: flex;
  gap: 0.75rem;
  max-width: 70%;
}

.message-bubble.me {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: #2d3748;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.7);
  flex-shrink: 0;
}

.msg-content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.message-bubble.me .msg-content-wrapper {
  align-items: flex-end;
}

.msg-username {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 0.25rem;
}

.msg-text {
  background: #27272a;
  color: rgba(255, 255, 255, 0.9);
  padding: 0.625rem 1rem;
  border-radius: 0 12px 12px 12px;
  font-size: 0.9375rem;
  line-height: 1.5;
}

.message-bubble.me .msg-text {
  background: #7c3aed; /* Purple */
  color: white;
  border-radius: 12px 0 12px 12px;
}

.msg-time {
  font-size: 0.6875rem;
  color: rgba(255, 255, 255, 0.2);
  margin-top: 0.25rem;
}

/* Chat Input */
.chat-input-area {
  padding: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  gap: 0.75rem;
  background: rgba(15, 16, 20, 0.8);
}

.chat-input-area input {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 100px;
  padding: 0.75rem 1.25rem;
  color: white;
  font-size: 0.9375rem;
}

.chat-input-area input:focus {
  outline: none;
  border-color: #8b5cf6;
  background: rgba(255, 255, 255, 0.08);
}

.btn-send {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 50%;
  background: #8b5cf6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-send:hover {
  background: #6d28d9;
  transform: scale(1.05);
}

/* Placeholder */
.chat-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
}

.placeholder-content {
  text-align: center;
}

.placeholder-content .icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-view {
    flex-direction: column;
    height: auto;
  }
  
  .chat-sidebar {
    width: 100%;
    height: 120px;
    border-right: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }
  
  .movie-channel-list {
    display: flex;
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .channel-item {
    width: 200px;
    flex-shrink: 0;
  }
  
  .chat-interface {
    height: 60vh;
  }
}

/* Create Room Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #1f1f1f;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  margin-bottom: 0.5rem;
}

.search-input-group {
  display: flex;
  gap: 0.5rem;
}

.search-input-group input {
  flex: 1;
  padding: 0.8rem;
  border-radius: 8px;
  border: 1px solid #333;
  background: #2b2b2b;
  color: white;
}

.search-btn {
  padding: 0 1.5rem;
  background: #e50914;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.search-results {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-height: 200px;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem;
  background: #2b2b2b;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  border: none;
  text-align: left;
  width: 100%;
}

.search-item:hover {
  background: #333;
}

.search-poster {
  width: 40px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.search-info {
  display: flex;
  flex-direction: column;
  color: white;
}

.search-title {
  font-weight: bold;
}

.search-year {
  font-size: 0.8rem;
  color: #888;
}

.close-btn {
  margin-top: 1rem;
  padding: 0.8rem;
  background: #333;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.add-room-btn {
  width: 100%;
  margin-top: 1rem;
  padding: 0.8rem;
  background: #333;
  color: #ccc;
  border: 1px dashed #555;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.add-room-btn:hover {
  background: #444;
  color: white;
  border-color: #888;
}
</style>