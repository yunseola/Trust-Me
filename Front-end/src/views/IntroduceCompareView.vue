<template>
  <div class="finance-compare-container">
    <h2 class="headline">
      지금 당신에게 더 잘 맞는 금융상품은?
      똑똑한 비교로 <span class="highlight">한눈에!</span>
      <span class="emoji">🔍</span>
    </h2>
    <div class="card-area">
      <div
        v-for="product in products"
        :key="product.fin_prdt_cd"
        :class="['product-card', isSelected(product) ? 'selected' : '']"
        @click="toggleSelect(product)"
      >
        <div class="logo-area">
          <img :src="getBankLogo(product.kor_co_nm)" :alt="product.kor_co_nm" class="bank-logo" width="80px" height="80px" />
          <span class="bank-name">{{ product.kor_co_nm }}</span>
        </div>
        <div class="product-name">{{ product.fin_prdt_nm }}</div>
        <div class="product-info">
          <span class="rate">연 {{ product.max_intr }}%</span>
          <span class="period">{{ product.type === 'deposit' ? '예금' : '적금' }}</span>
        </div>
      </div>
    </div>
    <div class="guide-text">비교하고 싶은 상품을 2개 고르세요</div>
    <div class="btn-row">
      <button class="reset-btn" @click="resetSelect">초기화</button>
      <button class="compare-btn" :disabled="selected.length !== 2" @click="compare">비교하기</button>
    </div>

    <div v-if="showCompare" class="compare-table-wrap">
      <table class="compare-table">
        <thead>
          <tr>
            <th></th>
            <th v-for="(p, i) in selected" :key="i">{{ p.fin_prdt_nm }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>상품 종류</td>
            <td v-for="p in selected">{{ p.type === 'deposit' ? '예금' : '적금' }}</td>
          </tr>
          <tr>
            <!-- <td>상품 기간</td>
            <td v-for="p in selected">{{ p.period }}개월</td> -->
          </tr>
          <tr>
            <td>기본 금리</td>
            <td v-for="p in selected">{{ p.max_intr }}%</td>
          </tr>
          <tr>
            <td>우대 금리</td>
            <td v-for="p in selected">
              <div v-for="(line, idx) in (p.spcl_cnd || '').split('\n')" :key="idx">{{ line }}</div>
            </td>
          </tr>
          <tr>
            <td>이자 방식</td>
            <td v-for="p in selected">복리</td>
          </tr>
          <tr>
            <td>가입 대상</td>
            <td v-for="p in selected">{{ p.join_member }}</td>
          </tr>
          <tr>
            <td>가입 방법</td>
            <td v-for="p in selected">{{ p.join_way }}</td>
          </tr>
          <tr>
            <td>만기 이자</td>
            <td v-for="p in selected">{{ p.mtrt_int }}</td>
          </tr>
          <tr>
            <td>기타 안내</td>
            <td v-for="p in selected">{{ p.etc_note }}</td>
          </tr>
        </tbody>
      </table>
      <button class="back-btn" @click="showCompare = false">목록으로</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getBankLogo } from '@/api/logos.js'

const router = useRouter()
const STORAGE_KEY = 'savedFinanceProducts'
const products = ref([])
const selected = ref([])
const showCompare = ref(false)

// 로그인 토큰 체크 함수
function checkAuthToken() {
  // 일반적인 토큰 키들을 체크 (프로젝트에 맞게 수정하세요)
  const tokenKeys = ['authToken', 'accessToken', 'jwt', 'userToken']
  
  for (const key of tokenKeys) {
    const token = localStorage.getItem(key)
    if (token && token.trim() !== '') {
      return true
    }
  }
  return false
}

// 로그인 페이지로 리다이렉트
function redirectToLogin() {
  alert('로그인 후 이용해주세요.')
  router.push('/login') // 로그인 페이지 경로에 맞게 수정하세요
}

function loadProducts() {
  const data = localStorage.getItem(STORAGE_KEY)
  products.value = data ? JSON.parse(data) : []
}

function isSelected(product) {
  return selected.value.some(
    p => p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type
  )
}

function toggleSelect(product) {
  const idx = selected.value.findIndex(
    p => p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type
  )
  if (idx >= 0) {
    selected.value.splice(idx, 1)
  } else if (selected.value.length < 2) {
    selected.value.push(product)
  }
}

function resetSelect() {
  selected.value = []
  showCompare.value = false
}

function compare() {
  if (selected.value.length === 2) {
    showCompare.value = true
  }
}

onMounted(() => {
  // 로그인 토큰 체크
  if (!checkAuthToken()) {
    redirectToLogin()
    return
  }
  
  loadProducts()
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY) loadProducts()
  })
})
</script>

<style scoped>
.finance-compare-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 10px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

.headline {
  text-align: center;
  font-size: 1.2rem;
  font-weight: 500;
  margin: 32px 0 24px 0;
  letter-spacing: -0.01em;
}

.highlight {
  color: #253a7d;
  font-weight: 700;
  text-decoration: underline;
}

.emoji {
  font-size: 1.1em;
  margin-left: 2px;
}

.card-area {
  display: flex;
  gap: 28px;
  justify-content: center;
  background: #f5eedd;
  padding: 36px 0 24px 0;
  border-radius: 12px;
  max-width: 900px;   /* 기존 700px → 900px */
  margin: 0 auto;
}

.product-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px #e5eaf0cc;
  border: 2px solid transparent;
  transition: border 0.2s, box-shadow 0.2s, transform 0.2s;
  cursor: pointer;
  width: 220px;      /* 기존 180px → 220px */
  padding: 24px 16px 18px 16px;
  text-align: center;
  position: relative;
}

.product-card.selected {
  border: 2px solid #253a7d;
  box-shadow: 0 4px 16px #253a7d22;
  transform: scale(1.03);
}

.logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}

.logo {
  width: 40px;
  height: 40px;
  margin-bottom: 4px;
}

.bank-name {
  font-weight: 700;
  color: #c59a1a;
  font-size: 1.03em;
  margin-bottom: 2px;
}

.product-name {
  font-weight: bold;
  font-size: 1.08em;
  margin-bottom: 12px;
  color: #222;
}

.product-info {
  display: flex;
  justify-content: space-between;
  font-size: 1em;
  color: #333;
}

.rate {
  font-weight: 600;
}

.period {
  color: #888;
}

.guide-text {
  text-align: center;
  margin: 12px 0 0 0;
  color: #555;
  font-size: 1em;
  font-weight: 400;
}

.btn-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin: 18px 0 0 0;
}

.reset-btn {
  background: #fff;
  color: #253a7d;
  border: 1px solid #bfc5d1;
  border-radius: 6px;
  padding: 7px 20px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.compare-btn {
  background: #253a7d;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 7px 26px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.compare-btn:disabled {
  background: #bfc5d1;
  color: #fff;
  cursor: not-allowed;
}

.compare-table-wrap {
  margin: 32px auto 0 auto;
  max-width: 1100px;
  padding: 0 0 40px 0;
}

.compare-table {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #e5eaf0cc;
  width: 100%;
  max-width: 950px;   /* 기존 800px → 950px */
  margin: 0 auto 18px auto;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 1.00em;
}

.compare-table th,
.compare-table td {
  padding: 18px 24px;
  border-bottom: 1px solid #f1f2f4;
}

.compare-table th {
  font-size: 1.08em;
  font-weight: 700;
  color: #253a7d;
  background: #f5eedd;
}

.compare-table td:first-child {
  text-align: right;
  color: #333;
  font-weight: 600;
}

.compare-table tr:last-child td {
  border-bottom: none;
}

.back-btn {
  display: block;
  margin: 0 auto;
  background: #253a7d;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 36px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

@media (max-width: 700px) {
  .card-area {
    flex-direction: column;
    align-items: center;
    max-width: 100vw;
    padding: 18px 0 12px 0;
    gap: 16px;
  }
  .product-card {
    width: 98vw;    /* 기존 92vw → 98vw */
    min-width: 0;
  }
  .compare-table {
    font-size: 0.98em;
    padding: 0;
    max-width: 99vw;
  }
}
</style>
