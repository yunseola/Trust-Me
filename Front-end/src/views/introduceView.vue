<template>
  <div class="finance-products-page">
    <!-- 상단 필터 바 -->
    <div class="filter-bar-new">
      <div class="main-filter-buttons">
        <button
          v-for="category in filterCategories"
          :key="category.id"
          :class="['main-filter-btn', { active: activeFilterPanel === category.id }]"
          @click="toggleFilterPanel(category.id)"
        >
          {{ category.label }}
        </button>
      </div>

      <!-- 각 필터 패널을 개별적으로 표시 -->
      <div v-if="activeFilterPanel === 'productType'" class="detail-filter-panel">
        <h4>상품 종류</h4>
        <div class="detail-options-container">
          <button
            v-for="option in productTypeOptions"
            :key="option.value"
            :class="['detail-option-btn', { active: tempFilters.productType === option.value }]"
            @click="toggleDetailOption('productType', option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <div class="detail-actions">
          <button class="detail-cancel-btn" @click="cancelDetailFilter">취소하기</button>
          <button class="detail-apply-btn" @click="applyDetailFilter">적용하기</button>
        </div>
      </div>

      <div v-if="activeFilterPanel === 'interestRate'" class="detail-filter-panel">
        <h4>금리 조건</h4>
        <div class="detail-options-container">
          <button
            v-for="option in interestRateOptions"
            :key="option.value"
            :class="['detail-option-btn', { active: tempFilters.interestRate === option.value }]"
            @click="toggleDetailOption('interestRate', option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <div class="detail-actions">
          <button class="detail-cancel-btn" @click="cancelDetailFilter">취소하기</button>
          <button class="detail-apply-btn" @click="applyDetailFilter">적용하기</button>
        </div>
      </div>

      <div v-if="activeFilterPanel === 'bank'" class="detail-filter-panel">
        <h4>금융기관</h4>
        <div class="detail-options-container">
          <button
            v-for="option in bankOptions"
            :key="option.value"
            :class="['detail-option-btn', { active: tempFilters.bank.includes(option.value) }]"
            @click="toggleDetailOption('bank', option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <div class="detail-actions">
          <button class="detail-cancel-btn" @click="cancelDetailFilter">취소하기</button>
          <button class="detail-apply-btn" @click="applyDetailFilter">적용하기</button>
        </div>
      </div>

      <div v-if="activeFilterPanel === 'maturity'" class="detail-filter-panel">
        <h4>만기 기간 (단위: 개월)</h4>
        <div class="detail-options-container">
          <button
            v-for="option in maturityOptions"
            :key="option.value"
            :class="['detail-option-btn', { active: tempFilters.maturity.includes(option.value) }]"
            @click="toggleDetailOption('maturity', option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <div class="detail-actions">
          <button class="detail-cancel-btn" @click="cancelDetailFilter">취소하기</button>
          <button class="detail-apply-btn" @click="applyDetailFilter">적용하기</button>
        </div>
      </div>

      <div v-if="activeFilterPanel === 'method'" class="detail-filter-panel">
        <h4>가입 방법</h4>
        <div class="detail-options-container">
          <button
            v-for="option in methodOptions"
            :key="option.value"
            :class="['detail-option-btn', { active: tempFilters.method.includes(option.value) }]"
            @click="toggleDetailOption('method', option.value)"
          >
            {{ option.label }}
          </button>
        </div>
        <div class="detail-actions">
          <button class="detail-cancel-btn" @click="cancelDetailFilter">취소하기</button>
          <button class="detail-apply-btn" @click="applyDetailFilter">적용하기</button>
        </div>
      </div>

      <div class="global-actions">
        <button class="global-reset-btn" @click="resetAllFilters">초기화</button>
        <button class="global-search-btn" @click="executeSearch">검색</button>
      </div>
    </div>

    <!-- 결과 요약 및 정렬 -->
    <div class="result-summary">
      <div class="result-info">
        <span class="result-count">{{ filteredProducts.length }}개의 상품이 검색되었습니다. (총 {{ allProducts.length }}건)</span>
        <span></span>
        <p>비교하고 싶은 상품이나 마음에 드는 상품을 최대 3개까지 선택하여 마이페이지에서 확인하실 수 있습니다.</p>
      </div>
      <div class="sort-controls">
        <select v-model="sortBy" @change="applySorting" class="sort-select">
          <option value="name">이름순</option>
          <option value="maturity-long">만기 긴순</option>
          <option value="maturity-short">만기 짧은순</option>
          <option value="rate-high">금리 높은순</option>
          <option value="rate-low">금리 낮은순</option>
        </select>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading-state">
      <div class="loader"></div>
      <p>상품 정보를 불러오는 중...</p>
    </div>

    <!-- 상품 목록 -->
    <div v-else class="products-container">
      <div class="products-list-new">
        <!-- 일반 상품 목록 -->
        <div class="products-section">
          <div
            v-for="product in paginatedProducts"
            :key="product.fin_prdt_cd + product.type"
            class="product-item"
          >
            <div class="product-header">
              <span :class="['type-badge', product.type]">
                {{ product.type === 'deposit' ? '예금' : '적금' }}
              </span>
              <button
                v-if="!isSaved(product)"
                @click="handleSaveProduct(product)"
                :disabled="isLoggedIn && savedProducts.length >= 3"
                class="save-heart-btn"
              >
                ♡
              </button>
              <button
                v-else
                @click="removeProduct(product)"
                class="save-heart-btn saved"
              >
                ♥
              </button>
            </div>
            <div class="product-content">
              <h4 class="product-name">{{ product.fin_prdt_nm }}</h4>
              <p class="bank-name">{{ product.kor_co_nm }}</p>
              <div class="rate-display">
                <span class="rate-label">최고</span>
                <span class="rate-value">{{ product.max_intr }}%</span>
              </div>
              <div class="method-tags">
                <span 
                  v-for="method in getJoinMethods(product.join_way)"
                  :key="method"
                  class="method-tag"
                >
                  {{ method }}
                </span>
              </div>
              <button 
  class="compare-btn" 
  @click="$router.push(`/introduce/${product.type}/${product.fin_prdt_cd}`)">
  <span class="compare-btn-link">상세정보</span>
</button>

            </div>
          </div>
        </div>

        <!-- 페이지네이션 -->
        <div v-if="totalPages > 1" class="pagination">
          <button @click="currentPage = 1" :disabled="currentPage === 1" class="page-btn">처음</button>
          <button @click="currentPage--" :disabled="currentPage === 1" class="page-btn">이전</button>
          <span
            v-for="page in visiblePages"
            :key="page"
            :class="['page-number', { active: currentPage === page }]"
            @click="currentPage = page"
          >{{ page }}</span>
          <button @click="currentPage++" :disabled="currentPage === totalPages" class="page-btn">다음</button>
          <button @click="currentPage = totalPages" :disabled="currentPage === totalPages" class="page-btn">마지막</button>
        </div>
      </div>
    </div>

    <!-- 로그인 필요 모달 -->
    <div v-if="showLoginModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>로그인이 필요합니다</h3>
        <p>로그인한 유저만 담기가 가능합니다.</p>
        <div class="modal-buttons">
          <button @click="goToLogin" class="login-btn">로그인하기</button>
          <button @click="closeModal" class="cancel-btn">취소</button>
        </div>
      </div>
    </div>

    <!-- 담기 제한 모달 -->
    <div v-if="showLimitModal" class="modal-overlay" @click="closeLimitModal">
      <div class="modal-content" @click.stop>
        <h3>담기 제한</h3>
        <p>담기는 3개만 가능합니다.<br>기존 상품을 삭제한 후 다시 시도해주세요.</p>
        <div class="modal-buttons">
          <button @click="closeLimitModal" class="cancel-btn">확인</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 상태 관리
const allProducts = ref([])
const savedProducts = ref([])
const isLoading = ref(false)
const error = ref(null)
const showLoginModal = ref(false)
const showLimitModal = ref(false)
const sortBy = ref('name')

// 페이지네이션
const currentPage = ref(1)
const itemsPerPage = ref(6)

const STORAGE_KEY = 'savedFinanceProducts'

// 필터 상태
const activeFilterPanel = ref(null)

const initialTempFilters = () => ({
  productType: null,
  interestRate: null,
  bank: [],
  maturity: [],
  method: []
})

const tempFilters = ref(initialTempFilters())
const appliedFilters = ref(initialTempFilters())

// 필터 옵션들
const productTypeOptions = ref([
  { label: '예금', value: 'deposit' },
  { label: '적금', value: 'saving' }
])

const interestRateOptions = ref([
  { label: '~ 1%', value: '0-1' },
  { label: '1% ~ 2%', value: '1-2' },
  { label: '2% ~ 3%', value: '2-3' },
  { label: '3% ~ 4%', value: '3-4' },
  { label: '4% ~ 5%', value: '4-5' },
  { label: '5% ~', value: '5-99' }
])

const bankOptions = ref([])

const maturityOptions = ref([
  { label: '~ 6', value: '0-6' },
  { label: '6 ~ 12', value: '6-12' },
  { label: '12 ~ 24', value: '12-24' },
  { label: '24 ~ 36', value: '24-36' },
  { label: '36 ~', value: '36-999' }
])

const methodOptions = ref([
  { label: '영업점', value: 'branch' },
  { label: '인터넷', value: 'internet' },
  { label: '스마트폰', value: 'mobile' }
])

// 필터 카테고리 정의
const filterCategories = computed(() => [
  { id: 'productType', label: '상품 종류' },
  { id: 'interestRate', label: '금리 조건' },
  { id: 'bank', label: '금융기관' },
  { id: 'maturity', label: '만기 기간' },
  { id: 'method', label: '가입 방법' }
])

// 로그인 상태 확인
const isLoggedIn = computed(() => {
  const token = localStorage.getItem('authToken')
  const user = localStorage.getItem('user')
  return !!(token && user)
})

// 가입방법 파싱 함수
function getJoinMethods(joinWayString) {
  if (!joinWayString) return []
  
  const methods = []
  const lowerStr = joinWayString.toLowerCase()
  
  if (lowerStr.includes('영업점')) methods.push('영업점')
  if (lowerStr.includes('인터넷')) methods.push('인터넷')
  if (lowerStr.includes('스마트폰') || lowerStr.includes('모바일')) methods.push('스마트폰')
  
  return methods
}

// 만기 기간 추출 함수
function getMaxMaturity(product) {
  const options = product.type === 'deposit' ? product.deposit_options : product.saving_options
  if (!options || options.length === 0) return 0
  return Math.max(...options.map(opt => parseInt(opt.save_trm) || 0))
}

// 정렬 함수
function applySorting() {
  currentPage.value = 1
}

// 필터 관련 함수들
function toggleFilterPanel(panelId) {
  if (activeFilterPanel.value === panelId) {
    activeFilterPanel.value = null
  } else {
    activeFilterPanel.value = panelId
    // 현재 적용된 필터 값으로 임시 필터 초기화
    if (panelId === 'productType' || panelId === 'interestRate') {
      tempFilters.value[panelId] = appliedFilters.value[panelId]
    } else {
      tempFilters.value[panelId] = [...appliedFilters.value[panelId]]
    }
  }
}

function toggleDetailOption(categoryId, optionValue) {
  if (categoryId === 'productType' || categoryId === 'interestRate') {
    // 단일 선택
    if (tempFilters.value[categoryId] === optionValue) {
      tempFilters.value[categoryId] = null
    } else {
      tempFilters.value[categoryId] = optionValue
    }
  } else {
    // 다중 선택
    const currentSelection = tempFilters.value[categoryId] || []
    const index = currentSelection.indexOf(optionValue)
    if (index > -1) {
      currentSelection.splice(index, 1)
    } else {
      currentSelection.push(optionValue)
    }
    tempFilters.value[categoryId] = currentSelection
  }
}

function applyDetailFilter() {
  if (activeFilterPanel.value) {
    const categoryId = activeFilterPanel.value
    if (categoryId === 'productType' || categoryId === 'interestRate') {
      appliedFilters.value[categoryId] = tempFilters.value[categoryId]
    } else {
      appliedFilters.value[categoryId] = [...(tempFilters.value[categoryId] || [])]
    }
  }
  activeFilterPanel.value = null
  currentPage.value = 1
}

function cancelDetailFilter() {
  if (activeFilterPanel.value) {
    const categoryId = activeFilterPanel.value
    if (categoryId === 'productType' || categoryId === 'interestRate') {
      tempFilters.value[categoryId] = appliedFilters.value[categoryId]
    } else {
      tempFilters.value[categoryId] = [...(appliedFilters.value[categoryId] || [])]
    }
  }
  activeFilterPanel.value = null
}

function resetAllFilters() {
  tempFilters.value = initialTempFilters()
  appliedFilters.value = initialTempFilters()
  activeFilterPanel.value = null
  currentPage.value = 1
}

function executeSearch() {
  currentPage.value = 1
}

// 필터링 및 정렬된 상품 목록
const filteredProducts = computed(() => {
  let filtered = [...allProducts.value]

  // 상품 타입 필터
  if (appliedFilters.value.productType) {
    filtered = filtered.filter(product => product.type === appliedFilters.value.productType)
  }

  // 금리 조건 필터
  if (appliedFilters.value.interestRate) {
    const [minRateStr, maxRateStr] = appliedFilters.value.interestRate.split('-')
    const minRate = parseFloat(minRateStr)
    const maxRate = parseFloat(maxRateStr)
    filtered = filtered.filter(product => {
      const intr = parseFloat(product.max_intr)
      return intr >= minRate && (maxRate === 99 ? true : intr < maxRate)
    })
  }
  
  // 은행 필터
  if (appliedFilters.value.bank && appliedFilters.value.bank.length > 0) {
    filtered = filtered.filter(product => appliedFilters.value.bank.includes(product.kor_co_nm))
  }

  // 가입방법 필터
  if (appliedFilters.value.method && appliedFilters.value.method.length > 0) {
    filtered = filtered.filter(product => {
      const productMethods = getJoinMethods(product.join_way)
      return appliedFilters.value.method.some(method => {
        if (method === 'branch') return productMethods.includes('영업점')
        if (method === 'internet') return productMethods.includes('인터넷')
        if (method === 'mobile') return productMethods.includes('스마트폰')
        return false
      })
    })
  }

  // 정렬 적용
  return filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.fin_prdt_nm.localeCompare(b.fin_prdt_nm)
      case 'maturity-long':
        return getMaxMaturity(b) - getMaxMaturity(a)
      case 'maturity-short':
        return getMaxMaturity(a) - getMaxMaturity(b)
      case 'rate-high':
        return parseFloat(b.max_intr) - parseFloat(a.max_intr)
      case 'rate-low':
        return parseFloat(a.max_intr) - parseFloat(b.max_intr)
      default:
        return 0
    }
  })
})

// 페이지네이션 계산
const totalPages = computed(() => Math.ceil(filteredProducts.value.length / itemsPerPage.value))

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredProducts.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

// 상품 관리 함수들
function loadSavedProducts() {
  if (isLoggedIn.value) {
    const data = localStorage.getItem(STORAGE_KEY)
    savedProducts.value = data ? JSON.parse(data) : []
  } else {
    savedProducts.value = []
  }
}

function isSaved(product) {
  if (!isLoggedIn.value) return false
  return savedProducts.value.some(
    p => p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type
  )
}

function handleSaveProduct(product) {
  if (!isLoggedIn.value) {
    showLoginModal.value = true
    return
  }
  saveProduct(product)
}

function saveProduct(product) {
  if (!isLoggedIn.value) return
  
  // 3개 이상일 때 모달 표시
  if (savedProducts.value.length > 3 && !isSaved(product)) {
    showLimitModal.value = true
    return
  }
  
  if (!isSaved(product)) {
    savedProducts.value.push(product)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(savedProducts.value))
  }
}

function removeProduct(product) {
  if (!isLoggedIn.value) return
  savedProducts.value = savedProducts.value.filter(
    p => !(p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type)
  )
  localStorage.setItem(STORAGE_KEY, JSON.stringify(savedProducts.value))
}

function closeModal() {
  showLoginModal.value = false
}

function closeLimitModal() {
  showLimitModal.value = false
}

function goToLogin() {
  showLoginModal.value = false
  router.push('/login')
}

// 상품 데이터 가져오기
async function fetchProducts() {
  isLoading.value = true
  error.value = null
  try {
    // 예금 상품 가져오기
    const depositRes = await fetch('http://127.0.0.1:8000/deposits/save/')
    if (!depositRes.ok) throw new Error('예금 상품 데이터를 불러올 수 없습니다.')
    const deposits = await depositRes.json()

    // 적금 상품 가져오기
    const savingRes = await fetch('http://127.0.0.1:8000/deposits/save2/')
    if (!savingRes.ok) throw new Error('적금 상품 데이터를 불러올 수 없습니다.')
    const savings = await savingRes.json()

    // 데이터 합치기
    allProducts.value = [
      ...deposits.map(item => ({ ...item, type: 'deposit' })),
      ...savings.map(item => ({ ...item, type: 'saving' }))
    ]
    
    // 은행 옵션 동적 생성 (중복 제거)
    const uniqueBanks = [...new Set(allProducts.value.map(product => product.kor_co_nm))]
      .filter(bank => bank) // null/undefined 제거
      .sort()
    
    bankOptions.value = uniqueBanks.map(bank => ({
      label: bank,
      value: bank
    }))

  } catch (err) {
    error.value = err.message
    console.error('상품 데이터 로딩 실패:', err)
  } finally {
    isLoading.value = false
  }
}

watch(appliedFilters, () => {
  currentPage.value = 1
}, { deep: true })

onMounted(async () => {
  loadSavedProducts()
  await fetchProducts()
})
</script>

<style scoped>
.finance-products-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

/* 필터 바 스타일 */
.filter-bar-new {
  background-color: #FDFBF5;
  border-radius: 12px;
  padding: 25px 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.main-filter-buttons {
  display: flex;
  justify-content: space-around;
  gap: 15px;
  margin-bottom: 20px;
}

.main-filter-btn {
  padding: 12px 24px;
  border: 1px solid #E0E0E0;
  border-radius: 25px;
  background-color: #FFFFFF;
  color: #555;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 15px;
  font-weight: 500;
  flex-grow: 1;
  text-align: center;
}

.main-filter-btn:hover {
  border-color: #22356F;
  color: #22356F;
  box-shadow: 0 2px 8px rgba(34, 53, 111, 0.1);
}

.main-filter-btn.active {
  background-color: #FFFFFF;
  color: #22356F;
  border: 2px solid #22356F;
  font-weight: 700;
  box-shadow: 0 2px 5px rgba(34, 53, 111, 0.15);
}

.detail-filter-panel {
  padding: 25px 15px;
  background-color: #FFFFFF;
  border-radius: 12px;
  margin: 20px 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.detail-filter-panel h4 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  text-align: left;
  padding-left: 5px;
}

.detail-options-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 25px;
  padding: 0 5px;
}

.detail-option-btn {
  padding: 10px 20px;
  border: 1px solid #D0D0D0;
  border-radius: 25px;
  background-color: #F7F7F7;
  color: #444;
  cursor: pointer;
  transition: all 0.25s ease;
  font-size: 14px;
  font-weight: 500;
}

.detail-option-btn:hover {
  border-color: #B0B0B0;
  background-color: #EDEDED;
}

.detail-option-btn.active {
  background-color: #22356F;
  color: white;
  border-color: #22356F;
  font-weight: 600;
}

.detail-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 5px;
  margin-top: 15px;
}

.detail-cancel-btn, .detail-apply-btn {
  padding: 12px 28px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: background-color 0.3s;
  border: none;
}

.detail-cancel-btn {
  background-color: #F0F0F0;
  color: #555;
}
.detail-cancel-btn:hover {
  background-color: #E5E5E5;
}

.detail-apply-btn {
  background-color: #22356F;
  color: white;
}
.detail-apply-btn:hover {
  background-color: #1A2A5A;
}

.global-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 25px;
}

.global-reset-btn, .global-search-btn {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: background-color 0.3s;
  min-width: 120px;
}

.global-reset-btn {
  background-color: #EAEAEA;
  color: #444;
}
.global-reset-btn:hover {
  background-color: #DADADA;
}

.global-search-btn {
  background-color: #22356F;
  color: white;
}
.global-search-btn:hover {
  background-color: #1A2A5A;
}

/* 결과 요약 및 정렬 */
.result-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px 0;
}

.result-count {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.sort-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid #D0D0D0;
  border-radius: 6px;
  background-color: white;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  min-width: 140px;
}

.sort-select:focus {
  outline: none;
  border-color: #22356F;
}

/* 새로운 상품 목록 스타일 */
.products-list-new {
  background-color: #F8F9FA;
  border-radius: 12px;
  padding: 20px;
}

/* 일반 상품 목록 */
.products-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.product-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.type-badge {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 12px;
  font-weight: 600;
}

.type-badge.deposit {
  background: #E3F2FD;
  color: #1E88E5;
}

.type-badge.saving {
  background: #E8F5E9;
  color: #43A047;
}

.save-heart-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #CCCCCC;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.save-heart-btn:hover {
  color: #FF6B6B;
}

.save-heart-btn.saved {
  color: #FF6B6B;
}

.product-content {
  text-align: left;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.bank-name {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
}

.rate-display {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.rate-label {
  font-size: 12px;
  color: #777;
}

.rate-value {
  font-size: 16px;
  font-weight: 700;
  color: #D32F2F;
}

.method-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 15px;
}

.method-tag {
  background: #F0F0F0;
  color: #666;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
}

.compare-btn {
  width: 100%;
  padding: 10px;
  background: #22356F;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.compare-btn:hover {
  background: #1A2A5A;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 30px;
}

.page-btn, .page-number {
  padding: 8px 12px;
  border: 1px solid #E0E0E0;
  background: white;
  cursor: pointer;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled), .page-number:hover:not(.active) {
  border-color: #22356F;
  color: #22356F;
}

.page-btn:disabled {
  background: #F5F5F5;
  color: #BBB;
  cursor: not-allowed;
}

.page-number.active {
  background: #22356F;
  color: white;
  border-color: #22356F;
  font-weight: bold;
}

/* 로딩 및 모달 */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  color: #555;
}

.loader {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #22356F;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 35px;
  border-radius: 10px;
  box-shadow: 0 5px 25px rgba(0,0,0,0.15);
  text-align: center;
  max-width: 420px;
  width: 90%;
}

.modal-content h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 20px;
  font-weight: 600;
}

.modal-content p {
  margin: 0 0 25px 0;
  color: #666;
  line-height: 1.6;
  font-size: 15px;
}

.modal-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.login-btn, .cancel-btn {
  border: none;
  padding: 10px 22px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.login-btn {
  background-color: #22356F;
  color: white;
}

.login-btn:hover {
  background-color: #1A2A5A;
}

.cancel-btn {
  background-color: #E0E0E0;
  color: #444;
}

.cancel-btn:hover {
  background-color: #D0D0D0;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .result-summary {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .sort-controls {
    justify-content: center;
  }
  
  .products-section {
    grid-template-columns: 1fr;
  }
  
  .main-filter-buttons {
    flex-direction: column;
  }
  
  .main-filter-btn {
    width: 100%;
    margin-bottom: 10px;
  }
}

@media (max-width: 480px) {
  .finance-products-page {
    padding: 15px;
  }
  
  .filter-bar-new {
    padding: 20px 15px;
  }
  
  .product-item {
    padding: 15px;
  }
}
</style>
