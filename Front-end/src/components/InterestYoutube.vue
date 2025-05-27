<template>
  <section class="youtube-search-section">
    <!-- 🔍 검색 바 -->
    <div class="search-bar">
      <span class="search-icon">🔍</span>
      <input
        v-model="query"
        @keyup.enter="filterVideos"
        type="text"
        placeholder="검색어를 입력하세요"
      />
      <button @click="filterVideos">검색</button>
    </div>

    <!-- 🕘 최근 검색어 표시 -->
    <div class="search-history" v-if="searchHistory.length">
      <span
        v-for="(item, index) in searchHistory"
        :key="index"
        class="history-tag"
      >
        {{ item }}
        <span class="remove-btn" @click="removeHistoryItem(item)">×</span>
      </span>
    </div>

    <!-- 🎥 유튜브 결과 카드 -->
    <div class="youtube-scroll-wrapper">
      <div
        v-for="(video, index) in filteredVideos"
        :key="video.videoId"
        class="youtube-card"
      >
        <a :href="video.url" target="_blank" rel="noopener noreferrer">
          <img :src="video.thumbnail" :alt="video.title" class="youtube-thumb" />
          <div class="youtube-info">
            <p class="youtube-title">{{ video.title }}</p>
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const query = ref('')
const youtubeVideos = ref([])
const filteredVideos = ref([])
const searchHistory = ref([]) // 🔍 검색 기록 상태

const filterVideos = async () => {
  const q = query.value.trim()
  if (!q) return

  // ✅ 중복 제거하고 가장 앞에 추가
  searchHistory.value = [q, ...searchHistory.value.filter(item => item !== q)].slice(0, 5)

  try {
    const res = await axios.get('http://127.0.0.1:8000/deposits/youtube/', {
      params: { query: q }
    })
    youtubeVideos.value = res.data.results
    filteredVideos.value = youtubeVideos.value.slice(0, 5)
    console.log('✅ 검색 결과:', filteredVideos.value)
  } catch (error) {
    console.error('❌ 검색 요청 실패:', error)
  }
}

// ❌ 검색 기록 삭제
const removeHistoryItem = (item) => {
  searchHistory.value = searchHistory.value.filter(q => q !== item)
}

// 📦 초기 로딩 시 기본 추천 영상 (금융)
onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/deposits/youtube/')
    youtubeVideos.value = res.data.results
    filteredVideos.value = youtubeVideos.value.slice(0, 5)
  } catch (error) {
    console.error('❌ 초기 영상 불러오기 실패:', error)
  }
})
</script>

<style scoped>
.youtube-search-section {
  max-width: 1024px;
  margin: 2rem auto;
}

/* 검색창 */
.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid #ccc;
  border-radius: 2rem;
  background-color: #fff;
}

.search-icon {
  font-size: 1.2rem;
}

.search-bar input {
  flex-grow: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  background: transparent;
}

.search-bar button {
  padding: 0.4rem 1rem;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 1rem;
  cursor: pointer;
}

/* 최근 검색어 */
.search-history {
  margin: 0 1rem 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.history-tag {
  background-color: #f3f4f6;
  color: #111827;
  padding: 0.3rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.remove-btn {
  cursor: pointer;
  font-weight: bold;
  color: #6b7280;
}
.remove-btn:hover {
  color: #ef4444;
}

/* 유튜브 카드 */
.youtube-scroll-wrapper {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 0 1rem;
}

.youtube-card {
  min-width: 180px;
  max-width: 180px;
  border: 1px solid #ddd;
  border-radius: 0.75rem;
  overflow: hidden;
  background: white;
  flex-shrink: 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.youtube-card a {
  text-decoration: none;
  color: inherit;
  display: block;
}

.youtube-thumb {
  width: 100%;
  height: 280px;
  object-fit: cover;
  display: block;
}

.youtube-info {
  padding: 0.5rem;
}

.youtube-title {
  font-size: 0.85rem;
  font-weight: 500;
  color: #111;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>