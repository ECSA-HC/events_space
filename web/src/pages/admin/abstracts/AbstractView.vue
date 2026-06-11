<template>
  <!-- height:100vh is self-contained — does NOT depend on parent layout -->
  <div class="flex flex-col w-full max-w-7xl mx-auto px-6 pb-6 pt-6 overflow-hidden" style="height:100vh;">

    <!-- Header — fixed height, never scrolls -->
    <div class="flex items-center gap-4 mb-5 flex-shrink-0">
      <router-link :to="{ name: 'AdminAbstracts' }" class="text-gray-400 hover:text-gray-700 flex-shrink-0">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </router-link>
      <h1 class="text-xl font-semibold text-black flex-1 truncate">{{ abstract?.title }}</h1>
      <span v-if="abstract" :class="statusClass(abstract.status)"
        class="px-3 py-1 rounded-full text-sm font-semibold capitalize flex-shrink-0">
        {{ abstract.status?.replace('_', ' ') }}
      </span>
      <button v-if="abstract" @click="deleteAbstract"
        class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-red-600 border border-red-200 hover:bg-red-50 transition flex-shrink-0">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
        </svg>
        Delete
      </button>
    </div>

    <div v-if="loading" class="text-gray-500 text-center py-20 flex-1">Loading...</div>

    <!-- flex-1 min-h-0 fills remaining height inside the 100vh outer div -->
    <div v-else-if="abstract"
      class="flex-1 min-h-0 grid grid-cols-1 xl:grid-cols-3 gap-6 overflow-hidden">

      <!-- ────────────────────────────────────────────────────────────────────
           LEFT — Management panel (1/3) — scrolls independently
      ─────────────────────────────────────────────────────────────────────── -->
      <div class="xl:col-span-1 overflow-y-auto space-y-5 order-2 xl:order-1 pb-4" style="min-height:0;">

        <!-- Update Status -->
        <div class="bg-white rounded-2xl shadow p-5">
          <h2 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Update Status</h2>
          <select v-model="newStatus" class="input w-full mb-3">
            <option value="submitted">Submitted</option>
            <option value="under_review">Under Review</option>
            <option value="accepted">Accepted</option>
            <option value="rejected">Rejected</option>
            <option value="revision_required">Revision Required</option>
          </select>
          <button @click="updateStatus"
            class="w-full px-4 py-2 text-white rounded-xl text-sm font-semibold hover:opacity-90 transition"
            style="background-color:#0095B6;">
            Save Status
          </button>
          <p v-if="statusMsg" class="mt-2 text-green-600 text-xs text-center">{{ statusMsg }}</p>
        </div>

        <!-- Reviewers panel -->
        <div class="bg-white rounded-2xl shadow p-5">
          <h2 class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 flex items-center gap-2">
            Reviewers
            <span v-if="abstract.reviewer_assignments.length"
              class="text-xs px-2 py-0.5 rounded-full font-semibold"
              style="background-color:#e6f7fb; color:#0095B6;">
              {{ abstract.reviewer_assignments.length }}
            </span>
          </h2>

          <!-- Currently assigned -->
          <div v-if="abstract.reviewer_assignments.length" class="mb-4 space-y-2">
            <div v-for="ra in abstract.reviewer_assignments" :key="ra.id"
              class="flex items-start justify-between px-3 py-2.5 bg-gray-50 rounded-xl text-sm border border-gray-100">
              <div class="min-w-0 flex-1">
                <p class="font-medium text-gray-800 truncate">{{ ra.reviewer_name }}</p>
                <p class="text-gray-400 text-xs truncate">{{ ra.reviewer_email }}</p>
              </div>
              <div class="flex flex-col items-end gap-1.5 ml-2 flex-shrink-0">
                <span :class="ra.completed ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'"
                  class="px-2 py-0.5 rounded-full text-xs font-semibold whitespace-nowrap">
                  {{ ra.completed ? '✓ Reviewed' : '⏳ Pending' }}
                </span>
                <button @click="removeReviewer(ra.reviewer_id)"
                  class="text-red-400 hover:text-red-600 text-xs font-medium">Remove</button>
              </div>
            </div>
          </div>
          <p v-else class="text-xs text-gray-400 italic mb-4">No reviewers assigned yet.</p>

          <!-- ── Reviewer dropdown (loaded from all users, not free-text) ── -->
          <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Add Reviewer
          </label>

          <!-- Custom dropdown trigger -->
          <div class="relative" ref="dropdownWrap">
            <button type="button" @click="toggleDropdown"
              class="w-full flex items-center justify-between px-3 py-2.5 rounded-xl border text-sm text-left transition-colors"
              :class="dropdownOpen
                ? 'border-[#0095B6] ring-2 ring-[#0095B6]/20'
                : 'border-gray-200 hover:border-[#0095B6]/40'">
              <span v-if="selectedReviewer" class="font-medium text-gray-800 truncate">
                {{ selectedReviewer.firstname }} {{ selectedReviewer.lastname }}
              </span>
              <span v-else class="text-gray-400">Select a reviewer…</span>
              <svg class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform ml-2"
                :class="dropdownOpen ? 'rotate-180' : ''"
                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
            </button>

            <!-- Dropdown panel -->
            <div v-if="dropdownOpen"
              class="absolute left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-xl z-30 flex flex-col"
              style="max-height:220px;">
              <!-- Filter input -->
              <div class="flex items-center gap-2 px-3 py-2 border-b border-gray-100 flex-shrink-0">
                <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z"/>
                </svg>
                <input v-model="reviewerFilter" ref="filterInputRef" type="text"
                  placeholder="Filter by name or email…"
                  class="flex-1 text-sm outline-none bg-transparent placeholder-gray-400" />
                <button v-if="reviewerFilter" @click="reviewerFilter = ''"
                  class="text-gray-300 hover:text-gray-500">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                </button>
              </div>
              <!-- List -->
              <div class="overflow-y-auto flex-1">
                <div v-if="usersLoading" class="px-4 py-3 text-xs text-gray-400 text-center">Loading users…</div>
                <div v-else-if="filteredUsers.length === 0"
                  class="px-4 py-3 text-xs text-gray-400 text-center">No users found</div>
                <div v-for="u in filteredUsers" :key="u.id"
                  @click="selectReviewer(u)"
                  class="flex items-center gap-2.5 px-3 py-2.5 cursor-pointer transition-colors text-sm"
                  :class="selectedReviewer?.id === u.id
                    ? 'bg-[#e6f7fb]'
                    : 'hover:bg-gray-50'">
                  <!-- Avatar initials -->
                  <div class="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0"
                    style="background-color:#0095B6;">
                    {{ u.firstname?.[0]?.toUpperCase() }}{{ u.lastname?.[0]?.toUpperCase() }}
                  </div>
                  <div class="min-w-0 flex-1">
                    <p class="font-medium text-gray-800 truncate">{{ u.firstname }} {{ u.lastname }}</p>
                    <p class="text-xs text-gray-400 truncate">{{ u.email }}</p>
                  </div>
                  <svg v-if="selectedReviewer?.id === u.id"
                    class="w-4 h-4 flex-shrink-0" style="color:#0095B6;"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Selected chip -->
          <div v-if="selectedReviewer"
            class="mt-2 flex items-center gap-2 px-3 py-2 rounded-xl border text-sm"
            style="background-color:#e6f7fb; border-color:#b3e4f0;">
            <span class="font-semibold flex-1 truncate" style="color:#006f87;">
              {{ selectedReviewer.firstname }} {{ selectedReviewer.lastname }}
            </span>
            <span class="text-xs truncate" style="color:#0095B6;">{{ selectedReviewer.email }}</span>
            <button @click="selectedReviewer = null"
              class="flex-shrink-0 hover:text-red-400 transition-colors" style="color:#0095B6;">✕</button>
          </div>

          <button @click="assignReviewer" :disabled="!selectedReviewer || assigning"
            class="mt-3 w-full px-4 py-2 rounded-xl text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-40 flex items-center justify-center gap-2"
            style="background-color:#0095B6;">
            <svg v-if="assigning" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
            </svg>
            {{ assigning ? 'Assigning…' : 'Assign Reviewer' }}
          </button>
          <p v-if="assignMsg" class="mt-2 text-green-600 text-xs text-center">{{ assignMsg }}</p>
          <p v-if="assignErr" class="mt-2 text-red-500 text-xs text-center">{{ assignErr }}</p>
        </div>

      </div>

      <!-- ────────────────────────────────────────────────────────────────────
           RIGHT — Abstract content (2/3) — scrolls independently
      ─────────────────────────────────────────────────────────────────────── -->
      <div class="xl:col-span-2 overflow-y-auto space-y-5 order-1 xl:order-2 pr-1 pb-4" style="min-height:0;">

        <!-- Meta row -->
        <div class="bg-white rounded-2xl shadow p-6 grid sm:grid-cols-3 gap-4 text-sm">
          <div>
            <span class="text-gray-400 text-xs uppercase tracking-wide">Event</span>
            <p class="font-medium mt-1">{{ abstract.event }}</p>
          </div>
          <div class="sm:col-span-3">
            <span class="text-gray-400 text-xs uppercase tracking-wide">Track</span>
            <div class="mt-1">
              <span v-if="abstract.track_code"
                class="inline-flex items-center gap-1.5 text-xs font-bold px-2 py-0.5 rounded-full border mr-2"
                style="background-color:#e6f7fb; color:#006f87; border-color:#b3e4f0;">
                {{ abstract.track_code }}
              </span>
              <span class="font-medium text-sm">{{ abstract.track_title || abstract.track || '—' }}</span>
              <p v-if="abstract.track_theme" class="text-xs text-gray-400 mt-0.5 italic">{{ abstract.track_theme }}</p>
            </div>
          </div>
          <div>
            <span class="text-gray-400 text-xs uppercase tracking-wide">Presentation Type</span>
            <p class="font-medium capitalize mt-1">{{ abstract.presentation_type }}</p>
          </div>
          <div>
            <span class="text-gray-400 text-xs uppercase tracking-wide">Words</span>
            <p class="font-medium mt-1">{{ abstract.word_count }}</p>
          </div>
          <div>
            <span class="text-gray-400 text-xs uppercase tracking-wide">Submitted by</span>
            <p class="font-medium mt-1">{{ abstract.submitter_name }}</p>
          </div>
          <div>
            <span class="text-gray-400 text-xs uppercase tracking-wide">Submitted on</span>
            <p class="font-medium mt-1">{{ formatDate(abstract.created_at) }}</p>
          </div>
        </div>

        <!-- Authors -->
        <div class="bg-white rounded-2xl shadow p-6">
          <h2 class="font-semibold text-gray-800 mb-4">Authors & Co-Authors</h2>
          <div class="overflow-x-auto">
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
                    <span v-if="au.is_presenting"
                      class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-xs font-semibold">Yes</span>
                    <span v-else class="text-gray-300 text-xs">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Abstract Text -->
        <div class="bg-white rounded-2xl shadow p-6">
          <h2 class="font-semibold text-gray-800 mb-3">Abstract</h2>
          <p class="text-gray-700 leading-relaxed text-sm whitespace-pre-wrap">{{ abstract.abstract_text }}</p>
          <div v-if="abstract.keywords" class="mt-4 text-xs text-gray-500">
            <strong class="text-gray-700">Keywords:</strong> {{ abstract.keywords }}
          </div>
        </div>

        <!-- Completed reviews -->
        <div v-if="completedReviews.length" class="bg-white rounded-2xl shadow p-6">
          <h2 class="font-semibold text-gray-800 mb-4 flex items-center gap-2">
            Reviews
            <span class="text-xs px-2 py-0.5 rounded-full font-medium"
              style="background-color:#e6f7fb; color:#0095B6;">
              {{ completedReviews.length }}
            </span>
          </h2>
          <div class="space-y-4">
            <div v-for="ra in completedReviews" :key="ra.id" class="border border-gray-100 rounded-xl p-4">
              <div class="flex items-center justify-between mb-3">
                <p class="font-medium text-sm">{{ ra.reviewer_name }}</p>
                <span :class="recClass(ra.review.recommendation)"
                  class="px-2 py-0.5 rounded-full text-xs font-semibold capitalize">
                  {{ ra.review.recommendation?.replace('_', ' ') }}
                </span>
              </div>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-3">
                <div class="bg-gray-50 rounded-lg p-2 text-center">
                  <p class="text-xs text-gray-400">Relevance</p>
                  <p class="text-lg font-bold" style="color:#0095B6;">{{ ra.review.relevance_score }}<span class="text-xs text-gray-400">/5</span></p>
                </div>
                <div class="bg-gray-50 rounded-lg p-2 text-center">
                  <p class="text-xs text-gray-400">Methodology</p>
                  <p class="text-lg font-bold" style="color:#0095B6;">{{ ra.review.methodology_score }}<span class="text-xs text-gray-400">/5</span></p>
                </div>
                <div class="bg-gray-50 rounded-lg p-2 text-center">
                  <p class="text-xs text-gray-400">Originality</p>
                  <p class="text-lg font-bold" style="color:#0095B6;">{{ ra.review.originality_score }}<span class="text-xs text-gray-400">/5</span></p>
                </div>
                <div class="bg-gray-50 rounded-lg p-2 text-center">
                  <p class="text-xs text-gray-400">Overall</p>
                  <p class="text-lg font-bold" style="color:#0095B6;">{{ ra.review.overall_score }}<span class="text-xs text-gray-400">/5</span></p>
                </div>
              </div>
              <p class="text-sm text-gray-700 leading-relaxed">{{ ra.review.comments }}</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios'

const route  = useRoute()
const router = useRouter()

const abstract         = ref(null)
const loading          = ref(true)
const newStatus        = ref('')
const statusMsg        = ref('')

// Reviewer selection
const allUsers         = ref([])
const usersLoading     = ref(false)
const selectedReviewer = ref(null)
const reviewerFilter   = ref('')
const dropdownOpen     = ref(false)
const dropdownWrap     = ref(null)
const filterInputRef   = ref(null)
const assigning        = ref(false)
const assignMsg        = ref('')
const assignErr        = ref('')

// ── Load users once on mount ─────────────────────────────────────────────────
onMounted(async () => {
  await fetchAbstract()
  loading.value = false
  loadAllUsers()
})

const loadAllUsers = async () => {
  usersLoading.value = true
  try {
    const res = await api.get('/abstracts/reviewers/candidates')
    allUsers.value = res.data || []
  } catch (_) {}
  finally { usersLoading.value = false }
}

// ── Abstract data ─────────────────────────────────────────────────────────────
const fetchAbstract = async () => {
  const res = await api.get(`/abstracts/${route.params.id}`)
  abstract.value = res.data
  newStatus.value = res.data.status
}

const completedReviews = computed(() =>
  (abstract.value?.reviewer_assignments || []).filter(ra => ra.review)
)

// ── Filtered dropdown list (excludes already assigned) ───────────────────────
const alreadyAssignedIds = computed(() =>
  new Set((abstract.value?.reviewer_assignments || []).map(ra => ra.reviewer_id))
)

const filteredUsers = computed(() => {
  const q = reviewerFilter.value.toLowerCase().trim()
  return allUsers.value
    .filter(u => !alreadyAssignedIds.value.has(u.id))
    .filter(u => !q || `${u.firstname} ${u.lastname} ${u.email}`.toLowerCase().includes(q))
})

// ── Dropdown open/close ───────────────────────────────────────────────────────
const toggleDropdown = async () => {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) {
    reviewerFilter.value = ''
    await nextTick()
    filterInputRef.value?.focus()
  }
}

const closeDropdown = (e) => {
  if (dropdownWrap.value && !dropdownWrap.value.contains(e.target)) {
    dropdownOpen.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', closeDropdown))
onBeforeUnmount(() => document.removeEventListener('mousedown', closeDropdown))

const selectReviewer = (u) => {
  selectedReviewer.value = u
  dropdownOpen.value = false
  reviewerFilter.value = ''
}

// ── Status update ─────────────────────────────────────────────────────────────
const updateStatus = async () => {
  await api.put(`/abstracts/${route.params.id}/status`, { status: newStatus.value })
  abstract.value.status = newStatus.value
  statusMsg.value = 'Status updated!'
  setTimeout(() => statusMsg.value = '', 3000)
}

// ── Assign / remove reviewer ─────────────────────────────────────────────────
const assignReviewer = async () => {
  if (!selectedReviewer.value) return
  assigning.value = true
  assignMsg.value = ''
  assignErr.value = ''
  try {
    await api.post(`/abstracts/${route.params.id}/assign-reviewer`, {
      reviewer_id: selectedReviewer.value.id,
    })
    assignMsg.value = `${selectedReviewer.value.firstname} ${selectedReviewer.value.lastname} assigned!`
    selectedReviewer.value = null
    await fetchAbstract()
    setTimeout(() => assignMsg.value = '', 3000)
  } catch (e) {
    assignErr.value = e.response?.data?.detail || 'Failed to assign reviewer'
  } finally {
    assigning.value = false
  }
}

const removeReviewer = async (reviewerId) => {
  if (!confirm('Remove this reviewer?')) return
  await api.delete(`/abstracts/${route.params.id}/reviewers/${reviewerId}`)
  await fetchAbstract()
}

const deleteAbstract = async () => {
  if (!confirm(`Delete "${abstract.value.title}"? This cannot be undone.`)) return
  try {
    await api.delete(`/abstracts/${route.params.id}`)
    router.push({ name: 'AdminAbstracts' })
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete abstract')
  }
}

const formatDate  = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' }) : '—'
const statusClass = (s) => ({ submitted:'bg-blue-100 text-blue-700', under_review:'bg-yellow-100 text-yellow-700', accepted:'bg-green-100 text-green-700', rejected:'bg-red-100 text-red-700', revision_required:'bg-orange-100 text-orange-700' }[s] || 'bg-gray-100 text-gray-600')
const recClass    = (r) => ({ accept:'bg-green-100 text-green-700', reject:'bg-red-100 text-red-700', revision_required:'bg-orange-100 text-orange-700' }[r] || 'bg-gray-100 text-gray-600')
</script>
