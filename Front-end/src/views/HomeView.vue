<template>
  <div class="banner-slideshow">
    <transition name="fade" mode="out-in">
      <a
        :href="images[currentIndex].link"
        target="_blank"
        :key="images[currentIndex].src"
      >
        <img
          :src="images[currentIndex].src"
          :alt="images[currentIndex].alt"
          class="banner-image"
        />
      </a>
    </transition>

    <div class="carousel-dots">
      <div
        v-for="(img, index) in images"
        :key="'dot-' + index"
        :class="['carousel-dot', currentIndex === index ? 'active' : '']"
        @click="currentIndex = index"
      ></div>
    </div>
  </div>

  <!-- ✅ 뉴스 & 서비스: 슬라이드 너비에 맞춰 양쪽 정렬 -->
<div class="info-wrapper">
  <!-- ✅ 왼쪽: 금융 소식 -->
  <div class="news-box">
    <h3>금융 소식</h3>
    <ul>
      <li v-for="(item, i) in newsList" :key="i">
        <a :href="item.link" target="_blank">{{ item.title }}</a>
      </li>
    </ul>
  </div>

  <!-- ✅ 오른쪽: 금융 서비스 -->
  <div class="service-box">
    <h3>금융 서비스</h3>
    <div class="service-grid">
      <a
        v-for="(service, i) in services"
        :key="i"
        :href="service.url"
        target="_blank"
      >
        <img :src="service.icon" :alt="service.name" />
        <span>{{ service.name }}</span>
      </a>
    </div>
  </div>
</div>

<section class="youtube-section">
  <h2 class="section-title">금융 리포트</h2>
  <div class="youtube-scroll-wrapper">
    <div
      v-for="(video, index) in youtubeVideos"
      :key="index"
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
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

const images = [
  {
    src: '/Home/banner1.jpg',
    alt: '소상공인 지원1 - 하나은행',
    link: 'https://www.kebhana.com/cont/news/news02/1505914_115431.jsp'
  },
  {
    src: '/Home/banner2.png',
    alt: '소상공인 지원2 - 삼성펀드',
    link: 'https://www.samsungfund.com/fund/insight/house-view/view.do?seq=215'
  },
  {
    src: '/Home/banner3.png',
    alt: '소상공인 지원3 - 토스',
    link: 'https://www.tossbank.com/articles/bbc-common-good'
  },
  {
    src: '/Home/banner4.png',
    alt: '소상공인 지원4 - 우리은행',
    link: 'https://spot.wooribank.com/pot/Dream?withyou=EVEVT0001&cc=c001308:c001386'
  }
]

const currentIndex = ref(0)
let interval = null

const startSlideshow = () => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.length
  }, 6000) // 6초 간격으로 전환
}

import icon1 from '@/assets/Home/service1.jpg'
import icon2 from '@/assets/Home/service2.jpg'
import icon3 from '@/assets/Home/service3.png'
import icon4 from '@/assets/Home/service4.png'

const services = [
  { name: '서민금융진흥원', url: 'https://www.kinfa.or.kr/main.do', icon: icon1 },
  { name: '복지로', url: 'https://bokjiro.go.kr/', icon: icon2 },
  { name: '이자 계산기', url: 'https://calculator.asamaru.net/%EA%B3%84%EC%82%B0%EA%B8%B0/%EA%B8%88%EC%9C%B5/%EC%98%88%EA%B8%88-%EC%9D%B4%EC%9E%90-%EA%B3%84%EC%82%B0/', icon: icon3 },
  { name: '홈택스', url: 'https://www.hometax.go.kr/', icon: icon4 }
]

const newsList = [
  {
    title: '美·中 무역 협상에 춤추는 환율…"환테크 당분간 멀리해라"',
    link: 'https://www.hankyung.com/article/2025052541621'
  },
  {
    title: '서울시, 청년 자산 형성 돕는다…月15만원 3년 저축땐 1080만원',
    link: 'https://www.hankyung.com/article/2025052543001'
  },
  {
    title: '우체국예금 "자산 100조원 금융 공룡" 됐다',
    link: 'https://www.hankyung.com/article/2025052325111'
  },
  {
    title: '[퇴직연금 바꾸자] ③ 연평균 수익률 2.8% 어찌할꼬…개선 대책은',
    link: 'https://www.yna.co.kr/view/AKR20250523026900008?section=economy/finance'
  },
  {title:'카카오뱅크, 예적금 금리 최고 0.15%p 인하한다',
    link: 'https://news.einfomax.co.kr/news/articleView.html?idxno=4352399'
  }
]

const youtubeVideos = ref([])

onMounted(async () => {
  // ① 유튜브 영상 불러오기
  try {
    const res = await axios.get('http://127.0.0.1:8000/deposits/youtube/') // 금융 관련 영상
    youtubeVideos.value = res.data.results
  } catch (error) {
    console.error('❌ 유튜브 영상 불러오기 실패:', error)
  }

  // ② 슬라이드쇼 시작
  startSlideshow()
})

// 임의의 조회수 텍스트 반환 함수
const getFakeViews = (i) => {
  const dummyViews = [16, 5, 46, 92, 29, 73, 12, 38, 54, 67]
  return dummyViews[i % dummyViews.length]
}

console.log('🎥 유튜브 데이터:', youtubeVideos.value)


onBeforeUnmount(() => {
  clearInterval(interval)
})

</script>

<style>
body {
  background-color: #edf0f2;
}
</style>

<style scoped>
.banner-slideshow {
  width: 100%;
  max-width: 1024px;
  height: 22rem;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.carousel-dots {
  position: absolute;
  bottom: 0.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
}

.carousel-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ccc;
  cursor: pointer;
}
.carousel-dot.active {
  background-color: #2563eb;
}

/* ✅ 하단 섹션 전체 wrapper */
.info-wrapper {
  max-width: 1024px;
  margin: 2rem auto;
  display: flex;
  gap: 2rem;
  margin-top: 50px;
}

/* 우측 - 금융 서비스 */
.service-box {
  flex: 0 0 300px;
  background-color: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.16);
}

.service-box h3 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.2rem;
  justify-items: center;
  text-align: center;
}

.service-grid a {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #111;
}
.service-grid img {
  width: 55px;
  height: 55px;
  object-fit: contain;
  margin-bottom: 0.5rem;
  border: 1px solid #d1d5db; /* 연한 회색 (tailwind 기준 gray-300) */
  border-radius: 0.5rem;     /* 약간 둥글게 */
  padding: 6px;              /* 내부 여백 */
  background-color: #fff;    /* 흰 배경 */
  box-sizing: border-box;
}

/* 좌좌측 - 금융 소식 */
.news-box {
  flex: 1;
  background-color: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.16);
}

.news-box h3 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
}

.news-box ul {
  list-style-type: disc;
  padding-left: 1.2rem;
}

.news-box li {
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.news-box a {
  color: #111827;
  text-decoration: none;
}

.news-box a:hover {
  text-decoration: underline;
  color: #2563eb;
}

.youtube-section {
  max-width: 1024px;
  margin: 3rem auto;
}

.section-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

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
  -webkit-line-clamp: 2; /* 두 줄까지 */
  -webkit-box-orient: vertical;
}

</style>
