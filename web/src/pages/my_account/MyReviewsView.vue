<template>
  <div class="space-y-8 flex-1">
    <h1 class="text-2xl font-semibold text-black">My Assigned Reviews</h1>

    <div v-if="loading" class="text-gray-500">Loading...</div>
    <div v-else-if="assignments.length === 0" class="bg-white rounded-2xl shadow p-8 text-center text-gray-400">
      No abstracts assigned for review.
    </div>

    <div v-else class="space-y-4">
      <div v-for="a in assignments" :key="a.assignment_id" class="bg-white rounded-2xl shadow p-6">
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div class="flex-1">
            <h2 class="font-semibold text-gray-800 text-lg">{{ a.abstract.title }}</h2>
            <p class="text-gray-500 text-sm mt-1">{{ a.abstract.event }} &bull; {{ a.abstract.track || 'No track' }}</p>
            <p class="text-gray-400 text-xs mt-1">{{ a.abstract.word_count }} words &bull; Assigned {{ formatDate(a.assigned_at) }}</p>
          </div>
          <span :class="a.completed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
            class="px-3 py-1 rounded-full text-sm font-semibold flex-shrink-0">
            {{ a.completed ? 'Reviewed' : 'Pending Review' }}
          </span>
        </div>

        <!-- Authors -->
        <div class="mt-3 flex flex-wrap gap-1">
          <span v-for="au in a.abstract.authors" :key="au.id" class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
            {{ au.firstname }} {{ au.lastname }}<span v-if="au.affiliation"> · {{ au.affiliation }}</span>
          </span>
        </div>

        <!-- Abstract text (always shown for reviewer) -->
        <div class="mt-4 text-gray-700 text-sm leading-relaxed border-t pt-3 whitespace-pre-wrap">{{ a.abstract.abstract_text }}</div>
        <p v-if="a.abstract.keywords" class="mt-2 text-xs text-gray-400"><strong>Keywords:</strong> {{ a.abstract.keywords }}</p>

        <!-- Submitted review -->
        <div v-if="a.review" class="mt-5 bg-green-50 border border-green-200 rounded-xl p-4">
          <p class="text-sm font-semibold text-green-700 mb-3">Your Review — <span class="capitalize">{{ a.review.recommendation?.replace('_',' ') }}</span></p>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-3">
            <div class="bg-white rounded-lg p-2 text-center border">
              <p class="text-xs text-gray-400">Relevance</p>
              <p class="font-bold text-bondi-blue">{{ a.review.relevance_score }}/5</p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center border">
              <p class="text-xs text-gray-400">Methodology</p>
              <p class="font-bold text-bondi-blue">{{ a.review.methodology_score }}/5</p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center border">
              <p class="text-xs text-gray-400">Originality</p>
              <p class="font-bold text-bondi-blue">{{ a.review.originality_score }}/5</p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center border">
              <p class="text-xs text-gray-400">Overall</p>
              <p class="font-bold text-bondi-blue">{{ a.review.overall_score }}/5</p>
            </div>
          </div>
          <p class="text-sm text-gray-700">{{ a.review.comments }}</p>
        </div>

        <!-- Review form (if not reviewed) -->
        <div v-else class="mt-5 border-t pt-4">
          <h3 class="font-semibold text-gray-700 mb-4">Submit Your Review</h3>
          <div class="grid sm:grid-cols-2 gap-4">
            <div v-for="field in scoreFields" :key="field.key">
              <label class="block text-sm font-medium text-gray-700 mb-1">{{ field.label }} <span class="text-gray-400 text-xs">(1–5)</span></label>
              <div class="flex gap-2">
                <button v-for="n in 5" :key="n"
                  @click="a._form[field.key] = n"
                  :class="a._form[field.key] >= n ? 'bg-bondi-blue text-white' : 'bg-gray-100 text-gray-600'"
                  class="w-9 h-9 rounded-lg font-semibold text-sm transition">{{ n }}</button>
              </div>
            </div>
          </div>
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Recommendation <span class="text-red-500">*</span></label>
            <select v-model="a._form.recommendation" class="input w-full sm:w-64">
              <option value="">Select recommendation</option>
              <option value="accept">Accept</option>
              <option value="revision_required">Revision Required</option>
              <option value="reject">Reject</option>
            </select>
          </div>
          <div class="mt-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">Comments to Author <span class="text-red-500">*</span></label>
            <textarea v-model="a._form.comments" rows="4" class="input w-full" placeholder="Your review comments..."></textarea>
          </div>
          <div class="mt-3">
            <label class="block text-sm font-medium text-gray-700 mb-1">Confidential Comments (to chair only)</label>
            <textarea v-model="a._form.confidential_comments" rows="2" class="input w-full" placeholder="Optional..."></textarea>
          </div>
          <div class="mt-4 flex items-center gap-3">
            <button @click="submitReview(a)" class="px-5 py-2 bg-bondi-blue text-white rounded-lg text-sm font-semibold hover:opacity-90 transition">Submit Review</button>
            <span v-if="a._error" class="text-red-500 text-sm">{{ a._error }}</span>
            <span v-if="a._success" class="text-green-600 text-sm">{{ a._success }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'

const assignments = ref([])
const loading = ref(true)

const scoreFields = [
  { key: 'relevance_score', label: 'Relevance' },
  { key: 'methodology_score', label: 'Methodology' },
  { key: 'originality_score', label: 'Originality' },
  { key: 'overall_score', label: 'Overall Score' },
]

onMounted(async () => {
  try {
    const res = await api.get('/abstracts/my-reviews')
    assignments.value = res.data.map(a => ({
      ...a,
      _form: { relevance_score: 0, methodology_score: 0, originality_score: 0, overall_score: 0, recommendation: '', comments: '', confidential_comments: '' },
      _error: '',
      _success: '',
    }))
  } catch (e) {
    console.error('Failed to load reviews', e)
  } finally {
    loading.value = false
  }
})

const submitReview = async (a) => {
  a._error = ''
  const f = a._form
  if (!f.relevance_score || !f.methodology_score || !f.originality_score || !f.overall_score) {
    a._error = 'Please score all criteria.'; return
  }
  if (!f.recommendation) { a._error = 'Please select a recommendation.'; return }
  if (!f.comments.trim()) { a._error = 'Please add comments.'; return }
  try {
    await api.post(`/abstracts/reviews/${a.assignment_id}`, f)
    a.review = { ...f }
    a.completed = true
    a._success = 'Review submitted!'
  } catch(e) {
    a._error = e.response?.data?.detail || 'Failed to submit review.'
  }
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'short', year:'numeric' }) : '—'
</script>
