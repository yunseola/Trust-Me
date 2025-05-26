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

  <div v-if="recommendationResult.length" class="recommendation-box">
  <h3>추천 상품</h3>
  <ul>
    <li v-for="(item, index) in recommendationResult" :key="index">
      {{ item }}
    </li>
  </ul>
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
import { useRouter } from 'vue-router'; // ✅ 꼭 필요함

const router = useRouter();
const recommendationResult = ref([]);
const isLoading = ref(false);

const ageOptions = ['10대', '20대', '30대', '40대', '50대', '60대 이상'];
const assetLabels = ['0', '~300만', '~500만', '~1000만', '~3000만', '~5000만', '~1억', '1억 이상'];
const goalOptions = ['목돈 마련', '생활비', '단기 수익', '결혼', '주택', '노후 준비', '기타'];
const productOptions = ['예금', '적금'];

const selectedAge = ref('');
const selectedAsset = ref(0);
const selectedGoal = ref('');
const selectedProduct = ref('');

const resetFilter = () => {
  selectedAge.value = '';
  selectedAsset.value = 0;
  selectedGoal.value = '';
  selectedProduct.value = '';
};

const searchProducts = async () => {
  isLoading.value = true;
  recommendationResult.value = [];

  const requestData = {
    age: selectedAge.value,
    asset: assetLabels[selectedAsset.value],
    goal: selectedGoal.value,
    type: selectedProduct.value
  };

  try {
    const response = await axios.post('http://localhost:8000/api/gpt-recommendation/', requestData);
    const rawText = response.data.recommendation;

    const splitResult = rawText
      .split(/\d+\.\s*상품명:/)
      .filter(item => item.trim() !== '')
      .map(item => "상품명:" + item.trim());

    recommendationResult.value = splitResult;
  } catch (error) {
    console.error('추천 요청 실패:', error);
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
  z-index: 0;
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


