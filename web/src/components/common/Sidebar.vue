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
        class="font-title font-black text-xl bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text"
      >
        Event Spaces
      </span>
    </router-link>

    <!-- Navigation Groups -->
    <div class="flex-1 px-2 space-y-6">
      <!-- General Group -->
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

      <!-- Events Group -->
      <div>
        <h3 v-if="!minimized" class="text-xs font-semibold text-gray-400 lowercase tracking-wide mb-2 px-3 select-none">
          events
        </h3>
        <ul>
          <li class="mb-1">
            <router-link
              :to="{ name: 'MyEvents' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <CalendarDaysIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">My Events</span>
            </router-link>
          </li>
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

      <!-- Settings Group -->
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
          <li class="mb-1">
            <router-link
              :to="{ name: 'Settings' }"
              class="flex items-center px-3 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
              active-class="bg-gray-300 text-gray-900 rounded-3xl"
            >
              <Cog6ToothIcon class="w-5 h-5" />
              <span v-if="!minimized" class="ml-3">Settings</span>
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <!-- User Info + Logout -->
    <div class="p-2 mt-auto mb-6 text-sm">
      <div v-if="!minimized" class="mb-3 px-2">
        <router-link to="/profile" class="block font-medium hover:underline text-gray-700">
          {{ username }}
        </router-link>
        <div class="text-xs text-gray-500 mt-0.5">{{ role }}</div>
      </div>
      <button
        @click="logout"
        class="flex items-center justify-between w-full px-2 py-2 text-gray-600 hover:bg-gray-200 hover:text-gray-800 rounded-3xl transition-colors"
      >
        <span v-if="!minimized">Logout</span>
        <ArrowLeftOnRectangleIcon class="w-5 h-5" />
      </button>
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

import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps({
  minimized: {
    type: Boolean,
    default: false,
  },
  username: {
    type: String,
    default: 'Admin',
  },
  role: {
    type: String,
    default: 'Administrator',
  },
})

const router = useRouter()
const auth = useAuthStore()

const logout = () => {
  auth.logout()
  router.push({ name: 'Login' })
}
</script>
