<template>
  <div class="flex gap-4">
    <input type="date" :value="startDate" @input="$emit('update:startDate', $event.target.value)" />
    <input type="date" :value="endDate" @input="$emit('update:endDate', $event.target.value)" />
  </div>
</template>

<script setup>
defineProps(['startDate', 'endDate'])
defineEmits(['update:startDate', 'update:endDate'])
</script>
