<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function exitImpersonation() {
  auth.stopImpersonation()
  router.push({ name: 'AdminDashboard' })
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100 text-gray-600 font-body text-dark-gray">

    <!-- ── Impersonation banner ────────────────────────────────────────── -->
    <div v-if="auth.isImpersonating"
      class="fixed top-0 left-0 right-0 z-[9999] flex items-center justify-between px-4 py-2.5 text-sm font-semibold shadow-lg"
      style="background:#F59E0B;color:#1C1917;">
      <div class="flex items-center gap-2">
        <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
        </svg>
        Viewing as: <span class="font-bold ml-1">{{ auth.user?.firstname }} {{ auth.user?.lastname }}</span>
        <span class="font-normal opacity-70">({{ auth.user?.email }})</span>
      </div>
      <button @click="exitImpersonation"
        class="flex items-center gap-1.5 px-3 py-1 bg-white rounded-full text-amber-800 font-bold hover:bg-amber-100 transition text-xs">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
        </svg>
        Exit
      </button>
    </div>

    <!-- Push content down when banner is visible -->
    <div :class="auth.isImpersonating ? 'pt-10' : ''" class="flex flex-col flex-1">
      <transition name="fade" mode="out-in">
        <router-view :key="$route.fullPath" />
      </transition>
    </div>

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
