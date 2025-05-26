<template>
  <div>
    <h2>금융상품 비교</h2>
    <div v-if="products.length === 0">
      <p>비교할 금융상품을 먼저 담아주세요.</p>
    </div>
    <table v-else border="1" cellpadding="8" style="border-collapse:collapse; width:100%;">
      <thead>
        <tr>
          <th>구분</th>
          <th>상품명</th>
          <th>금융회사</th>
          <th>최고금리(%)</th>
          <th>가입대상</th>
          <th>가입방법</th>
          <th>만기 후 이자율</th>
          <th>우대조건</th>
          <th>기타 안내</th>
          <th>삭제</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.type + product.fin_prdt_cd">
          <td>
            <span v-if="product.type === 'deposit'" style="color:#1976d2;">예금</span>
            <span v-else style="color:#43a047;">적금</span>
          </td>
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.max_intr }}</td>
          <td>{{ product.join_member }}</td>
          <td>{{ product.join_way }}</td>
          <td>{{ product.mtrt_int }}</td>
          <td>{{ product.spcl_cnd }}</td>
          <td>{{ product.etc_note }}</td>
          <td>
            <button @click="removeProduct(product)" style="color:red;">삭제</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="products.length > 0" style="margin-top:20px;">
      <button @click="clearAll" style="color:red;">전체비우기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'savedFinanceProducts'
const products = ref([])

function loadProducts() {
  const data = localStorage.getItem(STORAGE_KEY)
  products.value = data ? JSON.parse(data) : []
}

function removeProduct(product) {
  products.value = products.value.filter(
    p => !(p.fin_prdt_cd === product.fin_prdt_cd && p.type === product.type)
  )
  localStorage.setItem(STORAGE_KEY, JSON.stringify(products.value))
}

function clearAll() {
  products.value = []
  localStorage.removeItem(STORAGE_KEY)
}

onMounted(() => {
  loadProducts()
})
</script>
