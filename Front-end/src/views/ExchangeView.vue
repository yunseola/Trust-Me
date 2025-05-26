<template>
  <div v-if="loading" class="loader-container">
    <div class="spinner"></div>
    <p class="loading-text">환율 정보를 불러오는 중...</p>
  </div>
  <div v-else>
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

    <!-- 주요 차트 (슬라이더 적용) -->
    <MiniChartSlider />

    <!-- 환율 테이블 -->
    <div class="rate-table-wrapper">
      <table class="rate-table">
        <thead>
          <tr>
            <th>국가명</th>
            <th>통화</th>
            <th>매매기준율</th>
            <th>전일비</th>
            <th>사실 때</th>
            <th>파실 때</th>
            <th>송금 보낼 때</th>
            <th>송금 받을 때</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, idx) in enrichedRates"
            :key="row.code"
            :class="{ 'row-divider': (idx + 1) % 5 === 0 }"
          >
            <td class="flag-name-cell">
              <img :src="getFlagUrl(row.code)" alt="flag" class="flag-icon" />
              {{ row.country }}
            </td>
            <td>{{ row.currency }}</td>
            <td>{{ formatNumber(row.baseRate) }}</td>
            <td :class="row.change < 0 ? 'down' : 'up'">
              {{ row.change < 0 ? '▼' : '▲' }}{{ Math.abs(row.change).toFixed(2) }}
            </td>
            <td>{{ formatNumber(row.buy) }}</td>
            <td>{{ formatNumber(row.sell) }}</td>
            <td>{{ formatNumber(row.send) }}</td>
            <td>{{ formatNumber(row.receive) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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

const enrichedRates = ref([])

const formatNumber = (num) => {
  return Number(num).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const fetchPrevRates = async () => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const date = yesterday.toISOString().split('T')[0]
  const { data } = await axios.get(`https://api.frankfurter.app/${date}?from=USD`)
  return data.rates
}

const buildExchangeTable = async () => {
  const prev = await fetchPrevRates()
  const today = rates.value

  enrichedRates.value = Object.keys(today).map(code => {
    const todayRate = today[code]
    const yesterdayRate = prev[code] ?? todayRate
    const change = (todayRate - yesterdayRate) * 100

    return {
      code,
      country: countryNameMap[code] || code,
      currency: supported.value[code] || '',
      baseRate: todayRate * 100,
      change: change,
      buy: todayRate * 101,
      sell: todayRate * 99,
      send: todayRate * 102,
      receive: todayRate * 98
    }
  })

  console.log('📌 prevRates', prev)
  console.log('📌 todayRates', today)
  console.log('📌 enriched', enrichedRates.value)
}

const loading = ref(true)

onMounted(async () => {
  loading.value = true
  await fetchSupported()
  await fetchRates()
  await fetchChartRates()
  await buildExchangeTable()
  loading.value = false
})


const countryNameMap = {
  AED: '아랍에미리트', AUD: '호주', BRL: '브라질', CAD: '캐나다', CHF: '스위스',
  CNY: '중국', CZK: '체코', DKK: '덴마크', EUR: '유럽연합', GBP: '영국',
  HKD: '홍콩', IDR: '인도네시아', INR: '인도', JPY: '일본', KRW: '대한민국',
  MXN: '멕시코', MYR: '말레이시아', NOK: '노르웨이', NZD: '뉴질랜드', PLN: '폴란드',
  RUB: '러시아', SAR: '사우디아라비아', SEK: '스웨덴', SGD: '싱가포르', THB: '태국',
  TRY: '튀르키예', TWD: '대만', USD: '미국', VND: '베트남', ZAR: '남아프리카공화국'
}

const currencyToCountryCode = {
  USD: 'us', KRW: 'kr', CNY: 'cn', JPY: 'jp', EUR: 'eu', GBP: 'gb', RUB: 'ru',
  VND: 'vn', AUD: 'au', CAD: 'ca', CHF: 'ch', SGD: 'sg', HKD: 'hk', IDR: 'id',
  MYR: 'my', THB: 'th', TRY: 'tr', TWD: 'tw', ZAR: 'za', SAR: 'sa', NZD: 'nz',
  NOK: 'no', DKK: 'dk', SEK: 'se', INR: 'in', PLN: 'pl', MXN: 'mx', AED: 'ae', CZK: 'cz', BRL: 'br'
}
</script>


<style>
body {
  background-color: #edf0f2;
}
</style>


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

.rate-table-wrapper {
  margin: 40px auto;
  max-width: 1100px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
}
.rate-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.rate-table thead {
  background-color: #f4f4f4;
}
.rate-table th,
.rate-table td {
  padding: 10px 14px;
  border-bottom: 1px solid #eee;
  text-align: center;
}
.up {
  color: red;
  font-weight: bold;
}
.down {
  color: blue;
  font-weight: bold;
}

.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
}


.spinner {
  border: 6px solid #eee;
  border-top: 6px solid #3b82f6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 16px;
  font-size: 1rem;
  color: #666;
}

.flag-name-cell {
  display: flex;
  align-items: center;
  gap: 6px;
}

.flag-icon {
  width: 20px;
  height: 14px;
  object-fit: contain;
  border: 1px solid #ccc;
  border-radius: 3px;
}

/* 5개마다 굵은 선 */
.row-divider {
  border-bottom: 2px solid #bbb !important;
}


</style>
 