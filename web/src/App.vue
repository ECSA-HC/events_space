<script setup>
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100 text-gray-600 font-body text-dark-gray">
    <transition name="fade" mode="out-in">
      <!-- Use :key to trigger transition on route change -->
      <router-view :key="$route.fullPath" />
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.1s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
</style>
