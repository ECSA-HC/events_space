<template>
  <div class="flex-1 flex flex-col w-full max-w-5xl mx-auto p-6 space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-black">Abstract Tracks</h1>
        <p v-if="!loading" class="text-sm text-gray-400 mt-0.5">
          {{ tracks.length }} tracks across {{ events.length }} event{{ events.length !== 1 ? 's' : '' }}
        </p>
      </div>
      <!-- Event filter -->
      <select v-model="filterEvent" class="input w-52">
        <option value="">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="bg-white rounded-2xl shadow p-10 text-center text-gray-400">
      Loading tracks…
    </div>

    <!-- Grouped by theme -->
    <div v-else-if="groupedTracks.length === 0" class="bg-white rounded-2xl shadow p-10 text-center text-gray-400">
      No tracks found.
    </div>

    <div v-else class="space-y-6">
      <div v-for="group in groupedTracks" :key="group.theme" class="bg-white rounded-2xl shadow overflow-hidden">

        <!-- Theme header -->
        <div class="px-5 py-3 border-b flex items-center gap-3" style="background-color:#e6f7fb;">
          <div class="w-2 h-2 rounded-full flex-shrink-0" style="background-color:#0095B6;"></div>
          <p class="font-semibold text-sm" style="color:#006f87;">{{ group.theme }}</p>
          <span class="ml-auto text-xs font-medium px-2 py-0.5 rounded-full border"
            style="background-color:#fff; color:#0095B6; border-color:#b3e4f0;">
            {{ group.tracks.length }} track{{ group.tracks.length !== 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Tracks list -->
        <div class="divide-y divide-gray-50">
          <div v-for="track in group.tracks" :key="track.id" class="px-5 py-4">

            <!-- View mode -->
            <div v-if="editingId !== track.id" class="flex items-start gap-4">
              <span class="inline-flex items-center text-xs font-bold px-2.5 py-1 rounded-full border flex-shrink-0 mt-0.5"
                style="background-color:#e6f7fb; color:#006f87; border-color:#b3e4f0;">
                {{ track.code }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-800 text-sm leading-snug">{{ track.title }}</p>
                <div class="flex items-center gap-3 mt-1.5">
                  <router-link :to="{ name: 'AdminAbstracts', query: { track_id: track.id } }"
                    class="inline-flex items-center gap-1 text-xs font-medium transition-colors hover:underline"
                    style="color:#0095B6;">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    {{ track.abstract_count }} abstract{{ track.abstract_count !== 1 ? 's' : '' }}
                  </router-link>
                </div>
              </div>
              <button @click="startEdit(track)"
                class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-500 hover:border-gray-300 hover:text-gray-700 hover:bg-gray-50 transition flex-shrink-0">
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                </svg>
                Edit
              </button>
            </div>

            <!-- Edit mode (inline form) -->
            <div v-else class="space-y-3">
              <div class="flex items-center gap-2 mb-1">
                <span class="inline-flex items-center text-xs font-bold px-2.5 py-1 rounded-full border"
                  style="background-color:#e6f7fb; color:#006f87; border-color:#b3e4f0;">
                  {{ track.code }}
                </span>
                <span class="text-xs text-gray-400">Editing…</span>
              </div>

              <div class="grid sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Code</label>
                  <input v-model="editForm.code" type="text" class="input w-full text-sm"
                    placeholder="e.g. Track 1.1" />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Sort Order</label>
                  <input v-model.number="editForm.sort_order" type="number" class="input w-full text-sm" />
                </div>
              </div>

              <div>
                <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Track Title</label>
                <input v-model="editForm.title" type="text" class="input w-full text-sm"
                  placeholder="Full track subtitle" />
              </div>

              <div>
                <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Theme / Track Group</label>
                <input v-model="editForm.theme" type="text" class="input w-full text-sm"
                  placeholder="e.g. 1. Regional Health Security & Pandemic Agreement Implementation (Mohamed)" />
              </div>

              <p v-if="editError" class="text-xs text-red-500">{{ editError }}</p>
              <p v-if="editSuccess" class="text-xs text-green-600">{{ editSuccess }}</p>

              <div class="flex items-center gap-2 pt-1">
                <button @click="saveEdit(track.id)" :disabled="saving"
                  class="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white rounded-xl disabled:opacity-50 transition hover:opacity-90"
                  style="background-color:#0095B6;">
                  <svg v-if="saving" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                  </svg>
                  {{ saving ? 'Saving…' : 'Save Changes' }}
                </button>
                <button @click="cancelEdit"
                  class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 font-medium">
                  Cancel
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const tracks      = ref([])
const events      = ref([])
const loading     = ref(true)
const filterEvent = ref('')

const editingId   = ref(null)
const editForm    = ref({ code: '', title: '', theme: '', sort_order: 0 })
const saving      = ref(false)
const editError   = ref('')
const editSuccess = ref('')

const route = useRoute()

onMounted(async () => {
  // Honour ?track_id= or ?event_id= query param from other pages
  if (route.query.event_id) filterEvent.value = Number(route.query.event_id)

  await Promise.all([loadTracks(), loadEvents()])
  loading.value = false
})

const loadTracks = async () => {
  const params = filterEvent.value ? `?event_id=${filterEvent.value}` : ''
  const res = await api.get(`/abstracts/tracks/list${params}`)
  tracks.value = res.data
}

const loadEvents = async () => {
  const res = await api.get('/events/?skip=0&limit=200')
  events.value = res.data.data || []
}

watch(filterEvent, async () => {
  loading.value = true
  await loadTracks()
  loading.value = false
})

// Group tracks by theme
const groupedTracks = computed(() => {
  let list = tracks.value
  if (filterEvent.value) list = list.filter(t => t.event_id === filterEvent.value)

  const map = {}
  for (const t of list) {
    const key = t.theme || 'Ungrouped'
    if (!map[key]) map[key] = { theme: key, tracks: [] }
    map[key].tracks.push(t)
  }
  return Object.values(map)
})

const startEdit = (track) => {
  editingId.value = track.id
  editForm.value  = { code: track.code, title: track.title, theme: track.theme || '', sort_order: track.sort_order }
  editError.value   = ''
  editSuccess.value = ''
}

const cancelEdit = () => {
  editingId.value = null
  editError.value = ''
  editSuccess.value = ''
}

const saveEdit = async (trackId) => {
  saving.value    = true
  editError.value = ''
  editSuccess.value = ''
  try {
    const res = await api.put(`/abstracts/tracks/${trackId}`, editForm.value)
    // Update in place
    const idx = tracks.value.findIndex(t => t.id === trackId)
    if (idx !== -1) tracks.value[idx] = res.data
    editSuccess.value = 'Saved!'
    setTimeout(() => { editingId.value = null; editSuccess.value = '' }, 1200)
  } catch (e) {
    editError.value = e.response?.data?.detail || 'Failed to save'
  } finally {
    saving.value = false
  }
}
</script>
