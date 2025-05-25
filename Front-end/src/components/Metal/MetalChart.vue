<template>
  <div class="chart-wrapper">
    <Line :data="chartData" :options="chartOptions" />
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

const chartData = {
  labels: props.data.map(d => d.Date),
  datasets: [{
    label: '시세',
    data: props.data.map(d => d.Price),
    borderColor: '#22356F',
    backgroundColor: 'rgba(34, 53, 111, 0.1)',
    tension: 0.3,
    pointRadius: 3,
    fill: false
  }]
}


const chartOptions = {
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
    x: { ticks: { color: '#666' } },
    y: { ticks: { color: '#666' } }
  }
}
</script>

<style scoped>
.chart-wrapper {
  max-width: 1000px;
  margin: 0 auto;
}
</style>
