<template>
  <div>
    <dt class="text-sm font-bold text-gray-600 uppercase">{{ label }}</dt>
    <dd class="mt-1 text-sm text-gray-900">{{ value }}</dd>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number]
})
</script>
