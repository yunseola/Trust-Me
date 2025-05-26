<template>
  <div class="background-layer"></div>

  <div class="page-content">
    <!-- 여기에 필터, 타이틀 등 모든 컨텐츠 -->
    <div class="filter-title-wrapper">
      <h2 class="filter-title">지금 나에게 <span class="point">딱</span> 맞는 금융상품, <span class="ai">AI</span>와 함께 찾아보세요</h2>
    </div>

    <div class="filter-box">
      <!-- 연령대 -->
      <div class="filter-section">
        <span class="label">연령대</span>
        <div class="option-buttons">
          <button
            v-for="age in ageOptions"
            :key="age"
            :class="{ active: selectedAge === age }"
            @click="selectedAge = age"
          >
            {{ age }}
          </button>
        </div>
      </div>

      <!-- 자산 -->
      <div class="filter-section">
        <span class="label">자산</span>
        <input type="range" min="0" max="7" step="1" v-model="selectedAsset" class="slider" />
        <div class="asset-labels">
          <span v-for="(label, index) in assetLabels" :key="index">{{ label }}</span>
        </div>
      </div>

      <!-- 목적 -->
      <div class="filter-section">
        <span class="label">목적</span>
        <div class="option-buttons">
          <button
            v-for="goal in goalOptions"
            :key="goal"
            :class="{ active: selectedGoal === goal }"
            @click="selectedGoal = goal"
          >
            {{ goal }}
          </button>
        </div>
      </div>

      <!-- 상품 -->
      <div class="filter-section">
        <span class="label">상품</span>
        <div class="option-buttons">
          <button
            v-for="product in productOptions"
            :key="product"
            :class="{ active: selectedProduct === product }"
            @click="selectedProduct = product"
          >
            {{ product }}
          </button>
        </div>
      </div>

      <!-- 버튼 -->
      <div class="button-group">
        <button class="reset-button" @click="resetFilter">초기화</button>
        <button class="search-button" @click="searchProducts">검색</button>
      </div>
    </div>
  </div>

  <!-- 로딩 중 표시 -->
<div v-if="isLoading" class="loading">
  🔄 추천 상품을 불러오는 중...
</div>

<div v-if="recommendationCards.length" class="recommend-container">
  <!-- 추천 조건 -->
  <div class="recommend-condition">
    <strong>{{ selectedAge }} / {{ assetLabels[selectedAsset] }} / {{ selectedGoal }}</strong>
    → 아래 상품을 추천합니다
  </div>

  <!-- 추천 카드들 -->
  <div class="recommend-cards">
    <div class="card" v-for="(item, index) in recommendationCards" :key="index">
      <div class="bank-header">
        <img :src="getBankLogo(item.kor_co_nm)" class="bank-logo" />
        <span class="bank-name">{{ item.kor_co_nm }}</span>
      </div>

      <div class="product-name">{{ item.fin_prdt_nm }}</div>

      <div class="rate-info">
        <div>연 {{ item.intr_rate2 }}%</div>
        <div>{{ item.save_trm || 12 }}개월</div>
      </div>

      <div class="card-buttons">
        <a class="detail-btn" @click="goToDetail(item.fin_prdt_cd)">상세 보기</a>
        <a class="apply-btn" @click="alert(item.spcl_cnd)">가입하기</a>
      </div>
    </div>
  </div>
</div>


  <div class="button-wrapper">
    <button class="go-home-btn" @click="goHome">
      홈으로
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import {getBankLogo} from '@/api/logos.js'

const router = useRouter();

const goToDetail = (code, type) => {
  const routeType = type === '예금' ? 'deposit' : 'saving';
  router.push(`/introduce/${routeType}/${code}`);
};


// 선택값 관련
const ageOptions = ['10대', '20대', '30대', '40대', '50대', '60대 이상'];
const assetLabels = ['0', '~300만', '~500만', '~1000만', '~3000만', '~5000만', '~1억', '1억 이상'];
const goalOptions = ['목돈 마련', '생활비', '단기 수익', '결혼', '주택', '노후 준비', '기타'];
const productOptions = ['예금', '적금'];

const selectedAge = ref('');
const selectedAsset = ref(0);
const selectedGoal = ref('');
const selectedProduct = ref('');

// 상태값
const isLoading = ref(false);
const recommendationCards = ref([]); // 정보 보기 위해 최종 정보를 저장

const resetFilter = () => {
  selectedAge.value = '';
  selectedAsset.value = 0;
  selectedGoal.value = '';
  selectedProduct.value = '';
  recommendationCards.value = [];
};

const searchProducts = async () => {
  isLoading.value = true;
  recommendationCards.value = [];

  const requestData = {
    age: selectedAge.value,
    asset: assetLabels[selectedAsset.value],
    goal: selectedGoal.value,
    type: selectedProduct.value
  };

  try {
    const res = await axios.post('http://localhost:8000/deposits/recommend/', requestData);
    recommendationCards.value = res.data.recommendation.slice(0, 3);
  } catch (err) {
    console.error('추천 실패:', err);
  } finally {
    isLoading.value = false;
  }
};

const goHome = () => router.push('/');
</script>

<style>
body {
  background-color: #edf0f2;
}
</style>

<style scoped>
body {
  margin: 0;
  padding: 0;
}

.filter-container {
  background: #f0f0f0;
  padding: 40px 20px;
  font-family: 'Pretendard', sans-serif;
  text-align: center;
}

.filter-title {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #222;
  max-width: 800px;
  margin: 0 auto 30px auto;
  text-align: left; /* ✅ 이 줄 추가로 전체 왼쪽 정렬 */
  font-weight: bold;
}

.filter-title .point {
  color: #2a2a9f;
  font-weight: 800;
  position: relative;
}

:deep(.filter-title .point::after) {
  content: "✓";
  position: absolute;
  top: -0.6em;
  right: -0.6em;
  color: #ffc700 !important;
  font-size: 0.7em;
  font-weight: bold;
}

.filter-title .ai {
  color: #2a2a9f;
  font-weight: 600;
}

.filter-box {
  background: #f5ead1;
  padding: 30px;
  border-radius: 10px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  text-align: left; /* ✅ 이 줄 추가로 전체 왼쪽 정렬 */
}

/* ✅ 가장 뒤에 깔릴 배경 박스 */
.background-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 350px; /* 높이는 원하는 만큼 조절 */
  background-color: rgba(204, 185, 141, 0.15);
  z-index: -1;
}

/* ✅ 콘텐츠는 위로 오게 하기 */
.page-content {
  position: relative;
  z-index: 1;
}

.filter-title-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.filter-section {
  margin-bottom: 7px;
  text-align: left;
}

.label {
  font-weight: 600;
  display: block;
  margin-bottom: 6px;
  font-size: 15px;
  color: #333;
}

.option-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 17px;
}

.option-buttons button {
  background: #f9f5ec;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: 0.2s;
  color: #444;
}

.option-buttons button.active {
  background: #2c3e94;
  color: white;
  font-weight: 600;
}

.slider {
  width: 100%;
  margin-top: 5px;
}

.asset-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #666;
  margin-top: 8px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

.reset-button, .search-button {
  background: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.search-button {
  background: #222;
  color: white;
}

.reset-button:hover, .search-button:hover {
  opacity: 0.9;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 10px; /* ✅ 버튼 그룹 위 간격 줄임 */
  }

.reset-button,
.search-button {
  padding: 8px 16px; /* ✅ 버튼 사이즈 축소 */
  font-size: 13px;
  border-radius: 4px;
}

.recommendation-box {
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 20px;
  margin-top: 30px;
  border-radius: 8px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.recommendation-box h3 {
  margin-bottom: 10px;
  font-size: 16px;
}

.recommendation-box ul {
  padding-left: 20px;
}

.recommendation-box li {
  margin-bottom: 12px;
  line-height: 1.5;
}

.loading {
  text-align: center;
  font-size: 15px;
  margin-top: 24px;
  font-weight: 500;
  color: #444;
}

.recommend-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start; /* 왼쪽 정렬 */
}

.card {
  width: 240px;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 16px;
  background: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.bank-header {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 8px;
  margin-bottom: 20px;
}

.bank-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.bank-logo {
  width: 26px;
  height: 26px;
  object-fit: contain;
}

.product-name {
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 10px;
}

.rate-info {
  font-size: 14px;
  color: #555;
  display: flex;
  justify-content: space-between;
  margin-bottom: 14px;
  padding: 0 6px;
}

.card-buttons a {
  display: block;
  margin: 4px 0;
  padding: 8px;
  text-decoration: none;
  border-radius: 5px;
  font-size: 13px;
}

.card-buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-btn {
  border: 1px solid #ccc;
  background: white;
  color: #333;
  padding: 8px;
  border-radius: 5px;
  cursor: pointer;
}

.apply-btn {
  background: #22356F;
  color: white;
  padding: 8px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.recommend-condition {
  font-size: 16px;
  text-align: left;
  font-weight: 500;
  margin-bottom: 20px;
}

.recommend-condition strong {
  font-weight: 700;
}

.recommend-container {
  max-width: 900px;
  margin: 0px auto 0; /* 가운데 정렬 */
  padding: 0 50px;      /* ✅ filter-box와 맞추기 */
  box-sizing: border-box;
  padding-top: 30px;
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

.button-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>