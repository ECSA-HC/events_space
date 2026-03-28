<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-black">Abstract Submissions</h1>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow p-4 flex flex-wrap gap-3">
      <input v-model="search" type="text" placeholder="Search by title..."
        class="input flex-1 min-w-[180px]" />
      <select v-model="filterEvent" class="input w-44">
        <option value="">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
      <select v-model="filterStatus" class="input w-40">
        <option value="">All Statuses</option>
        <option value="submitted">Submitted</option>
        <option value="under_review">Under Review</option>
        <option value="accepted">Accepted</option>
        <option value="rejected">Rejected</option>
        <option value="revision_required">Revision Required</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow overflow-hidden">
      <div v-if="loading" class="p-8 text-center text-gray-500">Loading abstracts...</div>
      <div v-else-if="filtered.length === 0" class="p-8 text-center text-gray-400">No abstracts found.</div>
      <table v-else class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-600 text-xs uppercase">
          <tr>
            <th class="px-4 py-3 text-left">Title</th>
            <th class="px-4 py-3 text-left hidden md:table-cell">Event</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell">Track</th>
            <th class="px-4 py-3 text-left hidden md:table-cell">First Author</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell">Type</th>
            <th class="px-4 py-3 text-left">Status</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell">Submitted</th>
            <th class="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="abs in paginated" :key="abs.id" class="hover:bg-gray-50 transition">
            <td class="px-4 py-3 font-medium text-gray-800 max-w-[200px] truncate">{{ abs.title }}</td>
            <td class="px-4 py-3 text-gray-600 hidden md:table-cell">{{ abs.event }}</td>
            <td class="px-4 py-3 text-gray-500 hidden lg:table-cell">{{ abs.track || '—' }}</td>
            <td class="px-4 py-3 text-gray-600 hidden md:table-cell">
              {{ abs.authors[0] ? `${abs.authors[0].firstname} ${abs.authors[0].lastname}` : '—' }}
            </td>
            <td class="px-4 py-3 text-gray-500 capitalize hidden lg:table-cell">{{ abs.presentation_type }}</td>
            <td class="px-4 py-3">
              <span :class="statusClass(abs.status)" class="px-2 py-1 rounded-full text-xs font-semibold capitalize">
                {{ abs.status?.replace('_', ' ') }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-400 text-xs hidden lg:table-cell">{{ formatDate(abs.created_at) }}</td>
            <td class="px-4 py-3 text-right">
              <router-link :to="{ name: 'AdminAbstract', params: { id: abs.id } }"
                class="text-bondi-blue hover:underline text-xs font-medium">View</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Pagination -->
      <div v-if="filtered.length > pageSize" class="flex items-center justify-between px-4 py-3 border-t text-sm text-gray-500">
        <span>{{ filtered.length }} total</span>
        <div class="flex gap-2">
          <button @click="page--" :disabled="page===1" class="px-3 py-1 rounded border disabled:opacity-40">Prev</button>
          <span class="px-2 py-1">{{ page }} / {{ totalPages }}</span>
          <button @click="page++" :disabled="page===totalPages" class="px-3 py-1 rounded border disabled:opacity-40">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'

const abstracts = ref([])
const events = ref([])
const loading = ref(true)
const search = ref('')
const filterEvent = ref('')
const filterStatus = ref('')
const page = ref(1)
const pageSize = 15

onMounted(async () => {
  const [absRes, evRes] = await Promise.all([
    api.get('/abstracts/'),
    api.get('/events/?skip=0&limit=200'),
  ])
  abstracts.value = absRes.data
  events.value = evRes.data
  loading.value = false
})

const filtered = computed(() => {
  let list = abstracts.value
  if (search.value) list = list.filter(a => a.title.toLowerCase().includes(search.value.toLowerCase()))
  if (filterEvent.value) list = list.filter(a => a.event_id === filterEvent.value)
  if (filterStatus.value) list = list.filter(a => a.status === filterStatus.value)
  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)))
const paginated = computed(() => filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize))

const statusClass = (s) => ({
  submitted: 'bg-blue-100 text-blue-700',
  under_review: 'bg-yellow-100 text-yellow-700',
  accepted: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
  revision_required: 'bg-orange-100 text-orange-700',
}[s] || 'bg-gray-100 text-gray-600')

const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' }) : '—'
</script>
