<template>
  <div class="mini-chart-box">
    <div class="header">
      <div class="left">
        <img :src="flagUrl" class="flag" />
        <strong>{{ countryName }} {{ currency }}</strong>
      </div>
      <div class="right">
        <span class="inline-rate">
          {{ formattedLatestRate }}
        </span>
      </div>
    </div>
    <div class="chart-wrapper">
      <canvas ref="canvasEl" width="480" height="200"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import {
  Chart, LineController, LineElement, LinearScale,
  PointElement, CategoryScale, Filler
} from 'chart.js'
import { dateLabels } from '@/api/chartRates'

Chart.register(LineController, LineElement, LinearScale, PointElement, CategoryScale, Filler)

const props = defineProps({
  currency: String,
  countryName: String,
  flagUrl: String,
  data: Array
})

const canvasEl = ref(null)
const chartInstance = ref(null)
const latestRate = ref(0)
const formattedLatestRate = ref('')

const formatNumber = (num) => {
  return Number(num).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const renderChart = () => {
  if (!canvasEl.value || !props.data || props.data.length === 0) return

  const latest = props.data.at(-1) || 0
  const previous = props.data.at(-2) || latest
  const isUp = latest > previous

  latestRate.value = latest
  formattedLatestRate.value = formatNumber(latest)

  const lineColor = isUp ? '#E53935' : '#2196F3'
  const fillColor = isUp ? 'rgba(229, 57, 53, 0.1)' : 'rgba(33, 150, 243, 0.1)'

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  chartInstance.value = new Chart(canvasEl.value, {
    type: 'line',
    data: {
      labels: dateLabels.value,
      datasets: [
        {
          data: props.data,
          borderColor: lineColor,
          backgroundColor: fillColor,
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      animation: false,
      maintainAspectRatio: true,
      scales: {
        x: {
          display: true,
          title: { display: true, text: '날짜', font: { size: 12 } },
          ticks: { font: { size: 10 } }
        },
        y: {
          display: true,
          title: { display: true, text: '환율 (KRW 기준)', font: { size: 12 } },
          ticks: { font: { size: 10 } }
        }
      },
      plugins: { legend: { display: false } }
    }
  })
}

watch(
  () => props.data,
  (val) => {
    if (val && val.length > 0) renderChart()
  },
  { immediate: true, deep: true } // ✅ 핵심 포인트!
)

onMounted(async () => {
  await nextTick()
  if (props.data && props.data.length > 0) {
    renderChart()
  }
})

</script>

<style scoped>
.mini-chart-box {
  width: 520px;
  height: 280px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.flag {
  width: 24px;
}

.inline-rate {
  font-weight: bold;
  font-size: 1rem;
  color: #111;
}

.chart-wrapper {
  margin-top: 8px;
}

.inline-rate {
  font-weight: bold;
  font-size: 1.5rem; /* 기존 1rem → 더 큼 */
  color: #111;
}

</style>
