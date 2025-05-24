<template>
  <div class="min-h-screen bg-[#F0F2F5] py-10 px-4">
    <div class="relative-container">
    <!-- 투명 배경 상자 -->
    <div class="background-bar"></div>

    <!-- 문장 -->
    <p class="headline">
      데이터가 말해주는 현물의 흐름, 숫자 속
      <span class="highlight">기회</span>를 찾으세요! 
      <img :src="riseImg" alt="상승 아이콘" class="rise-icon" />
    </p>

    <!-- 시세 박스 -->
    <div class="price-box-wrapper">
        <!-- 금/은 시세 요약 -->
  <div class="price-grid-wrapper">
    <!-- 금 시세 -->
    <div class="price-cell">
      <img :src="goldIcon" alt="gold" class="price-icon" />
      <div class="price-text">
        <div class="title-row">
          <span class="title">오늘의 금 시세</span>
          <span class="unit">(단위: USD/oz)</span>
        </div>
        <div class="price-line"><span>시가</span><span>24.82</span></div>
        <div class="price-line"><span>고가</span><span>25.22</span></div>
        <div class="price-line"><span>저가</span><span>24.52</span></div>
      </div>
    </div>

    <!-- 은 시세 -->
    <div class="price-cell">
      <img :src="silverIcon" alt="silver" class="price-icon" />
      <div class="price-text">
        <div class="title-row">
          <span class="title">오늘의 은 시세</span>
          <span class="unit">(단위: USD/oz)</span>
        </div>
        <div class="price-line"><span>시가</span><span>24.82</span></div>
        <div class="price-line"><span>고가</span><span>25.22</span></div>
        <div class="price-line"><span>저가</span><span>24.52</span></div>
      </div>
    </div>
  </div>
</div>
</div>
    
  <div class="price-filter-box">
    <!-- 탭 -->
    <div class="filter-tab">
      <span class="tab-label">금/은 가격 변동</span>
    </div>

    <!-- 날짜 & 버튼 한 줄 정렬 -->
  <div class="filter-body">
    <div class="date-wrapper">
  <div class="date-group">
    <label>시작일:</label>
    <input type="date" v-model="startDate" />
  </div>
  <div class="date-group">
    <label>종료일:</label>
    <input type="date" v-model="endDate" />
  </div>
</div>
    <div class="metal-toggle">
      <button :class="isGold ? 'metal-btn active' : 'metal-btn'" @click="isGold = true">금</button>
      <button :class="!isGold ? 'metal-btn active' : 'metal-btn'" @click="isGold = false">은</button>
    </div>
</div>
  <div class="chart-container">
    <MetalChart :data="filteredData" />
</div>
  </div>
    <!-- 하단 버튼 -->
    <div class="button-wrapper">
    <button class="go-home-btn" @click="goHome">
      목록으로
    </button>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted , computed} from 'vue'
import { useRouter } from 'vue-router'
import goldIcon from '@/assets/Metal/gold-icon.png'
import silverIcon from '@/assets/Metal/silver-icon.png'
import riseImg from '@/assets/Metal/rise.png'
import * as XLSX from 'xlsx'
import MetalChart from '@/components/Metal/MetalChart.vue'
import goldExcel from '@/assets/Metal/Gold_prices.xlsx?url'
import silverExcel from '@/assets/Metal/Silver_prices.xlsx?url'

const router = useRouter()
const goHome = () => {
  router.push('/') // 🔁 루트 페이지로 이동
}

const goldData = ref([])
const silverData = ref([])

const isGold = ref(true)
const startDate = ref('')
const endDate = ref('')

const loadExcel = async () => {
  const load = async (url) => {
    const res = await fetch(url)
    const blob = await res.arrayBuffer()
    const workbook = XLSX.read(blob)
    const sheet = workbook.Sheets[workbook.SheetNames[0]]

    // 엑셀에서 Date와 Open을 추출해 변환
    return XLSX.utils.sheet_to_json(sheet).map(row => ({
      Date: typeof row['Date'] === 'string'
        ? row['Date'].substring(0, 10)
        : new Date(row['Date']).toISOString().substring(0, 10),
      Price: parseFloat(row['Open']) // 'Open' → 'Price' 필드로 저장
    }))
  }

  goldData.value = await load(goldExcel)
  silverData.value = await load(silverExcel)
}

onMounted(() => {
  loadExcel().then(() => {
    console.log('✅ goldData:', goldData.value)
    console.log('✅ silverData:', silverData.value)
    console.log('✅ filteredData:', filteredData.value)
  })
})

const filteredData = computed(() => {
  const source = isGold.value ? goldData.value : silverData.value

  if (!startDate.value || !endDate.value) return []

  return source
    .filter(item => {
      return (
        item.Date >= startDate.value &&
        item.Date <= endDate.value &&
        item.Price !== undefined &&
        !isNaN(item.Price)
      )
    })
    .sort((a, b) => a.Date.localeCompare(b.Date)) // 날짜 오름차순 정렬
})



</script>

<style scoped>
.header-wrapper {
  position: relative;
  width: 100%;
  margin-bottom: 16px;
}

.background-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 300px;
  background-color: rgba(204, 185, 141, 0.14); /* #CCB98D 14% */
  z-index: -1;
}

.headline {
  font-size: 18px;
  font-weight: 500;
  color: #111;
  padding: 24px 24px 8px;
  text-align: left;
  max-width: 1000px;
  margin: 0 auto;
}

.highlight {
  color: #22356F;
  font-weight: 700;
}

.rise-icon {
  width: 18px;
  height: 18px;
  margin-left: 6px;
  vertical-align: middle;
  transform: translateY(-2px); /* 미세 조정 */
}

.price-icon {
  width: 30px;
  height: 30px;
  object-fit: contain;
  flex-shrink: 0;
}

.price-grid-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr; /* ← 정확히 반씩 */
  background-color: #f5ecd9;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
  max-width: 1000px;
  margin: 0 auto;
  gap: 0;
}

.price-cell {
  display: flex;
  flex-direction: column;
  align-items: center; /* ← 내부도 중앙 정렬 */
  gap: 8px;
}

.price-icon {
  width: 30px;
  height: 30px;
  object-fit: contain;
  margin-bottom: 4px;
}

.price-text {
  font-size: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
  margin-bottom: 4px;
}

.title {
  font-weight: 600;
}

.unit {
  font-size: 13px;
  color: #555;
}

.price-line {
  display: flex;
  gap: 20px;
  font-size: 14px;
  font-weight: 520;
}

.price-filter-box {
  max-width: 1000px;
  margin: 0 auto;
  /* 기존 스타일 유지 가능 */
  padding: 20px;
  border-radius: 8px;
  /* 배경색 제거 완료됨 */
  background-color: transparent;
  margin-top: 30px;
}

.filter-tab {
  border-bottom: 1px solid #d1d5db;
  margin-bottom: 16px;
}

.tab-label {
  background-color: #3B4B70;
  color: white;
  padding: 6px 12px;
  border-radius: 4px 4px 0 0;
  font-weight: 600;
  font-size: 14px;
}

.filter-body {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 16px;
}


.date-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 150px;
}

.date-wrapper {
  display: flex;
  gap: 30px; /* ✅ 여기서 라벨 사이 간격 제어 */
}

.date-group label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.date-group input {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}

.metal-toggle {
  display: flex;
  gap: 8px;
  align-self: flex-end;
}

.metal-btn {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 14px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  color: #333;
  cursor: pointer;
}

.chart-container {
  margin-top: 24px;
}


.metal-btn.active {
  background-color: #3B4B70;
  color: white;
  border: none;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.go-home-btn {
  background-color: #22356F;
  color: white;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease;
}

.go-home-btn:hover {
  background-color: #1b2a58;
}


</style>
