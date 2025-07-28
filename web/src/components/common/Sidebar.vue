<template>
  <nav
    :class="[minimized ? 'w-16' : 'w-52', 'bg-catskill-white text-gray-600 flex flex-col min-h-screen transition-all duration-300 overflow-hidden']"
  >
    <!-- Logo Section -->
    <router-link :to="{ name: 'AdminDashboard' }" class="flex flex-col items-center justify-center py-4">
      <img v-if="!minimized" src="@/assets/ecsalogo.png" alt="Logo" class="h-16 mb-1" />
      <img v-else src="@/assets/ecsalogo.png" alt="Logo Icon" class="h-10" />
      <span
        v-if="!minimized"
        class="font-title font-black text-xl text-bondi-blue bg-clip-text"
      >
        Event Spaces
      </span>
    </router-link>

    <!-- Navigation Groups -->
    <div class="flex-1 px-2 space-y-6">
      <!-- General -->
      <div>
        <h3 v-if="!minimized" class="text-xs font-semibold text-gray-400 lowercase tracking-wide mb-2 px-3 select-none">
          general
        </h3>
        <ul>
          <li class="mb-1">
            <router-link
              :to="{ name: 'AdminDashboard' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <HomeIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">Home</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Events -->
      <div>
        <h3 v-if="!minimized" class="text-xs font-semibold text-gray-400 lowercase tracking-wide mb-2 px-3 select-none">
          events
        </h3>
        <ul>
          <li class="mb-1">
            <router-link
              :to="{ name: 'AdminEvents' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <ClipboardDocumentListIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">All Events</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Settings -->
      <div>
        <h3 v-if="!minimized" class="text-xs font-semibold text-gray-400 lowercase tracking-wide mb-2 px-3 select-none">
          settings
        </h3>
        <ul>
          <li class="mb-1">
            <router-link
              :to="{ name: 'Users' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <UsersIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">User Management</span>
            </router-link>
          </li>
          <li class="mb-1">
            <router-link
              :to="{ name: 'Roles' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <ShieldCheckIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">Access Roles</span>
            </router-link>
          </li>
          <li class="mb-1">
            <router-link
              :to="{ name: 'Clusters' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <BuildingOffice2Icon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">Clusters</span>
            </router-link>
          </li>
          <!-- <li class="mb-1">
            <router-link
              :to="{ name: 'Settings' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <Cog6ToothIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">Settings</span>
            </router-link>
          </li> -->
        </ul>

        <!-- My Account -->
        <ul>
          <li class="mb-1">
            <router-link
              :to="{ name: 'MyDashboard' }"
              class="flex items-center px-3 py-2 rounded-3xl transition-colors
                     bg-yellow-100 border-2 border-yellow-400 text-yellow-700 font-semibold
                     hover:bg-yellow-200 hover:border-yellow-500 shadow-md"
              active-class="bg-yellow-300 text-yellow-900 font-bold shadow-lg"
            >
              <CalendarDaysIcon class="w-5 h-5 text-yellow-600" />
              <span v-if="!minimized" class="ml-3">My Account</span>
            </router-link>
          </li>
        </ul>

        <!-- User Info + Logout directly below My Account -->
        <div
          class="mt-3 mx-2 p-3 rounded-3xl bg-blue-100 border-2 border-blue-400 text-blue-700 font-semibold shadow-md"
          :class="minimized ? 'text-center' : ''"
        >
          <div v-if="!minimized && username" class="mb-2 px-2">
            <router-link
              to="/profile"
              class="block font-medium hover:underline text-blue-800"
            >
              {{ username }}
            </router-link>
          </div>
          <button
            @click="logout"
            class="flex items-center justify-center w-full px-3 py-2 bg-blue-200 hover:bg-blue-300 rounded-3xl transition-colors text-blue-900 font-semibold shadow"
          >
            <span v-if="!minimized" class="mr-2 hidden sm:inline">Logout</span>
            <ArrowLeftOnRectangleIcon class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import {
  HomeIcon,
  CalendarDaysIcon,
  ClipboardDocumentListIcon,
  UsersIcon,
  ShieldCheckIcon,
  BuildingOffice2Icon,
  Cog6ToothIcon,
  ArrowLeftOnRectangleIcon,
} from '@heroicons/vue/24/outline'

import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps({
  minimized: {
    type: Boolean,
    default: false,
  },
})

const auth = useAuthStore()
const router = useRouter()

const username = computed(() => auth.user?.firstname || 'User')

const logout = () => {
  auth.logout()
  router.push({ name: 'Login' })
}
</script>
