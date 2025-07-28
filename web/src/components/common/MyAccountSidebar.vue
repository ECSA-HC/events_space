<!-- src/components/common/MyAccountSidebar.vue -->
<template>
  <aside class="p-4 md:p-6 w-full md:w-64 bg-white rounded-2xl shadow-md flex flex-col">
    <!-- Title -->
    <h2 class="text-2xl font-semibold text-black mb-8 flex items-center gap-2">
      <UserIcon class="w-6 h-6 text-bondi-blue" />
      My Account
    </h2>

    <!-- Nav Links -->
    <nav class="flex-1 space-y-2 text-sm font-medium">
      <router-link
        :to="{ name: 'MyDashboard' }"
        class="flex items-center gap-3 px-4 py-2 rounded-lg transition hover:bg-gray-100"
        active-class="bg-gray-100 text-bondi-blue font-semibold"
      >
        <LayoutDashboardIcon class="w-5 h-5" />
        Dashboard
      </router-link>

      <router-link
        :to="{ name: 'MyEvents' }"
        class="flex items-center gap-3 px-4 py-2 rounded-lg transition hover:bg-gray-100"
        active-class="bg-gray-100 text-bondi-blue font-semibold"
      >
        <CalendarIcon class="w-5 h-5" />
        Events
      </router-link>

      <router-link
        :to="{ name: 'MyProfile' }"
        class="flex items-center gap-3 px-4 py-2 rounded-lg transition hover:bg-gray-100"
        active-class="bg-gray-100 text-bondi-blue font-semibold"
      >
        <UserCircleIcon class="w-5 h-5" />
        My Profile
      </router-link>

      <router-link
        :to="{ name: 'AdminDashboard' }"
        v-if="canViewAdminDashboard"
        class="flex items-center gap-3 px-4 py-2 rounded-lg transition 
               bg-yellow-100 border-2 border-yellow-400 text-yellow-700 font-semibold
               hover:bg-yellow-200 hover:border-yellow-500 shadow-md"
        active-class="bg-yellow-300 text-yellow-900 font-bold shadow-lg"
      >
        <ShieldIcon class="w-5 h-5 text-yellow-600" />
        Events Admin
      </router-link>
    </nav>

    <!-- Logout -->
    <div class="mt-8 pt-4 border-t text-sm">
<button @click="logout" class="flex items-center gap-2 text-red-600 hover:underline">
  <LogOutIcon class="w-5 h-5" />
  <span class="hidden sm:inline">Logout</span>
</button>
    </div>
  </aside>
</template>

<script setup>
import {
  UserIcon,
  LayoutDashboardIcon,
  CalendarIcon,
  UserCircleIcon,
  LogOutIcon,
  ShieldIcon,
} from 'lucide-vue-next'
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from 'vue-router'

const auth = useAuthStore();
const router = useRouter()

function logout() {
  auth.logout()
  router.push({ name: 'Login' })
}

const canViewAdminDashboard = computed(() => auth.hasPermission("ADMIN_DASHBOARD"));
</script>
