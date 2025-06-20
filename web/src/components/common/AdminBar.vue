<template>
  <header class="bg-white p-4 flex items-center text-gray-700">
    <div class="flex items-center space-x-2 text-base">
      <HomeIcon class="h-5 w-5 text-gray-500" />
      <span>Home</span>
      <ChevronRightIcon class="h-4 w-4 text-gray-400" />
      <span class="font-bold">{{ title }}</span>
    </div>
  </header>
</template>

<script setup>
import { HomeIcon, ChevronRightIcon } from '@heroicons/vue/24/outline'

defineProps({
  title: {
    type: String,
    required: true,
  },
})
</script>
