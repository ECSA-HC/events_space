<template>
  <div class="bg-gray-50 text-gray-800 font-sans">
    <!-- Banner -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center">
      <div class="max-w-2xl mx-auto space-y-3">
        <h1 class="text-4xl font-bold tracking-tight">{{ event?.event }}</h1>
        <p class="text-lg">
          {{ formatDate(event?.start_date) }} – {{ formatDate(event?.end_date) }} &middot;
          {{ event?.location }}
        </p>
        <p class="text-base text-white/90">
          Please enter your Registration ID to mark attendance.
        </p>
      </div>
    </section>

    <!-- Attendance Form -->
    <section class="max-w-md mx-auto px-6 py-12">
      <div class="bg-white p-6 rounded-lg shadow space-y-4">
        <label for="participantId" class="block text-sm font-medium text-gray-700">
          Registration ID
        </label>
        <input
          v-model="participantId"
          type="number"
          id="participantId"
          placeholder="Enter your Registration ID (e.g. 36)"
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-bondi-blue"
        />

        <button
          @click="markAttendance"
          :disabled="!participantId || loading"
          class="w-full bg-bondi-blue text-white font-semibold py-2 px-4 rounded-md hover:bg-bondi-blue/90 disabled:opacity-50"
        >
          {{ loading ? 'Marking...' : 'Mark Attendance' }}
        </button>

        <p v-if="successMessage" class="text-green-600 text-sm">{{ successMessage }}</p>
        <p v-if="errorMessage" class="text-red-600 text-sm">{{ errorMessage }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route = useRoute()
const eventId = Number(route.params.id)

const event = ref(null)
const participantId = ref('')
const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

async function loadEvent() {
  try {
    const res = await api.get(`/events/${eventId}`)
    event.value = res.data.event
  } catch (error) {
    console.error('Failed to load event:', error)
    errorMessage.value = 'Failed to load event details.'
  }
}

async function markAttendance() {
  loading.value = true
  successMessage.value = ''
  errorMessage.value = ''
  const regId = parseInt(participantId.value, 10)

  if (isNaN(regId)) {
    errorMessage.value = 'Please enter a valid Registration ID number.'
    loading.value = false
    return
  }

  try {
    const res = await api.post(`/event_attendance/events/${eventId}/attendance`, {
      registration_id: regId
    })
    successMessage.value = res.data.message || 'Attendance marked successfully.'
    participantId.value = ''
  } catch (err) {
    errorMessage.value = err.response?.data?.detail || 'Failed to mark attendance.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadEvent()
})
</script>

<style scoped>
.text-bondi-blue {
  color: #0095b6;
}
.bg-bondi-blue {
  background-color: #0095b6;
}
</style>
