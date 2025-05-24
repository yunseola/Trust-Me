import axios from 'axios'

export const getSummary = async () => {
  const res = await axios.get('/api/summary')  // 백엔드 연동 필요
  return res.data
}

export const getPriceData = async (metal, start, end) => {
  const res = await axios.get(`/api/prices?metal=${metal}&start=${start}&end=${end}`)
  return res.data
}
