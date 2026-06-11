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
        <option value="pending">Pending</option>
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
            <th class="px-5 py-3 text-left">Status</th>
            <th class="px-5 py-3 text-left">Opened</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in paginated" :key="log.id"
              class="border-b last:border-0 hover:bg-blue-50 cursor-pointer transition-colors"
              :class="log.status === 'failed' ? 'bg-red-50 hover:bg-red-100' : ''"
              @click="openDetail(log)">
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
            <td class="px-5 py-3">
              <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                :class="statusClass(log.status)">
                {{ log.status }}
              </span>
              <p v-if="log.error_message" class="text-xs text-red-500 mt-0.5 max-w-xs truncate" :title="log.error_message">
                {{ log.error_message }}
              </p>
            </td>
            <td class="px-5 py-3">
              <span v-if="log.opened_count > 0" class="inline-flex items-center gap-1 text-xs font-semibold text-green-700">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                {{ log.opened_count }}×
              </span>
              <span v-else class="text-xs text-gray-400">—</span>
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

    <!-- Detail modal -->
    <Teleport to="body">
      <div v-if="selectedLog" class="fixed inset-0 z-50 flex items-center justify-center p-4"
           @click.self="closeDetail">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="closeDetail" />

        <!-- Panel -->
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">

          <!-- Modal header -->
          <div class="flex items-start justify-between p-5 border-b shrink-0">
            <div class="min-w-0 flex-1 pr-4">
              <h2 class="text-lg font-semibold text-gray-900 truncate">{{ selectedLog.subject }}</h2>
              <p class="text-sm text-gray-500 mt-0.5">To: {{ selectedLog.recipient_email }}</p>
            </div>
            <button @click="closeDetail"
              class="shrink-0 p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 transition-colors">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Meta strip -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 px-5 py-3 bg-gray-50 border-b text-xs shrink-0">
            <div>
              <p class="text-gray-400 uppercase font-semibold tracking-wide mb-0.5">Sent at</p>
              <p class="text-gray-700">{{ fmtDate(selectedLog.sent_at) }}</p>
            </div>
            <div>
              <p class="text-gray-400 uppercase font-semibold tracking-wide mb-0.5">Sent by</p>
              <p class="text-gray-700">{{ selectedLog.sent_by || 'System' }}</p>
            </div>
            <div>
              <p class="text-gray-400 uppercase font-semibold tracking-wide mb-0.5">Status</p>
              <span class="px-2 py-0.5 rounded-full font-semibold"
                :class="statusClass(selectedLog.status)">{{ selectedLog.status }}</span>
            </div>
            <div>
              <p class="text-gray-400 uppercase font-semibold tracking-wide mb-0.5">Opened</p>
              <div v-if="detailLoading" class="text-gray-400">…</div>
              <div v-else-if="detailLog && detailLog.opened_count > 0">
                <p class="text-green-700 font-semibold">
                  {{ detailLog.opened_count }}× opened
                </p>
                <p class="text-gray-500">First: {{ fmtDate(detailLog.opened_at) }}</p>
              </div>
              <p v-else class="text-gray-400 italic">Not opened yet</p>
            </div>
          </div>

          <!-- Email body -->
          <div class="flex-1 overflow-auto p-5">
            <div v-if="detailLoading" class="text-center text-gray-400 py-10">Loading email content…</div>
            <div v-else-if="detailLog && detailLog.body">
              <iframe
                ref="previewFrame"
                class="w-full border border-gray-200 rounded-xl bg-white"
                style="min-height: 480px;"
                sandbox="allow-same-origin"
                :srcdoc="detailLog.body"
                @load="resizeFrame"
              />
            </div>
            <div v-else-if="detailLog && !detailLog.body"
                 class="text-center text-gray-400 py-10 italic">
              Email content not available for this log entry.
            </div>
            <div v-else-if="detailError" class="text-center text-red-500 py-10">
              Failed to load email content.
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import api from '@/plugins/axios'

const logs        = ref([])
const total       = ref(0)
const loading     = ref(true)
const search      = ref('')
const filterType  = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const perPage     = 50

// detail modal
const selectedLog  = ref(null)
const detailLog    = ref(null)
const detailLoading = ref(false)
const detailError  = ref(false)
const previewFrame = ref(null)

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

async function openDetail(log) {
  selectedLog.value  = log
  detailLog.value    = null
  detailError.value  = false
  detailLoading.value = true
  try {
    const res = await api.get(`/email-logs/${log.id}`)
    detailLog.value = res.data
  } catch (e) {
    detailError.value = true
  } finally {
    detailLoading.value = false
    await nextTick()
    resizeFrame()
  }
}

function closeDetail() {
  selectedLog.value = null
  detailLog.value   = null
}

function resizeFrame() {
  const frame = previewFrame.value
  if (!frame) return
  try {
    const h = frame.contentDocument?.body?.scrollHeight
    if (h) frame.style.height = `${h + 24}px`
  } catch (_) {}
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

function statusClass(s) {
  const map = {
    sent:    'bg-green-100 text-green-700',
    failed:  'bg-red-100 text-red-700',
    pending: 'bg-yellow-100 text-yellow-700',
  }
  return map[s] || 'bg-gray-100 text-gray-600'
}
</script>
