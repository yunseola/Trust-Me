<template>
  <div class="mini-chart-box">
    <div class="header">
      <img :src="flagUrl" class="flag" />
      <div class="info">
        <strong>{{ countryName }}</strong>
        <span>{{ currency }}</span>
      </div>
    </div>
    <div class="rate">
      {{ latestRate }}
    </div>
    <canvas ref="canvasEl"></canvas>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
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

const renderChart = () => {
  if (!canvasEl.value || !props.data || props.data.length === 0) return

  latestRate.value = props.data.at(-1)

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  chartInstance.value = new Chart(canvasEl.value, {
    type: 'line',
    data: {
      labels: dateLabels,
      datasets: [
        {
          data: props.data,
          borderColor: '#2196F3',
          backgroundColor: 'rgba(33, 150, 243, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: '날짜',
            font: { size: 12 }
          },
          ticks: {
            font: { size: 10 }
          }
        },
        y: {
          display: true,
          title: {
            display: true,
            text: '환율 (KRW 기준)',
            font: { size: 12 }
          },
          ticks: {
            font: { size: 10 }
          }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  })
}

watch(() => props.data, (val) => {
  if (val && val.length > 0) renderChart()
}, { immediate: true })
</script>

<style scoped>
.mini-chart-box {
  width: 360px;
  height: 240px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.flag {
  width: 24px;
  margin-right: 8px;
}

.rate {
  font-weight: bold;
  font-size: 1.3rem;
  margin-bottom: 6px;
}
</style>
