<script setup>
import { ref, onMounted } from 'vue'
import AdminBar from '@/components/common/AdminBar.vue'
import {
  UserIcon,
  CalendarDaysIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import api from '@/plugins/axios'

const totalUsers = ref(0)
const upcomingEventsCount = ref(0)
const completedEventsCount = ref(0)
const recentEvents = ref([])

const loading = ref(false)
const error = ref(null)

async function loadDashboard() {
  loading.value = true
  error.value = null

  try {
    const res = await api.get('/dashboard')
    totalUsers.value = res.data.total_users
    upcomingEventsCount.value = res.data.upcoming_events_count
    completedEventsCount.value = res.data.completed_events_count
    recentEvents.value = res.data.recent_events
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <AdminBar title="Dashboard">
      <a href="#" class="text-sm text-blue-600 hover:underline">Dashboard</a>
    </AdminBar>

    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Admin Overview</h1>
    </div>

    <main class="p-6 space-y-6">
      <div v-if="loading" class="text-center text-gray-500">Loading dashboard...</div>
      <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
      <div v-else>
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-white rounded-2xl shadow p-5 flex items-center gap-5">
            <div class="bg-blue-100 text-blue-600 rounded-full p-3">
              <UserIcon class="h-7 w-7" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Total Users</h3>
              <p class="text-2xl font-extrabold">{{ totalUsers }}</p>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow p-5 flex items-center gap-5">
            <div class="bg-green-100 text-green-600 rounded-full p-3">
              <CalendarDaysIcon class="h-7 w-7" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Upcoming Events</h3>
              <p class="text-2xl font-extrabold">{{ upcomingEventsCount }}</p>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow p-5 flex items-center gap-5">
            <div class="bg-yellow-100 text-yellow-600 rounded-full p-3">
              <CheckCircleIcon class="h-7 w-7" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Completed Events</h3>
              <p class="text-2xl font-extrabold">{{ completedEventsCount }}</p>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow p-5 flex items-center gap-5">
            <div class="bg-indigo-100 text-indigo-600 rounded-full p-3">
              <ClockIcon class="h-7 w-7" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">System Uptime</h3>
              <p class="text-2xl font-extrabold">99.9%</p>
            </div>
          </div>
        </div>

<!-- Recent Events Table -->
<div class="bg-white shadow rounded-xl overflow-hidden mt-8">
  <h2 class="text-xl font-semibold px-6 pt-6">Recent Events</h2>
  <div class="w-full overflow-x-auto">
    <table class="w-full table-auto text-sm text-gray-800">
      <thead class="bg-gray-100 text-left uppercase text-xs text-gray-800 hidden md:table-header-group">
        <tr>
          <th class="px-6 py-4">Event</th>
          <th class="px-6 py-4">Start Date</th>
          <th class="px-6 py-4">End Date</th>
          <th class="px-6 py-4">Participants</th>
          <th class="px-6 py-4">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="recentEvents.length === 0">
          <td colspan="5" class="text-center px-6 py-6 text-gray-400 italic">No recent events found.</td>
        </tr>
        <tr
          v-for="event in recentEvents"
          :key="event.id"
          class="block md:table-row border-t md:border-0 md:hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
        >
          <td class="px-6 py-4 block md:table-cell">
            <div class="font-medium">{{ event.name }}</div>
          </td>
          <td class="px-6 py-4 block md:table-cell">
            {{ new Date(event.start_date).toLocaleDateString() }}
          </td>
          <td class="px-6 py-4 block md:table-cell">
            {{ new Date(event.end_date).toLocaleDateString() }}
          </td>
          <td class="px-6 py-4 block md:table-cell">
            {{ event.participants }}
          </td>
          <td class="px-6 py-4 block md:table-cell">
            <span
              :class="[
                'px-3 py-1 rounded-full text-xs font-semibold',
                event.status === 'upcoming'
                  ? 'bg-blue-100 text-blue-600'
                  : 'bg-green-100 text-green-600'
              ]"
            >
              {{ event.status }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

      </div>
    </main>
  </div>
</template>
