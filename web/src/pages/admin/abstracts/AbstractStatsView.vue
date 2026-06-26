<template>
  <div class="flex-1 flex flex-col w-full max-w-7xl mx-auto p-6 space-y-6">

    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-black">Abstract Reports</h1>
        <p v-if="!loading" class="text-sm text-gray-400 mt-0.5">{{ stats.total }} abstracts total</p>
      </div>
      <select v-model.number="filterEvent" class="input w-56">
        <option :value="null">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
    </div>

    <div v-if="loading" class="text-gray-400 text-sm py-12 text-center">Loading stats…</div>

    <template v-else>

      <!-- ── KPI cards ─────────────────────────────────────────────────────── -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div v-for="kpi in kpis" :key="kpi.label"
          class="bg-white rounded-2xl shadow p-5 flex flex-col gap-1"
          :style="kpi.accent ? `border-top: 4px solid ${kpi.accent}` : 'border-top: 4px solid #e5e7eb'">
          <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">{{ kpi.label }}</p>
          <p class="text-3xl font-bold" :style="kpi.accent ? `color:${kpi.accent}` : 'color:#111827'">
            {{ kpi.value }}
          </p>
          <p v-if="kpi.sub" class="text-xs text-gray-400">{{ kpi.sub }}</p>
        </div>
      </div>

      <!-- ── Row 1: Status bar + Type donut ───────────────────────────────── -->
      <div class="grid lg:grid-cols-2 gap-6">

        <!-- By Status -->
        <div class="bg-white rounded-2xl shadow p-6">
          <h2 class="font-semibold text-gray-700 mb-4">Abstracts by Status</h2>
          <div class="space-y-3">
            <div v-for="s in statusBars" :key="s.label" class="flex items-center gap-3">
              <span class="w-28 text-xs text-gray-500 text-right flex-shrink-0">{{ s.label }}</span>
              <div class="flex-1 bg-gray-100 rounded-full h-5 overflow-hidden">
                <div class="h-5 rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                  :style="{ width: s.pct + '%', backgroundColor: s.color, minWidth: s.count ? '2rem' : '0' }">
                  <span class="text-white text-xs font-bold leading-none">{{ s.count }}</span>
                </div>
              </div>
              <span class="w-10 text-xs text-gray-400 flex-shrink-0">{{ s.pct }}%</span>
            </div>
          </div>
        </div>

        <!-- By Type (donut) -->
        <div class="bg-white rounded-2xl shadow p-6 flex flex-col">
          <h2 class="font-semibold text-gray-700 mb-4">Presentation Type</h2>
          <div class="flex items-center justify-center gap-10 flex-1">
            <svg :viewBox="`0 0 ${D} ${D}`" class="w-40 h-40 -rotate-90">
              <circle :cx="D/2" :cy="D/2" :r="R" fill="none" :stroke="'#f3f4f6'" :stroke-width="W" />
              <circle v-for="seg in donutSegs" :key="seg.label"
                :cx="D/2" :cy="D/2" :r="R" fill="none"
                :stroke="seg.color"
                :stroke-width="W"
                :stroke-dasharray="`${seg.dash} ${circumference - seg.dash}`"
                :stroke-dashoffset="-seg.offset"
                stroke-linecap="round" />
            </svg>
            <div class="space-y-3">
              <div v-for="seg in donutSegs" :key="seg.label" class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full flex-shrink-0" :style="{ backgroundColor: seg.color }"></span>
                <div>
                  <p class="text-sm font-semibold text-gray-700">{{ seg.count }}</p>
                  <p class="text-xs text-gray-400 capitalize">{{ seg.label }}</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-gray-200 flex-shrink-0"></span>
                <div>
                  <p class="text-sm font-semibold text-gray-700">{{ unspecifiedCount }}</p>
                  <p class="text-xs text-gray-400">Unspecified</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Row 2: Countries ──────────────────────────────────────────────── -->
      <div class="bg-white rounded-2xl shadow p-6">
        <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
          <h2 class="font-semibold text-gray-700">Abstracts by Country</h2>
          <span class="text-xs text-gray-400">Showing top {{ Math.min(countryRows.length, showAllCountries ? 999 : 15) }} of {{ countryRows.length }}</span>
        </div>
        <div class="space-y-2">
          <div v-for="c in visibleCountries" :key="c.country" class="flex items-center gap-3 group">
            <!-- Country label -->
            <div class="w-32 sm:w-40 flex-shrink-0 flex items-center gap-1.5">
              <span v-if="isEswatini(c.country)"
                class="text-xs font-bold px-1.5 py-0.5 rounded"
                style="background:#d1fae5;color:#065f46;">ESW</span>
              <span class="text-xs text-gray-600 truncate font-medium group-[.esw]:font-bold">{{ c.country }}</span>
            </div>
            <!-- Stacked bar -->
            <div class="flex-1 flex rounded-full overflow-hidden h-5 bg-gray-100">
              <!-- Accepted portion -->
              <div class="h-5 transition-all duration-500 flex items-center justify-end"
                :style="{ width: (c.accepted / maxCountryTotal * 100) + '%', backgroundColor: '#0095B6', minWidth: c.accepted ? '1.5rem' : '0' }">
                <span v-if="c.accepted" class="text-white text-xs font-bold pr-1.5">{{ c.accepted }}</span>
              </div>
              <!-- Non-accepted portion -->
              <div class="h-5 transition-all duration-500"
                :style="{ width: ((c.total - c.accepted) / maxCountryTotal * 100) + '%', backgroundColor: '#bae6fd' }">
              </div>
            </div>
            <span class="w-8 text-xs text-gray-400 flex-shrink-0 text-right">{{ c.total }}</span>
          </div>
        </div>
        <!-- Legend -->
        <div class="mt-3 flex items-center gap-4 text-xs text-gray-400">
          <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm inline-block" style="background:#0095B6"></span> Accepted</span>
          <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm inline-block" style="background:#bae6fd"></span> Other</span>
        </div>
        <button v-if="countryRows.length > 15" @click="showAllCountries = !showAllCountries"
          class="mt-3 text-xs font-medium hover:underline" style="color:#0095B6;">
          {{ showAllCountries ? 'Show less ▲' : `Show all ${countryRows.length} countries ▼` }}
        </button>
      </div>

      <!-- ── Row 3: By Track ───────────────────────────────────────────────── -->
      <div class="bg-white rounded-2xl shadow p-6">
        <h2 class="font-semibold text-gray-700 mb-4">Abstracts by Track</h2>
        <div v-if="trackBars.length === 0" class="text-gray-400 text-sm text-center py-4">No track data</div>
        <div v-else class="space-y-2">
          <div v-for="t in trackBars" :key="t.label" class="flex items-center gap-3">
            <span class="w-48 text-xs text-gray-500 truncate flex-shrink-0" :title="t.label">{{ t.label }}</span>
            <div class="flex-1 flex rounded-full overflow-hidden h-5 bg-gray-100">
              <div class="h-5 transition-all duration-500 flex items-center justify-end"
                :style="{ width: (t.accepted / t.total * 100) + '%', backgroundColor: '#0095B6', minWidth: t.accepted ? '1.5rem' : '0' }">
                <span v-if="t.accepted" class="text-white text-xs font-bold pr-1.5">{{ t.accepted }}</span>
              </div>
              <div class="h-5 transition-all duration-500"
                :style="{ width: ((t.total - t.accepted) / t.total * 100) + '%', backgroundColor: '#e0f2fe' }">
              </div>
            </div>
            <span class="w-8 text-xs text-gray-400 flex-shrink-0 text-right">{{ t.total }}</span>
          </div>
        </div>
        <div class="mt-3 flex items-center gap-4 text-xs text-gray-400">
          <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm inline-block" style="background:#0095B6"></span> Accepted</span>
          <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm inline-block" style="background:#e0f2fe"></span> Other</span>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/plugins/axios'

const loading     = ref(true)
const filterEvent = ref(null)
const stats       = ref({ total: 0, total_accepted: 0, eswatini_accepted: 0, by_status: [], by_type: [], by_track: [], by_country: [], events: [] })
const showAllCountries = ref(false)

// Donut geometry
const D = 140, W = 22, R = (D - W) / 2
const circumference = computed(() => 2 * Math.PI * R)

const events = computed(() => stats.value.events || [])

const kpis = computed(() => {
  const s = stats.value
  const accepted = s.total_accepted || 0
  const pct = s.total ? Math.round(accepted / s.total * 100) : 0
  const oral   = (s.by_type.find(t => t.type === 'oral')?.count)   || 0
  const poster = (s.by_type.find(t => t.type === 'poster')?.count) || 0
  const countries = new Set((s.by_country || []).map(c => c.country)).size
  return [
    { label: 'Total Abstracts',     value: s.total,              accent: '#6b7280' },
    { label: 'Accepted',            value: accepted,             accent: '#0095B6', sub: `${pct}% acceptance rate` },
    { label: 'Oral',                value: oral,                 accent: '#1B3F6E' },
    { label: 'Poster',              value: poster,               accent: '#F7941D' },
    { label: 'Eswatini (accepted)', value: s.eswatini_accepted,  accent: '#059669', sub: 'require ethical clearance' },
  ]
})

const STATUS_COLORS = {
  accepted:         '#0095B6',
  submitted:        '#3b82f6',
  under_review:     '#f59e0b',
  rejected:         '#ef4444',
  revision_required:'#f97316',
}
const statusBars = computed(() => {
  const total = stats.value.total || 1
  return (stats.value.by_status || [])
    .sort((a, b) => b.count - a.count)
    .map(s => ({
      label: s.status.replace('_', ' '),
      count: s.count,
      pct:   Math.round(s.count / total * 100),
      color: STATUS_COLORS[s.status] || '#9ca3af',
    }))
})

const TYPE_COLORS = { oral: '#1B3F6E', poster: '#F7941D', unspecified: '#d1d5db' }
const donutSegs = computed(() => {
  const circ = circumference.value
  const types = (stats.value.by_type || []).filter(t => t.type !== 'unspecified')
  const total = types.reduce((s, t) => s + t.count, 0) || 1
  let offset = 0
  return types.map(t => {
    const dash = (t.count / total) * circ
    const seg = { label: t.type, count: t.count, color: TYPE_COLORS[t.type] || '#9ca3af', dash, offset }
    offset += dash
    return seg
  })
})
const unspecifiedCount = computed(() =>
  (stats.value.by_type || []).find(t => t.type === 'unspecified')?.count || 0
)

const countryRows = computed(() =>
  (stats.value.by_country || []).filter(c => c.country)
)
const maxCountryTotal = computed(() => Math.max(...countryRows.value.map(c => c.total), 1))
const visibleCountries = computed(() =>
  showAllCountries.value ? countryRows.value : countryRows.value.slice(0, 15)
)
const isEswatini = (c) => ['eswatini','swaziland'].includes((c||'').trim().toLowerCase())

const trackBars = computed(() =>
  (stats.value.by_track || []).filter(t => t.track !== 'Untracked')
)

async function fetchStats() {
  loading.value = true
  try {
    const params = filterEvent.value ? `?event_id=${filterEvent.value}` : ''
    const res = await api.get(`/abstracts/stats${params}`)
    stats.value = res.data
  } catch (e) {
    console.error('Failed to load stats', e)
  } finally {
    loading.value = false
  }
}

watch(filterEvent, fetchStats)
onMounted(fetchStats)
</script>
