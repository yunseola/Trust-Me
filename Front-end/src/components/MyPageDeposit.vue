<template>
  <div class="finance-compare-container">
    <div class="card-area">
      <div
        v-for="product in products"
        :key="product.fin_prdt_cd"
        :class="['product-card']"
        @click="toggleSelect(product)"
      >
        <div class="logo-area">
          <img :src="getBankLogo(product.kor_co_nm)" :alt="product.kor_co_nm" class="bank-logo" width="80px" height="80px" />
          <span class="bank-name">{{ product.kor_co_nm }}</span>
        </div>
        <div class="product-name">{{ product.fin_prdt_nm }}</div>
        <div class="product-info">
          <span class="rate">연 {{ product.max_intr }}%</span>
          <span class="period">{{ product.type === 'deposit' ? '예금' : '적금' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getBankLogo } from '@/api/logos.js'

const STORAGE_KEY = 'savedFinanceProducts'
const products = ref([])
const selected = ref([])

function loadProducts() {
  const data = localStorage.getItem(STORAGE_KEY)
  products.value = data ? JSON.parse(data) : []
}

function isSelected(product) {
  return selected.value.some(
    p => p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type
  )
}

function toggleSelect(product) {
  const idx = selected.value.findIndex(
    p => p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type
  )
  if (idx >= 0) {
    selected.value.splice(idx, 1)
  } else if (selected.value.length < 2) {
    selected.value.push(product)
  }
}

onMounted(() => {
  loadProducts()
  window.addEventListener('storage', (e) => {
    if (e.key === STORAGE_KEY) loadProducts()
  })
})
</script>

<style scoped>
.finance-compare-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 10px;
  font-family: 'Noto Sans KR', sans-serif;
  color: #333;
}

.card-area {
  display: flex;
  gap: 28px;
  justify-content: center;
  background: #E8E8E4;
  padding: 36px 0 24px 0;
  border-radius: 12px;
  max-width: 1200px;
  margin: 0 auto;
}

.product-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px #e5eaf0cc;
  border: 2px solid transparent;
  transition: border 0.2s, box-shadow 0.2s, transform 0.2s;
  cursor: pointer;
  width: 220px;
  padding: 24px 16px 18px 16px;
  text-align: center;
  position: relative;
}

.logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}

.bank-logo {
  width: 80px;
  height: 80px;
  margin-bottom: 4px;
}

.bank-name {
  font-weight: 700;
  color: #c59a1a;
  font-size: 1.03em;
  margin-bottom: 2px;
}

.product-name {
  font-weight: bold;
  font-size: 1.08em;
  margin-bottom: 12px;
  color: #222;
}

.product-info {
  display: flex;
  justify-content: space-between;
  font-size: 1em;
  color: #333;
}

.rate {
  font-weight: 600;
}

.period {
  color: #888;
}

@media (max-width: 700px) {
  .card-area {
    flex-direction: column;
    align-items: center;
    max-width: 100vw;
    padding: 18px 0 12px 0;
    gap: 16px;
  }
  .product-card {
    width: 98vw;
    min-width: 0;
  }
}
</style>
