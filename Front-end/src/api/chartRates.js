// chartRates.js

import axios from 'axios'
import { ref } from 'vue'

export const currencies = [
  { code: 'USD', name: '미국', flag: 'us' },
  { code: 'JPY', name: '일본', flag: 'jp' },
  { code: 'CNY', name: '중국', flag: 'cn' },
  { code: 'EUR', name: '유럽연합', flag: 'eu' },
  { code: 'GBP', name: '영국', flag: 'gb' },
  { code: 'AUD', name: '호주', flag: 'au' }
]

export const rateSeries = ref({})
export const dateLabels = ref([]) // ✅ 추가

export const fetchChartRates = async () => {
  const base = 'KRW'
  const today = new Date()
  const dates = [...Array(7)].map((_, i) => {
    const d = new Date(today)
    d.setDate(d.getDate() - (6 - i))
    return d.toISOString().split('T')[0]
  })

  dateLabels.value = dates // ✅ 레이블도 세팅

  for (const cur of currencies) {
    const results = []
    for (const date of dates) {
      try {
        const { data } = await axios.get(`https://api.frankfurter.app/${date}`, {
          params: { from: base, to: cur.code }
        })
        const rate = data?.rates?.[cur.code]
        results.push(rate ? 1 / rate : 0)
      } catch (err) {
        console.warn(`❌ ${cur.code} ${date} error`, err)
        results.push()
      }
    }
    rateSeries.value[cur.code] = results
  }

  console.log('📊 최종 rateSeries:', rateSeries.value)
}
