<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminBar from '@/components/common/AdminBar.vue'
import { useAuthStore } from '@/stores/auth'
import {
  UserIcon,
  CalendarDaysIcon,
  CheckCircleIcon,
  DocumentTextIcon,
  ClipboardDocumentCheckIcon,
} from '@heroicons/vue/24/outline'
import api from '@/plugins/axios'

const auth = useAuthStore()
const isFullAdmin = computed(() => auth.hasPermission('VIEW_USER'))

const totalUsers = ref(0)
const upcomingEventsCount = ref(0)
const completedEventsCount = ref(0)
const totalAbstracts = ref(0)
const totalRegistrations = ref(0)
const recentEvents = ref([])
const eventStats = ref([])

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
    totalAbstracts.value = res.data.total_abstracts
    totalRegistrations.value = res.data.total_registrations
    recentEvents.value = res.data.recent_events
    eventStats.value = res.data.event_stats
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

onMounted(loadDashboard)
</script>

<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <AdminBar title="Dashboard">
      <a href="#" class="text-sm text-blue-600 hover:underline">Dashboard</a>
    </AdminBar>

    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">
        {{ isFullAdmin ? 'Admin Overview' : 'Statistics Overview' }}
      </h1>
    </div>

    <main class="p-6 space-y-6">
      <div v-if="loading" class="text-center text-gray-500 py-10">Loading…</div>
      <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
      <div v-else class="space-y-6">

        <!-- Full admin top cards -->
        <div v-if="isFullAdmin" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
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
              <DocumentTextIcon class="h-7 w-7" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Total Abstracts</h3>
              <p class="text-2xl font-extrabold">{{ totalAbstracts }}</p>
            </div>
          </div>
        </div>

        <!-- Stats-only summary cards (always shown) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="bg-white rounded-2xl shadow p-6 flex items-center gap-5">
            <div class="bg-[#0095B6]/10 text-[#0095B6] rounded-full p-4">
              <DocumentTextIcon class="h-8 w-8" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Total Abstracts Submitted</h3>
              <p class="text-3xl font-extrabold text-gray-800">{{ totalAbstracts }}</p>
            </div>
          </div>
          <div class="bg-white rounded-2xl shadow p-6 flex items-center gap-5">
            <div class="bg-green-100 text-green-600 rounded-full p-4">
              <ClipboardDocumentCheckIcon class="h-8 w-8" />
            </div>
            <div>
              <h3 class="text-sm text-gray-500">Total Registrations</h3>
              <p class="text-3xl font-extrabold text-gray-800">{{ totalRegistrations }}</p>
            </div>
          </div>
        </div>

        <!-- Per-event stats table (always shown) -->
        <div class="bg-white shadow rounded-xl overflow-hidden">
          <h2 class="text-base font-semibold px-6 pt-5 pb-3 text-gray-800">
            Registrations &amp; Abstracts by Event
          </h2>
          <div class="overflow-x-auto">
            <table class="w-full table-auto text-sm text-gray-800">
              <thead class="bg-gray-100 text-left uppercase text-xs text-gray-600">
                <tr>
                  <th class="px-6 py-3">Event</th>
                  <th class="px-6 py-3 text-center">Status</th>
                  <th class="px-6 py-3 text-center">Registrations</th>
                  <th class="px-6 py-3 text-center">Abstracts</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="eventStats.length === 0">
                  <td colspan="4" class="text-center px-6 py-8 text-gray-400 italic">No events found.</td>
                </tr>
                <tr
                  v-for="ev in eventStats"
                  :key="ev.id"
                  class="border-t hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
                >
                  <td class="px-6 py-4 font-medium">{{ ev.name }}</td>
                  <td class="px-6 py-4 text-center">
                    <span
                      :class="ev.status === 'upcoming' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'"
                      class="px-3 py-1 rounded-full text-xs font-semibold capitalize"
                    >{{ ev.status }}</span>
                  </td>
                  <td class="px-6 py-4 text-center font-semibold text-gray-700">{{ ev.registrations }}</td>
                  <td class="px-6 py-4 text-center font-semibold text-gray-700">{{ ev.abstracts }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Full admin recent events (only for full admins) -->
        <div v-if="isFullAdmin" class="bg-white shadow rounded-xl overflow-hidden">
          <h2 class="text-base font-semibold px-6 pt-5 pb-3 text-gray-800">Recent Events Detail</h2>
          <div class="overflow-x-auto">
            <table class="w-full table-auto text-sm text-gray-800">
              <thead class="bg-gray-100 text-left uppercase text-xs text-gray-600">
                <tr>
                  <th class="px-6 py-3">Event</th>
                  <th class="px-6 py-3">Start Date</th>
                  <th class="px-6 py-3">End Date</th>
                  <th class="px-6 py-3 text-center">Participants</th>
                  <th class="px-6 py-3 text-center">Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="recentEvents.length === 0">
                  <td colspan="5" class="text-center px-6 py-6 text-gray-400 italic">No recent events.</td>
                </tr>
                <tr
                  v-for="event in recentEvents"
                  :key="event.id"
                  class="border-t hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
                >
                  <td class="px-6 py-4 font-medium">{{ event.name }}</td>
                  <td class="px-6 py-4">{{ new Date(event.start_date).toLocaleDateString() }}</td>
                  <td class="px-6 py-4">{{ new Date(event.end_date).toLocaleDateString() }}</td>
                  <td class="px-6 py-4 text-center">{{ event.participants }}</td>
                  <td class="px-6 py-4 text-center">
                    <span
                      :class="event.status === 'upcoming' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'"
                      class="px-3 py-1 rounded-full text-xs font-semibold capitalize"
                    >{{ event.status }}</span>
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
