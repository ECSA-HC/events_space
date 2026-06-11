<template>
  <div class="flex-1 flex flex-col w-full max-w-7xl mx-auto p-6 space-y-6 overflow-x-hidden">

    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-black">Email Logs</h1>
        <p v-if="!loading" class="text-sm text-gray-400 mt-0.5">
          {{ total }} email{{ total !== 1 ? 's' : '' }} sent
        </p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow p-4 flex flex-wrap gap-3">
      <input v-model="search" type="text" placeholder="Search recipient or subject..."
        class="input flex-1 min-w-[200px]" />
      <select v-model="filterType" class="input w-52">
        <option value="">All Types</option>
        <option value="reviewer_assignment">Reviewer Assignment</option>
        <option value="new_account">New Account</option>
        <option value="general">General</option>
      </select>
      <select v-model="filterStatus" class="input w-40">
        <option value="">All Statuses</option>
        <option value="sent">Sent</option>
        <option value="failed">Failed</option>
      </select>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow overflow-hidden">
      <div v-if="loading" class="p-10 text-center text-gray-400">Loading…</div>
      <div v-else-if="filtered.length === 0" class="p-10 text-center text-gray-400">No emails found.</div>
      <table v-else class="w-full text-sm text-gray-700">
        <thead class="bg-gray-50 text-xs uppercase text-gray-500 border-b">
          <tr>
            <th class="px-5 py-3 text-left">Sent At</th>
            <th class="px-5 py-3 text-left">Recipient</th>
            <th class="px-5 py-3 text-left">Subject</th>
            <th class="px-5 py-3 text-left">Type</th>
            <th class="px-5 py-3 text-left">Sent By</th>
            <th class="px-5 py-3 text-left">Reply-To</th>
            <th class="px-5 py-3 text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in paginated" :key="log.id"
              class="border-b last:border-0 hover:bg-gray-50 transition-colors"
              :class="log.status === 'failed' ? 'bg-red-50' : ''">
            <td class="px-5 py-3 whitespace-nowrap text-gray-500 text-xs">
              {{ fmtDate(log.sent_at) }}
            </td>
            <td class="px-5 py-3 font-medium">{{ log.recipient_email }}</td>
            <td class="px-5 py-3 max-w-xs truncate" :title="log.subject">{{ log.subject }}</td>
            <td class="px-5 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                :class="typeClass(log.email_type)">
                {{ typeLabel(log.email_type) }}
              </span>
            </td>
            <td class="px-5 py-3">
              <span v-if="log.sent_by" class="text-gray-700">{{ log.sent_by }}</span>
              <span v-else class="text-gray-400 italic">System</span>
            </td>
            <td class="px-5 py-3 text-gray-500 text-xs">{{ log.reply_to_email || '—' }}</td>
            <td class="px-5 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                :class="log.status === 'sent' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
                {{ log.status }}
              </span>
              <p v-if="log.error_message" class="text-xs text-red-500 mt-0.5 max-w-xs truncate" :title="log.error_message">
                {{ log.error_message }}
              </p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && filtered.length > 0"
         class="flex items-center justify-between text-sm text-gray-600 flex-wrap gap-3">
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <div class="flex gap-2">
        <button :disabled="currentPage === 1" @click="currentPage--"
          class="px-3 py-1 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-40">
          Previous
        </button>
        <button :disabled="currentPage === totalPages" @click="currentPage++"
          class="px-3 py-1 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-40">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'

const logs        = ref([])
const total       = ref(0)
const loading     = ref(true)
const search      = ref('')
const filterType  = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const perPage     = 50

onMounted(fetchLogs)

async function fetchLogs() {
  loading.value = true
  try {
    const res = await api.get('/email-logs/?skip=0&limit=500')
    logs.value  = res.data?.data  || []
    total.value = res.data?.total || 0
  } catch (e) {
    console.error('Failed to load email logs', e)
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  const q = search.value.toLowerCase().trim()
  return logs.value.filter(l => {
    if (filterType.value   && l.email_type !== filterType.value)   return false
    if (filterStatus.value && l.status     !== filterStatus.value) return false
    if (q && !`${l.recipient_email} ${l.subject} ${l.sent_by ?? ''}`.toLowerCase().includes(q)) return false
    return true
  })
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / perPage)))
const paginated  = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filtered.value.slice(start, start + perPage)
})

function fmtDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function typeLabel(t) {
  const map = {
    reviewer_assignment: 'Reviewer Assignment',
    new_account: 'New Account',
    general: 'General',
  }
  return map[t] || t
}

function typeClass(t) {
  const map = {
    reviewer_assignment: 'bg-blue-100 text-blue-700',
    new_account:         'bg-purple-100 text-purple-700',
    general:             'bg-gray-100 text-gray-600',
  }
  return map[t] || 'bg-gray-100 text-gray-600'
}
</script>
