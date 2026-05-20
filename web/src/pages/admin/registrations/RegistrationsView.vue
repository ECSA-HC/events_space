<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <AdminBar title="Registrations">
      <a href="#" class="text-sm text-blue-600 hover:underline">Registrations</a>
    </AdminBar>

    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Event Registrations</h1>
    </div>

    <!-- Filters -->
    <div class="px-6 pb-4 flex flex-col md:flex-row md:items-center gap-3 flex-wrap">
      <input
        v-model="search"
        type="text"
        placeholder="Search by name, email or phone..."
        class="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
      />
      <select
        v-model="selectedEventId"
        class="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
      >
        <option :value="null">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
      <select
        v-model="paidFilter"
        class="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
      >
        <option value="all">All Payment Status</option>
        <option value="true">Paid</option>
        <option value="false">Unpaid</option>
      </select>
      <button
        v-if="canExport"
        @click="exportRegistrations"
        :disabled="exporting"
        class="ml-auto flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white px-5 py-2 rounded-xl transition text-sm"
      >
        <ArrowDownTrayIcon class="w-4 h-4" />
        {{ exporting ? 'Exporting…' : 'Export Excel' }}
      </button>
    </div>

    <main class="px-6 pb-6">
      <div class="w-full overflow-hidden bg-white shadow rounded-lg">
        <table class="w-full table-auto text-sm text-gray-800 rounded-lg overflow-hidden">
          <thead class="bg-gray-100 text-left uppercase text-xs text-gray-800 hidden md:table-header-group">
            <tr>
              <th class="px-4 py-3">#</th>
              <th class="px-4 py-3">Name</th>
              <th class="px-4 py-3">Email</th>
              <th class="px-4 py-3">Event</th>
              <th class="px-4 py-3">Role</th>
              <th class="px-4 py-3">Payment</th>
              <th class="px-4 py-3">Registered</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td colspan="7" class="py-8 text-center">
                <DataLoadingSpinner />
              </td>
            </tr>
            <tr
              v-for="(reg, index) in registrations"
              :key="reg.id"
              class="border-t hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
              v-else
            >
              <td class="px-4 py-3 text-gray-400 text-xs font-mono">
                {{ (currentPage - 1) * perPage + index + 1 }}
              </td>
              <td class="px-4 py-3 font-medium">
                {{ reg.title ? reg.title + ' ' : '' }}{{ reg.firstname }} {{ reg.lastname }}
                <div class="text-xs text-gray-400">{{ reg.phone }}</div>
              </td>
              <td class="px-4 py-3 text-gray-600">{{ reg.email }}</td>
              <td class="px-4 py-3 text-gray-600">{{ reg.event || '—' }}</td>
              <td class="px-4 py-3">
                <span class="inline-block px-2 py-0.5 text-xs bg-blue-50 text-blue-700 rounded-full border border-blue-200 capitalize">
                  {{ reg.participation_role?.replace('_', ' ') || '—' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span
                  :class="reg.paid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
                  class="inline-block px-2 py-0.5 text-xs rounded-full font-semibold"
                >
                  {{ reg.paid ? 'Paid' : 'Unpaid' }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-500 text-xs">{{ formatDate(reg.registered_at) }}</td>
            </tr>
            <tr v-if="!isLoading && registrations.length === 0">
              <td colspan="7" class="text-center px-6 py-8 text-gray-400">No registrations found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex flex-col md:flex-row md:items-center justify-between mt-4 gap-4 text-sm text-gray-600">
        <div class="flex items-center space-x-2">
          <label class="text-sm">Show</label>
          <select
            v-model="perPage"
            class="border border-gray-300 rounded-md px-2 py-1 focus:outline-none focus:ring-1 focus:ring-[#0095B6]"
          >
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
          </select>
          <span class="text-gray-400">of {{ total }} total</span>
        </div>
        <div class="text-center">Page {{ currentPage }} of {{ totalPages }}</div>
        <div class="flex justify-end items-center space-x-2">
          <button
            :disabled="currentPage === 1"
            @click="currentPage--"
            class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
          >Previous</button>
          <button
            :disabled="currentPage === totalPages"
            @click="currentPage++"
            class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
          >Next</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ArrowDownTrayIcon } from '@heroicons/vue/24/outline'
import AdminBar from '@/components/common/AdminBar.vue'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'
import api from '@/plugins/axios'
import { debounce } from 'lodash'

const auth = useAuthStore()
const search = ref('')
const debouncedSearch = ref('')
const selectedEventId = ref(null)
const paidFilter = ref('all')
const currentPage = ref(1)
const perPage = ref(10)
const totalPages = ref(1)
const total = ref(0)
const registrations = ref([])
const events = ref([])
const isLoading = ref(false)
const exporting = ref(false)

const canExport = computed(() => auth.hasPermission('EXPORT_REGISTRATIONS'))

const updateDebouncedSearch = debounce((val) => {
  debouncedSearch.value = val
  currentPage.value = 1
}, 300)

watch(search, updateDebouncedSearch)
watch([perPage, selectedEventId, paidFilter], () => (currentPage.value = 1))

const fetchEvents = async () => {
  try {
    const res = await api.get('/events/?limit=200')
    events.value = res.data?.data || []
  } catch (e) {
    console.error('Failed to load events', e)
  }
}

const fetchRegistrations = async () => {
  isLoading.value = true
  try {
    const skip = (currentPage.value - 1) * perPage.value
    const params = {
      skip,
      limit: perPage.value,
      search: debouncedSearch.value,
      paid: paidFilter.value,
    }
    if (selectedEventId.value) params.event_id = selectedEventId.value
    const res = await api.get('/registrations/', { params })
    registrations.value = res.data.data
    totalPages.value = res.data.pages || 1
    total.value = res.data.total || 0
  } catch (e) {
    console.error('Failed to load registrations', e)
  } finally {
    isLoading.value = false
  }
}

const exportRegistrations = async () => {
  exporting.value = true
  try {
    const params = { paid: paidFilter.value, search: debouncedSearch.value }
    if (selectedEventId.value) params.event_id = selectedEventId.value
    const res = await api.get('/registrations/export', {
      params,
      responseType: 'blob',
    })
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = 'registrations_export.xlsx'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Export failed', e)
  } finally {
    exporting.value = false
  }
}

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'

watch([currentPage, perPage, debouncedSearch, selectedEventId, paidFilter], fetchRegistrations)
onMounted(() => {
  fetchEvents()
  fetchRegistrations()
})
</script>
