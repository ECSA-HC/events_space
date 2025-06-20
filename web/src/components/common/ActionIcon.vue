<!-- ClusterActionIcon.vue -->
<template>
    <div v-if="can" class="relative group cursor-pointer" @click="$emit('click')">
      <component :is="icon" class="w-5 h-5" :class="colorClass" />
      <Tooltip>{{ label }}</Tooltip>
    </div>
  </template>
  
  <script setup>
  import Tooltip from '@/components/common/Tooltip.vue'
  defineProps({
    can: Boolean,
    icon: Object,
    label: String,
    colorClass: String,
  });
  </script>
  