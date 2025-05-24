<template>
  <div class="flex justify-around bg-yellow-100 rounded p-4">
    <div>
      <h3 class="font-bold">오늘의 금 시세</h3>
      <p>시가: {{ gold.open }}</p>
      <p>고가: {{ gold.high }}</p>
      <p>저가: {{ gold.low }}</p>
    </div>
    <div>
      <h3 class="font-bold">오늘의 은 시세</h3>
      <p>시가: {{ silver.open }}</p>
      <p>고가: {{ silver.high }}</p>
      <p>저가: {{ silver.low }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps(['gold', 'silver'])
</script>
