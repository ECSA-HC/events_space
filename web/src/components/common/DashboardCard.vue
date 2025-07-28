<script setup>
import {
  UserIcon,
  CalendarDaysIcon,
  CurrencyDollarIcon,
  ClockIcon,
} from '@heroicons/vue/24/outline'

const props = defineProps({
  icon: String,
  title: String,
  value: String,
  color: String,
})

const icons = {
  UserIcon,
  CalendarDaysIcon,
  CurrencyDollarIcon,
  ClockIcon,
}
</script>

<template>
  <div class="bg-white rounded-2xl shadow p-4 flex items-center gap-4">
    <div :class="`bg-${color}-100 text-${color}-600`" class="rounded-full p-3">
      <component :is="icons[icon]" class="h-6 w-6" />
    </div>
    <div>
      <h3 class="text-sm text-gray-500">{{ title }}</h3>
      <p class="text-xl font-bold">{{ value }}</p>
    </div>
  </div>
</template>
