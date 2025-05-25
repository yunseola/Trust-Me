<template>
     <!-- 환율 요약 -->
  <div class="exchange-wrapper">
    <div class="converter-box">
      <!-- 왼쪽 국가 선택 -->
      <div class="currency-box">
        <div class="country-wrapper">
          <div class="country-select-box">
            <img :src="getFlagUrl(selectedLeft.code)" alt="flag" />
            <span>{{ countryNameMap[selectedLeft.code] }}</span>
            <span class="code">{{ selectedLeft.code }}</span>
            <span class="arrow-button" @click.stop="toggleDropdown('left')">v</span>
          </div>
          <ul v-if="isDropdownLeft" class="dropdown-list">
            <li
              v-for="(name, code) in supported"
              :key="code"
              @click="selectCountry('left', code)"
            >
              {{ countryNameMap[code] || code }}
            </li>
          </ul>
        </div>
        <div class="amount-box">
          <div class="amount">1</div>
          <div class="unit">1 {{ selectedLeft.code }}</div>
        </div>
      </div>

      <!-- 등호 -->
      <div class="equals">=</div>

      <!-- 오른쪽 국가 선택 -->
      <div class="currency-box">
        <div class="country-wrapper">
          <div class="country-select-box">
            <img :src="getFlagUrl(selectedRight.code)" alt="flag" />
            <span>{{ countryNameMap[selectedRight.code] }}</span>
            <span class="code">{{ selectedRight.code }}</span>
            <span class="arrow-button" @click.stop="toggleDropdown('right')">v</span>
          </div>
          <ul v-if="isDropdownRight" class="dropdown-list">
            <li
              v-for="(name, code) in supported"
              :key="code"
              @click="selectCountry('right', code)"
            >
              {{ countryNameMap[code] || code }}
            </li>
          </ul>
        </div>
        <div class="amount-box">
          <div class="amount">{{ convertedRate }}</div>
          <div class="unit">{{ convertedRate }} {{ selectedRight.code }}</div>
        </div>
      </div>
    </div>
  </div>

    <!-- 주요 차트 -->
  <!-- 주요 차트 (슬라이더 적용) -->
<MiniChartSlider />

    <!-- 환율 테이블 -->
    <table class="rate-table">
      <thead>
        <tr>
          <th>국가명</th>
          <th>통화</th>
          <th>매매기준율</th>
          <th>전일비</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in exchangeData" :key="item.code">
          <td>{{ item.country }}</td>
          <td>{{ item.currency }}</td>
          <td>{{ item.rate }}</td>
          <td :class="item.change < 0 ? 'down' : 'up'">
            {{ item.change < 0 ? '▼' : '▲' }}{{ Math.abs(item.change) }}
          </td>
        </tr>
      </tbody>
    </table>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MiniChartSlider from '@/components/Exchange/MiniChartSlider.vue'
import MiniChartBox from '@/components/Exchange/MiniChartBox.vue'
import { currencies, rateSeries, fetchChartRates, dateLabels } from '@/api/chartRates'

const supported = ref({})
const rates = ref({})
const convertedRate = ref(0)

const selectedLeft = ref({ code: 'CNY' })
const selectedRight = ref({ code: 'KRW' })

const isDropdownLeft = ref(false)
const isDropdownRight = ref(false)

const toggleDropdown = (side) => {
  if (side === 'left') {
    isDropdownLeft.value = !isDropdownLeft.value
    isDropdownRight.value = false
  } else {
    isDropdownRight.value = !isDropdownRight.value
    isDropdownLeft.value = false
  }
}

const selectCountry = (side, code) => {
  if (side === 'left') {
    selectedLeft.value = { code }
  } else {
    selectedRight.value = { code }
  }
  isDropdownLeft.value = false
  isDropdownRight.value = false
  fetchConversion()
}

const getFlagUrl = (code) => {
  const countryCode = currencyToCountryCode[code] || code.toLowerCase()
  return `https://flagcdn.com/w40/${countryCode}.png`
}

const fetchSupported = async () => {
  const { data } = await axios.get('http://localhost:8000/deposits/exchange/supported/')
  supported.value = data
}

const fetchRates = async () => {
  const { data } = await axios.get('http://localhost:8000/deposits/exchange/major/')
  rates.value = data.rates
  fetchConversion()
}

const fetchConversion = async () => {
  const from = selectedLeft.value.code
  const to = selectedRight.value.code
  if (!from || !to) return

  if (from === 'USD') {
    convertedRate.value = (rates.value[to] || 0).toFixed(2)
  } else if (to === 'USD') {
    convertedRate.value = (1 / (rates.value[from] || 1)).toFixed(2)
  } else {
    const usdToFrom = 1 / (rates.value[from] || 1)
    const usdToTo = rates.value[to] || 0
    convertedRate.value = (usdToFrom * usdToTo).toFixed(2)
  }
}

const countryNameMap = {
  AED: '아랍에미리트',
  AUD: '호주',
  BRL: '브라질',
  CAD: '캐나다',
  CHF: '스위스',
  CNY: '중국',
  CZK: '체코',
  DKK: '덴마크',
  EUR: '유럽연합',
  GBP: '영국',
  HKD: '홍콩',
  IDR: '인도네시아',
  INR: '인도',
  JPY: '일본',
  KRW: '대한민국',
  MXN: '멕시코',
  MYR: '말레이시아',
  NOK: '노르웨이',
  NZD: '뉴질랜드',
  PLN: '폴란드',
  RUB: '러시아',
  SAR: '사우디아라비아',
  SEK: '스웨덴',
  SGD: '싱가포르',
  THB: '태국',
  TRY: '튀르키예',
  TWD: '대만',
  USD: '미국',
  VND: '베트남',
  ZAR: '남아프리카공화국'
}

const currencyToCountryCode = {
  USD: 'us',
  KRW: 'kr',
  CNY: 'cn',
  JPY: 'jp',
  EUR: 'eu',
  GBP: 'gb',
  RUB: 'ru',
  VND: 'vn',
  AUD: 'au',
  CAD: 'ca',
  CHF: 'ch',
  SGD: 'sg',
  HKD: 'hk',
  IDR: 'id',
  MYR: 'my',
  THB: 'th',
  TRY: 'tr',
  TWD: 'tw',
  ZAR: 'za',
  SAR: 'sa',
  NZD: 'nz',
  NOK: 'no',
  DKK: 'dk',
  SEK: 'se',
  INR: 'in',
  PLN: 'pl',
  MXN: 'mx',
  AED: 'ae',
  CZK: 'cz'
}

onMounted(() => {
  fetchSupported()
  fetchRates()
  fetchChartRates()
})

const exchangeData = ref([
  { country: '미국', currency: '달러', rate: 1375.2, change: -1.8, code: 'USD' },
  { country: '일본', currency: '엔', rate: 958.36, change: -2.67, code: 'JPY' },
  { country: '중국', currency: '위안', rate: 190.97, change: -0.25, code: 'CNY' },
  { country: '영국', currency: '파운드', rate: 1684.93, change: -0.49, code: 'GBP' },
])
</script>

<style scoped>
.exchange-wrapper {
  background-color: #f3e6c8;
  padding: 30px;
  display: flex;
  justify-content: center;
}

.converter-box {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 30px;
  max-width: 900px;     /* 💡 전체 최대 폭 제한 */
  margin: 0 auto;       /* 가운데 정렬 */
  width: 100%;
  padding: 0 20px;      /* 여백 */
  box-sizing: border-box;
}

.currency-box {
  flex: 1 1 320px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-sizing: border-box;
}

.country {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: bold;
  margin-bottom: 8px;
}

.country-select-box {
  width: 100%;
  background-color: rgba(255, 255, 255, 0.3);
  padding: 8px 12px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.country-select-box img {
  width: 28px;   /* ✅ 기존 30px에서 줄이기 */
  height: 18px;  /* ✅ 비율에 맞춰 줄이기 */
  object-fit: cover;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.country-wrapper {
  position: relative;
  width: 100%;
  max-width: 300px;
}

.country img {
  width: 30px;
  height: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.arrow-button {
  margin-left: auto;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  user-select: none;
  transition: all 0.2s ease;
}

.arrow-button:hover {
  background-color: #f0f0f0;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%; /* ✅ 부모인 country-wrapper와 동일하게 */
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-height: 300px;
  overflow-y: auto;
  z-index: 100;
  margin-top: 6px;
}

.dropdown-list li {
  padding: 6px 12px;       /* ✅ 기존보다 padding을 줄이거나 조정 */
  line-height: 1.2;        /* ✅ 글자 간 간격 조절 (기존보다 좁게) */
  font-size: 0.95rem;      /* (선택) 글자 조금 더 키우기 */
  cursor: pointer;
  white-space: nowrap; 
}

.dropdown-list li:hover {
  background-color: #f5f5f5;
}

.code {
  color: #888;
  font-size: 0.7rem;
}

.amount-box {
  background-color: #eef0f3;
  width: 100%;
  height: 80px;
  border-radius: 4px;
  padding: 10px 20px;
  text-align: right;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  box-sizing: border-box;
  margin-top: 6px;
}

.amount {
  font-size: 2rem;
  font-weight: bold;
  line-height: 1;
}

.unit {
  font-size: 0.8rem;
  color: #444;
}

.equals {
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #f4d35e; /* 노란 원 */
  color: #fff;               /* ✅ 흰색 텍스트 */
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
line-height: 1.2; /* ✅ 텍스트만 위로 살짝 이동 */
  /* ✅ 아래로 위치 이동 */
  margin-top: 30px;
}

.chart-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 30px;
}
</style>
 