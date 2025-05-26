<script setup>
import { ref, computed } from 'vue'
import MiniChartBox from './MiniChartBox.vue'
import { currencies, rateSeries } from '@/api/chartRates'

const currentPage = ref(0)
const itemsPerPage = 2

const totalPages = computed(() => Math.ceil(currencies.length / itemsPerPage))

const visibleCharts = computed(() => {
  const start = currentPage.value * itemsPerPage
  return currencies.slice(start, start + itemsPerPage)
})

// ✅ 무한 슬라이딩 로직
const nextPage = () => {
  currentPage.value = (currentPage.value + 1) % totalPages.value
}

const prevPage = () => {
  currentPage.value = (currentPage.value - 1 + totalPages.value) % totalPages.value
}
</script>

<template>
  <div class="slider-wrapper">
    <!-- 🔁 버튼에서 disabled 제거 -->
    <button @click="prevPage" class="arrow">◀</button>

    <div class="chart-container">
      <MiniChartBox
        v-for="cur in visibleCharts"
        :key="cur.code"
        :currency="cur.code"
        :countryName="cur.name"
        :flagUrl="`https://flagcdn.com/w40/${cur.flag}.png`"
        :data="rateSeries[cur.code]"
      />
    </div>

    <button @click="nextPage" class="arrow">▶</button>
  </div>
</template>

<style scoped>
.slider-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.chart-container {
  display: flex;
  gap: 40px;
  flex-direction: row;
}

.arrow {
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.arrow:hover {
  background: #f0f0f0;
}
</style>
