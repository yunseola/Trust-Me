<template>
  <div class="chart-wrapper">
    <Line v-if="chartData.labels.length > 0" :data="chartData" :options="chartOptions" />
    <div v-else class="no-data">📭 선택한 날짜에 해당하는 시세 데이터가 없습니다.</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  LineElement, CategoryScale, LinearScale, PointElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps(['data'])

const prices = computed(() =>
  props.data.map(d => parseFloat(d.Price)).filter(v => !isNaN(v))
)

const yMin = computed(() => {
  if (prices.value.length === 0) return 0
  const min = Math.min(...prices.value)
  return Math.floor(min - 1)
})

const yMax = computed(() => {
  if (prices.value.length === 0) return 10
  const max = Math.max(...prices.value)
  return Math.ceil(max + 1)
})

const chartData = computed(() => ({
  labels: props.data.map(d => d.Date),
  datasets: [{
    label: '시세',
    data: prices.value,
    borderColor: '#22356F',
    backgroundColor: 'rgba(34, 53, 111, 0.1)',
    tension: 0.3,
    pointRadius: 3,
    fill: false
  }]
}))

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: {
      display: true,
      labels: {
        color: '#333',
        font: { size: 14 }
      }
    }
  },
  scales: {
    x: {
      ticks: { color: '#666' }
    },
    y: {
      min: yMin.value,
      max: yMax.value,
      ticks: {
        color: '#666',
        stepSize: 0.5
      }
    }
  }
}))
</script>

