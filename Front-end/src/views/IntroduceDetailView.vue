<template>
  <div class="product-detail-container">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>상품 정보를 불러오는 중입니다...</p>
    </div>
    
    <div v-else-if="product" class="product-detail">
      <!-- 상품 헤더 -->
      <div class="product-header">
        <div class="header-content">
          <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>
          <button 
            @click="toggleSaveProduct" 
            class="heart-button"
            :class="{ 'saved': isProductSaved }"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" 
                    :fill="isProductSaved ? '#ff4757' : 'none'" 
                    :stroke="isProductSaved ? '#ff4757' : '#666'" 
                    stroke-width="2"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- 메인 정보 카드 -->
      <div class="main-info-card">
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">금융기관</div>
            <div class="info-value bank-name">{{ product.kor_co_nm }}</div>
          </div>
          <div class="info-item">
            <div class="info-label">이자방식</div>
            <div class="info-value">단리</div>
          </div>
          <div class="info-item">
            <div class="info-label">금리</div>
            <div class="info-value rate-info">
              최저 연 <span class="rate">{{ getMinRate() }}%</span> ~ 최고 연 <span class="rate">{{ getMaxRate() }}%</span>
            </div>
          </div>
          <div class="info-item">
            <div class="info-label">가입기간</div>
            <div class="info-value">{{ getJoinPeriod() }}</div>
          </div>
          <div class="info-item">
            <div class="info-label">가입방법</div>
            <div class="info-value">{{ getJoinMethods() }}</div>
          </div>
        </div>

        <!-- 상품 특징 태그들 -->
        <div class="feature-tags">
          <a href="#" class="tag">채팅상담</a>
          <a href="#" class="tag">Email상담</a>
          <a href="#" class="tag">전화예약</a>
          <a href="#" class="tag">가입안내</a>
          <RouterLink :to="`/searchbank/${product.kor_co_nm}`"  target="_blank" class="tag">은행찾기</RouterLink>
        </div>

        <!-- 이자 계산기 섹션 -->
        <div class="calculator-section">
          <div class="calculator-row">
            <span class="calc-label">이 상품을</span>
            <select v-model="selectedPeriod" class="period-select" @change="updateRate">
              <option v-for="period in availablePeriods" :key="period.save_trm" :value="period.save_trm">
                {{ period.save_trm }}
              </option>
            </select>
            <span class="calc-text">개월</span>
            <input 
              v-model="depositAmount" 
              type="text" 
              class="amount-input"
              @input="formatAmount"
            />
            <span class="calc-text">원으로 금리 연</span>
            <span class="selected-rate">{{ getMaxRate() }}</span>
            <span class="calc-text">% 적용하면 받게 될 돈은?</span>
          </div>
          
          <div class="result-section">
            <div class="result-label">결과보기</div>
          </div>
          
          <div class="final-result">
            <span class="result-text">세전</span>
            <span class="result-amount">{{ formatNumber(calculateResult()) }}</span>
          </div>
        </div>
      </div>

      <!-- 상품설명 섹션 -->
      <div class="product-description-section">
        <div class="section-header">
          <h2 class="section-title">상품설명</h2>
        </div>
        
        <div class="description-content">
          <div class="description-row">
            <div class="description-label">상품특징</div>
            <div class="description-value">
              <div v-if="summaryLoading" class="summary-loading">요약 정보를 불러오는 중...</div>
              <div v-else-if="summaryError" class="summary-error">{{ summaryError }}</div>
              <div v-else-if="productSummary" class="summary-content">{{ productSummary }}</div>
              <div v-else>상품 특징 정보가 없습니다.</div>
            </div>
          </div>
          
          <div class="description-row">
            <div class="description-label">가입대상</div>
            <div class="description-value">{{ product.join_member || '개인' }}</div>
          </div>
          
          <div class="description-row">
            <div class="description-label">가입기간</div>
            <div class="description-value">{{ getDetailedPeriods() }}</div>
          </div>
          
          <div class="description-row">
            <div class="description-label">가입금액</div>
            <div class="description-value">{{ getJoinAmount() }}</div>
          </div>
          
          <div class="description-row">
            <div class="description-label">상품과목</div>
            <div class="description-value">예금</div>
          </div>

          <div class="description-row">
            <div class="description-label">이자지급방법</div>
            <div class="description-value">
              <div>우대금리</div>
              <div>만기 후 금리</div>
            </div>
          </div>

          <div class="description-row">
            <div class="description-label">가입안내</div>
            <div class="description-value">영업점, 비대면 채널</div>
          </div>
        </div>
      </div>

      <!-- 목록으로 버튼 -->
      <div class="action-section">
        <button @click="$router.back()" class="back-button">
          목록으로
        </button>
      </div>
    </div>
    
    <div v-else class="error">
      <p>상품 정보를 찾을 수 없습니다.</p>
      <button @click="$router.back()" class="back-btn">
        목록으로 돌아가기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const product = ref(null)
const options = ref([])
const productType = ref('')
const loading = ref(true)

// 하트 버튼 관련 데이터
const isProductSaved = ref(false)

// 계산기 관련 데이터
const selectedPeriod = ref(12)
const depositAmount = ref('1,000,000')
const selectedRate = ref('2.65')

// 새로 추가: 상품 요약 관련 데이터
const productSummary = ref('')
const summaryLoading = ref(false)
const summaryError = ref(null)

// 계산된 속성들
const availablePeriods = computed(() => {
  return options.value.length > 0 ? options.value : [{ save_trm: 12, intr_rate2: 2.65 }]
})

// 상품 요약 정보를 가져오는 함수
const fetchProductSummary = async (fin_prdt_cd) => {
  if (!fin_prdt_cd) return
  
  summaryLoading.value = true
  summaryError.value = null
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/deposits/summarize/${fin_prdt_cd}`)
    
    if (response.ok) {
      const data = await response.json()
      // 따옴표 제거하고 summary만 추출
      productSummary.value = data.summary ? data.summary.replace(/"/g, '') : '상품 특징 정보가 없습니다.'
    } else {
      summaryError.value = '요약 정보를 불러올 수 없습니다.'
    }
  } catch (error) {
    console.error('상품 요약 정보 가져오기 실패:', error)
    summaryError.value = '요약 정보를 불러오는 중 오류가 발생했습니다.'
  } finally {
    summaryLoading.value = false
  }
}

// 로컬스토리지 관련 메서드
const getSavedProducts = () => {
  const saved = localStorage.getItem('savedFinanceProducts')
  return saved ? JSON.parse(saved) : []
}

const saveProductToStorage = (productData) => {
  const savedProducts = getSavedProducts()
  const productExists = savedProducts.some(p => p.fin_prdt_cd === productData.fin_prdt_cd)
  
  if (!productExists) {
    savedProducts.push(productData)
    localStorage.setItem('savedFinanceProducts', JSON.stringify(savedProducts))
  }
}

const removeProductFromStorage = (fin_prdt_cd) => {
  const savedProducts = getSavedProducts()
  const filteredProducts = savedProducts.filter(p => p.fin_prdt_cd !== fin_prdt_cd)
  localStorage.setItem('savedFinanceProducts', JSON.stringify(filteredProducts))
}

const checkIfProductSaved = () => {
  if (!product.value) return false
  const savedProducts = getSavedProducts()
  return savedProducts.some(p => p.fin_prdt_cd === product.value.fin_prdt_cd)
}

// 하트 버튼 토글 메서드 - 경고창으로 변경
const toggleSaveProduct = () => {
  if (!product.value) return
  
  const savedProducts = getSavedProducts()
  
  if (isProductSaved.value) {
    // 이미 저장된 상품이면 제거
    removeProductFromStorage(product.value.fin_prdt_cd)
    isProductSaved.value = false
  } else {
    // 저장되지 않은 상품이면 추가 시도
    if (savedProducts.length >= 3) {
      alert('담기는 최대 3개까지 가능합니다.')
      return
    }
    
    const productData = {
      etc_note: product.value.etc_note || '',
      fin_prdt_cd: product.value.fin_prdt_cd,
      fin_prdt_nm: product.value.fin_prdt_nm,
      join_deny: product.value.join_deny || '개인',
      join_member: product.value.join_member || '개인',
      join_way: product.value.join_way || '영업점, 비대면 채널',
      kor_co_nm: product.value.kor_co_nm,
      max_intr: product.max_intr || 2.65,
      mtrt_int: product.value.mtrt_int || 2.65,
      spcl_cnd: product.value.spcl_cnd || '',
      type: productType.value,
      user_count: product.value.user_count || 0,
      savedAt: new Date().toISOString()
    }
    
    saveProductToStorage(productData)
    isProductSaved.value = true
  }
}

// 기존 메서드들
const getMinRate = () => {
  if (options.value.length === 0) return '2.65'
  const rates = options.value.map(opt => parseFloat(opt.intr_rate || opt.intr_rate2))
  return Math.min(...rates).toFixed(2)
}

const getMaxRate = () => {
  if (options.value.length === 0) return '2.65'
  const rates = options.value.map(opt => parseFloat(opt.intr_rate || opt.intr_rate2))
  return Math.max(...rates).toFixed(2)
}

const getJoinPeriod = () => {
  return '3년이내'
}

const getJoinMethods = () => {
  return '스마트폰, 인터넷'
}

const getDetailedPeriods = () => {
  if (options.value.length === 0) return '12개월 이상 36개월 이내 (월 단위)'
  const periods = options.value.map(opt => opt.save_trm)
  const min = Math.min(...periods)
  const max = Math.max(...periods)
  return `${min}개월 이상 ${max}개월 이내 (월 단위)`
}

const getJoinAmount = () => {
  return '10만원 이상 1억원 이하 (1만원 단위)'
}

const formatAmount = () => {
  let value = depositAmount.value.replace(/[^\d]/g, '')
  if (value) {
    value = parseInt(value).toLocaleString()
    depositAmount.value = value
  }
}

const formatNumber = (num) => {
  return parseInt(num).toLocaleString()
}

const updateRate = () => {
  const selectedOption = options.value.find(opt => opt.save_trm == selectedPeriod.value)
  if (selectedOption) {
    selectedRate.value = selectedOption.intr_rate2 || selectedOption.intr_rate || '2.65'
  }
}

const calculateResult = () => {
  const principal = parseInt(depositAmount.value.replace(/[^\d]/g, '')) || 1000000
  const rate = parseFloat(selectedRate.value) / 100
  const months = parseInt(selectedPeriod.value)
  
  // 단리 계산: 원금 × (1 + 연이율 × 기간/12)
  const result = principal * (1 + rate * months / 12)
  
  // 세금 15.4% 적용
  const interest = result - principal
  const taxedInterest = interest * (1 - 0.154)
  const finalResult = principal + taxedInterest
  
  return finalResult
}

const fetchDataSeparately = async (fin_prdt_cd, type) => {
  try {
    const productUrl = type === 'deposit'
      ? 'http://127.0.0.1:8000/deposits/save/'
      : 'http://127.0.0.1:8000/deposits/save2/'
    
    const productRes = await fetch(productUrl)
    const productList = await productRes.json()
    product.value = productList.find(p => p.fin_prdt_cd === fin_prdt_cd)
    
    const optionUrl = type === 'deposit'
      ? 'http://127.0.0.1:8000/deposits/depositoptions/'
      : 'http://127.0.0.1:8000/deposits/savingoptions/'
    
    const optionRes = await fetch(optionUrl)
    const optionList = await optionRes.json()
    
    options.value = optionList.filter(option => option.fin_prdt_cd === fin_prdt_cd)
    
    if (options.value.length > 0) {
      selectedPeriod.value = options.value[0].save_trm
      selectedRate.value = options.value[0].intr_rate2 || options.value[0].intr_rate
    }
  } catch (error) {
    console.error('데이터 가져오기 실패:', error)
  }
}

onMounted(async () => {
  const { fin_prdt_cd, type } = route.params
  productType.value = type
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/products/${type}/${fin_prdt_cd}/`)
    
    if (response.ok) {
      const data = await response.json()
      product.value = data.product
      options.value = data.options
      productType.value = data.product_type
      
      // 상품 정보 로드 후 저장 상태 확인
      isProductSaved.value = checkIfProductSaved()
      
      if (options.value.length > 0) {
        selectedPeriod.value = options.value[0].save_trm
        selectedRate.value = options.value[0].intr_rate2 || options.value[0].intr_rate
      }
    } else {
      await fetchDataSeparately(fin_prdt_cd, type)
      isProductSaved.value = checkIfProductSaved()
    }
    
    // 상품 정보 로드 후 요약 정보도 가져오기
    await fetchProductSummary(fin_prdt_cd)
    
  } catch (error) {
    console.error('통합 API 호출 실패:', error)
    await fetchDataSeparately(fin_prdt_cd, type)
    isProductSaved.value = checkIfProductSaved()
    await fetchProductSummary(fin_prdt_cd)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.product-detail-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0;
  font-family: 'Noto Sans KR', sans-serif;
  background-color: #f0f0f0;
}

.loading {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.product-detail {
  border-radius: 0;
  overflow: hidden;
}

.product-header {
  padding: 20px 30px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
}

.product-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
  flex: 1;
}

.heart-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.heart-button:hover {
  background-color: #f5f5f5;
  transform: scale(1.1);
}

.heart-button.saved {
  animation: heartBeat 0.6s ease-in-out;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  25% { transform: scale(1.2); }
  50% { transform: scale(1); }
  75% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.main-info-card {
  margin-bottom: 50px;
  background: #f8f4e6;
  padding: 25px 30px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.info-item {
  text-align: center;
}

.info-label {
  display: block;
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}

.info-value {
  display: block;
  font-size: 13px;
  color: #333;
  font-weight: 500;
  line-height: 1.3;
}

.bank-name {
  font-weight: bold;
  color: #1976d2;
}

.rate {
  color: #d32f2f;
  font-weight: bold;
}

.feature-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 25px;
  flex-wrap: wrap;
  justify-content: center;
}

.tag {
  background: white;
  color: #666;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  border: 1px solid #ddd;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.tag:hover {
  background-color: #f0f0f0;
  color: #333;
}

.calculator-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.calculator-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.calc-label, .calc-text {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
}

.period-select {
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background: white;
  min-width: 60px;
}

.amount-input {
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 100px;
  text-align: right;
}

.selected-rate {
  font-size: 14px;
  font-weight: bold;
  color: #d32f2f;
}

.result-section {
  text-align: center;
  margin-bottom: 10px;
}

.result-label {
  font-size: 14px;
  color: #666;
  text-decoration: underline;
  cursor: pointer;
}

.final-result {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.result-text {
  font-size: 14px;
  color: #333;
}

.result-amount {
  font-size: 20px;
  font-weight: bold;
  color: #1976d2;
}

.product-description-section {
  background: white;
}

.section-header {
  background: #3b4a6b;
  color: white;
  padding: 15px 30px;
  margin: 0;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
}

.description-content {
  padding: 0;
}

.description-row {
  display: grid;
  grid-template-columns: 140px 1fr;
  padding: 15px 30px;
  border-bottom: 1px solid #eee;
  align-items: start;
}

.description-row:last-child {
  border-bottom: none;
}

.description-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.description-value {
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}

.description-value > div {
  margin-bottom: 2px;
}

.description-value > div:last-child {
  margin-bottom: 0;
}

.summary-loading {
  color: #666;
  font-style: italic;
}

.summary-error {
  color: #d32f2f;
  font-size: 13px;
}

.summary-content {
  line-height: 1.5;
  color: #333;
}

.action-section {
  padding: 30px;
  text-align: center;
  background: white;
}

.back-button {
  background: #3b4a6b;
  color: white;
  border: none;
  padding: 12px 40px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background: #2c3a56;
}

.error {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.back-btn {
  background: #3b4a6b;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 20px;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .product-detail-container {
    padding: 0;
  }
  
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .heart-button {
    align-self: flex-end;
  }
  
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .calculator-row {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  
  .amount-input {
    width: 100%;
  }
  
  .description-row {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 15px 20px;
  }
  
  .product-header, .main-info-card, .section-header, .action-section {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .product-title {
    font-size: 20px;
  }
  
  .feature-tags {
    justify-content: center;
  }
}
</style>
