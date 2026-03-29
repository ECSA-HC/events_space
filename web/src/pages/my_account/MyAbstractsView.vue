<template>
  <div class="space-y-8 flex-1">
    <h1 class="text-2xl font-semibold text-black">My Abstract Submissions</h1>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="abstracts.length === 0" class="bg-white rounded-2xl shadow p-8 text-center text-gray-400">
      <p class="text-lg">No abstracts submitted yet.</p>
      <router-link :to="{ name: 'AbstractSubmission' }" class="mt-3 inline-block text-bondi-blue underline text-sm">Submit an abstract</router-link>
    </div>

    <div v-else class="space-y-4">
      <div v-for="abs in abstracts" :key="abs.id" class="bg-white rounded-2xl shadow p-6">
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div class="flex-1">
            <h2 class="font-semibold text-gray-800 text-lg">{{ abs.title }}</h2>
            <p class="text-gray-500 text-sm mt-1">{{ abs.event }} &bull; {{ abs.track || 'No track' }}</p>
            <p class="text-gray-400 text-xs mt-1">{{ abs.word_count }} words &bull; Submitted {{ formatDate(abs.created_at) }}</p>
          </div>
          <span :class="statusClass(abs.status)" class="px-3 py-1 rounded-full text-sm font-semibold capitalize flex-shrink-0">
            {{ abs.status?.replace('_', ' ') }}
          </span>
        </div>

        <!-- Authors -->
        <div class="mt-4 flex flex-wrap gap-2">
          <span v-for="(au, i) in abs.authors" :key="au.id"
            class="inline-flex items-center gap-1 text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">
            <span class="font-medium">{{ au.firstname }} {{ au.lastname }}</span>
            <span v-if="au.is_presenting" class="bg-bondi-blue text-white text-xs px-1 rounded">Presenting</span>
            <span v-if="au.affiliation" class="text-gray-400">· {{ au.affiliation }}</span>
          </span>
        </div>

        <!-- Expandable abstract text -->
        <div class="mt-4">
          <button @click="abs._expanded = !abs._expanded" class="text-bondi-blue text-sm hover:underline">
            {{ abs._expanded ? 'Hide abstract ▲' : 'Show abstract ▼' }}
          </button>
          <div v-if="abs._expanded" class="mt-3 text-gray-700 text-sm leading-relaxed border-t pt-3 whitespace-pre-wrap">
            {{ abs.abstract_text }}
            <p v-if="abs.keywords" class="mt-3 text-xs text-gray-400"><strong>Keywords:</strong> {{ abs.keywords }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'

const abstracts = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/abstracts/my-submissions')
    abstracts.value = res.data.map(a => ({ ...a, _expanded: false }))
  } catch (e) {
    console.error('Failed to load abstracts', e)
  } finally {
    loading.value = false
  }
})

const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' }) : '—'
const statusClass = (s) => ({ submitted:'bg-blue-100 text-blue-700', under_review:'bg-yellow-100 text-yellow-700', accepted:'bg-green-100 text-green-700', rejected:'bg-red-100 text-red-700', revision_required:'bg-orange-100 text-orange-700' }[s] || 'bg-gray-100 text-gray-600')
</script>
