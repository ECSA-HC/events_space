<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <AdminBar title="Abstract Reviewers">
      <a href="#" class="text-sm text-blue-600 hover:underline">Reviewers</a>
    </AdminBar>

    <div class="px-6 pt-4 pb-2 flex items-center justify-between">
      <h1 class="text-xl font-bold text-gray-800">Abstract Reviewers</h1>
    </div>

    <!-- Filters -->
    <div class="px-6 pb-4 flex flex-col sm:flex-row gap-3">
      <input
        v-model="search"
        type="text"
        placeholder="Search by name or email..."
        class="w-full sm:w-72 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
      />
      <select
        v-model="selectedEventId"
        class="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
        @change="fetchReviewers"
      >
        <option :value="null">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
    </div>

    <main class="px-6 pb-6 space-y-4">
      <div v-if="isLoading" class="flex justify-center py-10">
        <DataLoadingSpinner />
      </div>

      <div v-else-if="filteredReviewers.length === 0" class="bg-white rounded-xl shadow p-10 text-center text-gray-400">
        No reviewers found.
      </div>

      <div
        v-for="reviewer in filteredReviewers"
        :key="reviewer.reviewer_id"
        class="bg-white rounded-xl shadow overflow-hidden"
      >
        <!-- Reviewer header -->
        <div
          class="flex items-center justify-between px-6 py-4 cursor-pointer hover:bg-gray-50 transition"
          @click="toggle(reviewer.reviewer_id)"
        >
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-full bg-[#0095B6] flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
              {{ initials(reviewer.name) }}
            </div>
            <div>
              <p class="font-semibold text-gray-800">{{ reviewer.name }}</p>
              <p class="text-xs text-gray-400">{{ reviewer.email }}</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right hidden sm:block">
              <p class="text-sm font-medium text-gray-700">{{ reviewer.total }} abstract{{ reviewer.total !== 1 ? 's' : '' }}</p>
              <p class="text-xs text-gray-400">{{ reviewer.completed }} reviewed</p>
            </div>
            <div class="flex gap-2">
              <span class="px-2 py-0.5 text-xs rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                {{ reviewer.total - reviewer.completed }} pending
              </span>
              <span class="px-2 py-0.5 text-xs rounded-full bg-green-50 text-green-700 border border-green-200">
                {{ reviewer.completed }} done
              </span>
            </div>
            <ChevronDownIcon
              class="w-5 h-5 text-gray-400 transition-transform"
              :class="expanded.has(reviewer.reviewer_id) ? 'rotate-180' : ''"
            />
          </div>
        </div>

        <!-- Assignments list -->
        <div v-if="expanded.has(reviewer.reviewer_id)" class="border-t divide-y">
          <div
            v-for="a in reviewer.assignments"
            :key="a.assignment_id"
            class="flex items-center justify-between px-6 py-3 hover:bg-gray-50"
          >
            <div class="flex-1 min-w-0 mr-4">
              <p class="text-sm font-medium text-gray-700 truncate">{{ a.abstract_title }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ a.event || '—' }} · Assigned {{ formatDate(a.assigned_at) }}</p>
            </div>
            <div class="flex items-center gap-3 flex-shrink-0">
              <span
                :class="a.completed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
                class="px-2 py-0.5 rounded-full text-xs font-semibold"
              >
                {{ a.completed ? 'Reviewed' : 'Pending' }}
              </span>
              <router-link
                :to="{ name: 'AdminAbstract', params: { id: a.abstract_id } }"
                class="text-xs text-blue-600 hover:underline"
              >View</router-link>
              <button
                @click="removeAssignment(reviewer.reviewer_id, a.abstract_id, a.assignment_id)"
                class="text-xs text-red-400 hover:text-red-600"
              >Remove</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ChevronDownIcon } from '@heroicons/vue/24/outline'
import AdminBar from '@/components/common/AdminBar.vue'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'
import api from '@/plugins/axios'

const reviewers = ref([])
const events = ref([])
const selectedEventId = ref(null)
const search = ref('')
const isLoading = ref(false)
const expanded = ref(new Set())

const filteredReviewers = computed(() => {
  const q = search.value.toLowerCase()
  if (!q) return reviewers.value
  return reviewers.value.filter(
    (r) => r.name.toLowerCase().includes(q) || r.email.toLowerCase().includes(q)
  )
})

const toggle = (id) => {
  const s = new Set(expanded.value)
  s.has(id) ? s.delete(id) : s.add(id)
  expanded.value = s
}

const initials = (name) =>
  name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()

const fetchEvents = async () => {
  try {
    const res = await api.get('/events/?limit=200')
    events.value = res.data?.data || []
  } catch (e) {
    console.error('Failed to load events', e)
  }
}

const fetchReviewers = async () => {
  isLoading.value = true
  try {
    const params = {}
    if (selectedEventId.value) params.event_id = selectedEventId.value
    const res = await api.get('/abstracts/reviewers', { params })
    reviewers.value = res.data
  } catch (e) {
    console.error('Failed to load reviewers', e)
  } finally {
    isLoading.value = false
  }
}

const removeAssignment = async (reviewerId, abstractId, assignmentId) => {
  if (!confirm('Remove this reviewer from the abstract?')) return
  try {
    await api.delete(`/abstracts/${abstractId}/reviewers/${reviewerId}`)
    await fetchReviewers()
  } catch (e) {
    console.error('Failed to remove assignment', e)
  }
}

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '—'

onMounted(() => {
  fetchEvents()
  fetchReviewers()
})
</script>
