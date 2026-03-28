<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <router-link :to="{ name: 'AdminAbstracts' }" class="text-gray-400 hover:text-gray-700">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </router-link>
      <h1 class="text-xl font-semibold text-black flex-1 truncate">{{ abstract?.title }}</h1>
      <span v-if="abstract" :class="statusClass(abstract.status)" class="px-3 py-1 rounded-full text-sm font-semibold capitalize flex-shrink-0">
        {{ abstract.status?.replace('_', ' ') }}
      </span>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-10">Loading...</div>
    <template v-else-if="abstract">

      <!-- Meta row -->
      <div class="bg-white rounded-2xl shadow p-6 grid sm:grid-cols-3 gap-4 text-sm">
        <div><span class="text-gray-400">Event</span><p class="font-medium mt-0.5">{{ abstract.event }}</p></div>
        <div><span class="text-gray-400">Track</span><p class="font-medium mt-0.5">{{ abstract.track || '—' }}</p></div>
        <div><span class="text-gray-400">Presentation Type</span><p class="font-medium capitalize mt-0.5">{{ abstract.presentation_type }}</p></div>
        <div><span class="text-gray-400">Words</span><p class="font-medium mt-0.5">{{ abstract.word_count }}</p></div>
        <div><span class="text-gray-400">Submitted by</span><p class="font-medium mt-0.5">{{ abstract.submitter_name }}</p></div>
        <div><span class="text-gray-400">Submitted on</span><p class="font-medium mt-0.5">{{ formatDate(abstract.created_at) }}</p></div>
      </div>

      <!-- Authors -->
      <div class="bg-white rounded-2xl shadow p-6">
        <h2 class="font-semibold text-gray-800 mb-4">Authors & Co-Authors</h2>
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-500 text-xs uppercase">
            <tr>
              <th class="px-3 py-2 text-left">#</th>
              <th class="px-3 py-2 text-left">Name</th>
              <th class="px-3 py-2 text-left hidden md:table-cell">Email</th>
              <th class="px-3 py-2 text-left hidden lg:table-cell">Affiliation</th>
              <th class="px-3 py-2 text-left hidden md:table-cell">Country</th>
              <th class="px-3 py-2 text-left">Presenting</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="(au, i) in abstract.authors" :key="au.id">
              <td class="px-3 py-2 text-gray-400">{{ i + 1 }}</td>
              <td class="px-3 py-2 font-medium">{{ au.firstname }} {{ au.lastname }}</td>
              <td class="px-3 py-2 text-gray-500 hidden md:table-cell">{{ au.email || '—' }}</td>
              <td class="px-3 py-2 text-gray-500 hidden lg:table-cell">{{ au.affiliation || '—' }}</td>
              <td class="px-3 py-2 text-gray-500 hidden md:table-cell">{{ au.country || '—' }}</td>
              <td class="px-3 py-2">
                <span v-if="au.is_presenting" class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-semibold">Yes</span>
                <span v-else class="text-gray-300 text-xs">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Abstract Text -->
      <div class="bg-white rounded-2xl shadow p-6">
        <h2 class="font-semibold text-gray-800 mb-3">Abstract</h2>
        <p class="text-gray-700 leading-relaxed text-sm whitespace-pre-wrap">{{ abstract.abstract_text }}</p>
        <div class="mt-4 flex flex-wrap gap-4 text-xs text-gray-400">
          <span v-if="abstract.keywords"><strong class="text-gray-600">Keywords:</strong> {{ abstract.keywords }}</span>
        </div>
      </div>

      <!-- Update Status -->
      <div class="bg-white rounded-2xl shadow p-6 flex flex-wrap gap-3 items-end">
        <div class="flex-1 min-w-[160px]">
          <label class="block text-sm font-medium text-gray-700 mb-1">Update Status</label>
          <select v-model="newStatus" class="input w-full">
            <option value="submitted">Submitted</option>
            <option value="under_review">Under Review</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
            <option value="revision_required">Revision Required</option>
          </select>
        </div>
        <button @click="updateStatus" class="px-4 py-2 bg-bondi-blue text-white rounded-lg text-sm hover:opacity-90 transition">Update Status</button>
        <span v-if="statusMsg" class="text-green-600 text-sm">{{ statusMsg }}</span>
      </div>

      <!-- Assign Reviewer -->
      <div class="bg-white rounded-2xl shadow p-6">
        <h2 class="font-semibold text-gray-800 mb-4">Reviewers</h2>

        <!-- Current reviewers -->
        <div v-if="abstract.reviewer_assignments.length" class="mb-5 space-y-2">
          <div v-for="ra in abstract.reviewer_assignments" :key="ra.id"
            class="flex items-center justify-between px-4 py-3 bg-gray-50 rounded-xl text-sm">
            <div>
              <p class="font-medium">{{ ra.reviewer_name }}</p>
              <p class="text-gray-400 text-xs">{{ ra.reviewer_email }}</p>
            </div>
            <div class="flex items-center gap-3">
              <span :class="ra.completed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
                class="px-2 py-0.5 rounded-full text-xs font-semibold">
                {{ ra.completed ? 'Reviewed' : 'Pending' }}
              </span>
              <button @click="removeReviewer(ra.reviewer_id)" class="text-red-400 hover:text-red-600 text-xs">Remove</button>
            </div>
          </div>
        </div>

        <!-- Add reviewer form -->
        <div class="flex flex-wrap gap-3 items-end">
          <div class="flex-1 min-w-[200px]">
            <label class="block text-sm font-medium text-gray-700 mb-1">Search & Assign Reviewer</label>
            <input v-model="reviewerSearch" @input="searchUsers" type="text" placeholder="Search by name or email..."
              class="input w-full" />
            <div v-if="userResults.length" class="mt-1 bg-white border border-gray-200 rounded-xl shadow-lg max-h-40 overflow-y-auto z-10">
              <div v-for="u in userResults" :key="u.id"
                @click="selectReviewer(u)"
                class="px-4 py-2 hover:bg-gray-50 cursor-pointer text-sm flex justify-between">
                <span>{{ u.firstname }} {{ u.lastname }}</span>
                <span class="text-gray-400 text-xs">{{ u.email }}</span>
              </div>
            </div>
          </div>
          <div v-if="selectedReviewer" class="text-sm">
            <span class="font-medium text-bondi-blue">{{ selectedReviewer.firstname }} {{ selectedReviewer.lastname }}</span>
          </div>
          <button @click="assignReviewer" :disabled="!selectedReviewer" class="px-4 py-2 bg-bondi-blue text-white rounded-lg text-sm hover:opacity-90 disabled:opacity-40 transition">Assign</button>
          <span v-if="assignMsg" class="text-green-600 text-sm">{{ assignMsg }}</span>
          <span v-if="assignErr" class="text-red-500 text-sm">{{ assignErr }}</span>
        </div>
      </div>

      <!-- Reviews -->
      <div v-if="completedReviews.length" class="bg-white rounded-2xl shadow p-6">
        <h2 class="font-semibold text-gray-800 mb-4">Reviews ({{ completedReviews.length }})</h2>
        <div class="space-y-4">
          <div v-for="ra in completedReviews" :key="ra.id" class="border border-gray-100 rounded-xl p-4">
            <div class="flex items-center justify-between mb-3">
              <p class="font-medium text-sm">{{ ra.reviewer_name }}</p>
              <span :class="recClass(ra.review.recommendation)" class="px-2 py-0.5 rounded-full text-xs font-semibold capitalize">
                {{ ra.review.recommendation?.replace('_', ' ') }}
              </span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-3">
              <div class="bg-gray-50 rounded-lg p-2 text-center">
                <p class="text-xs text-gray-400">Relevance</p>
                <p class="text-lg font-bold text-bondi-blue">{{ ra.review.relevance_score }}<span class="text-xs text-gray-400">/5</span></p>
              </div>
              <div class="bg-gray-50 rounded-lg p-2 text-center">
                <p class="text-xs text-gray-400">Methodology</p>
                <p class="text-lg font-bold text-bondi-blue">{{ ra.review.methodology_score }}<span class="text-xs text-gray-400">/5</span></p>
              </div>
              <div class="bg-gray-50 rounded-lg p-2 text-center">
                <p class="text-xs text-gray-400">Originality</p>
                <p class="text-lg font-bold text-bondi-blue">{{ ra.review.originality_score }}<span class="text-xs text-gray-400">/5</span></p>
              </div>
              <div class="bg-gray-50 rounded-lg p-2 text-center">
                <p class="text-xs text-gray-400">Overall</p>
                <p class="text-lg font-bold text-bondi-blue">{{ ra.review.overall_score }}<span class="text-xs text-gray-400">/5</span></p>
              </div>
            </div>
            <p class="text-sm text-gray-700 leading-relaxed">{{ ra.review.comments }}</p>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route = useRoute()
const abstract = ref(null)
const loading = ref(true)
const newStatus = ref('')
const statusMsg = ref('')
const reviewerSearch = ref('')
const userResults = ref([])
const selectedReviewer = ref(null)
const assignMsg = ref('')
const assignErr = ref('')

onMounted(async () => {
  await fetchAbstract()
  loading.value = false
})

const fetchAbstract = async () => {
  const res = await api.get(`/abstracts/${route.params.id}`)
  abstract.value = res.data
  newStatus.value = res.data.status
}

const completedReviews = computed(() =>
  (abstract.value?.reviewer_assignments || []).filter(ra => ra.review)
)

const updateStatus = async () => {
  await api.put(`/abstracts/${route.params.id}/status`, { status: newStatus.value })
  abstract.value.status = newStatus.value
  statusMsg.value = 'Status updated!'
  setTimeout(() => statusMsg.value = '', 3000)
}

let searchTimeout = null
const searchUsers = () => {
  clearTimeout(searchTimeout)
  selectedReviewer.value = null
  if (!reviewerSearch.value.trim()) { userResults.value = []; return }
  searchTimeout = setTimeout(async () => {
    const res = await api.get(`/users/?search=${encodeURIComponent(reviewerSearch.value)}&limit=10`)
    userResults.value = res.data?.users || res.data || []
  }, 300)
}

const selectReviewer = (u) => {
  selectedReviewer.value = u
  reviewerSearch.value = `${u.firstname} ${u.lastname}`
  userResults.value = []
}

const assignReviewer = async () => {
  assignMsg.value = ''; assignErr.value = ''
  try {
    await api.post(`/abstracts/${route.params.id}/assign-reviewer`, { reviewer_id: selectedReviewer.value.id })
    assignMsg.value = 'Reviewer assigned!'
    selectedReviewer.value = null
    reviewerSearch.value = ''
    await fetchAbstract()
    setTimeout(() => assignMsg.value = '', 3000)
  } catch (e) {
    assignErr.value = e.response?.data?.detail || 'Failed to assign reviewer'
  }
}

const removeReviewer = async (reviewerId) => {
  if (!confirm('Remove this reviewer?')) return
  await api.delete(`/abstracts/${route.params.id}/reviewers/${reviewerId}`)
  await fetchAbstract()
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' }) : '—'
const statusClass = (s) => ({ submitted:'bg-blue-100 text-blue-700', under_review:'bg-yellow-100 text-yellow-700', accepted:'bg-green-100 text-green-700', rejected:'bg-red-100 text-red-700', revision_required:'bg-orange-100 text-orange-700' }[s] || 'bg-gray-100 text-gray-600')
const recClass = (r) => ({ accept:'bg-green-100 text-green-700', reject:'bg-red-100 text-red-700', revision_required:'bg-orange-100 text-orange-700' }[r] || 'bg-gray-100 text-gray-600')
</script>
