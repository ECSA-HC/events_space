<template>
  <div class="bg-gray-50 text-gray-800 font-sans min-h-screen p-6">
    <div v-if="loading" class="text-center py-12">
      <DataLoadingSpinner />
    </div>

    <div v-else-if="error" class="text-center text-red-600 py-12">
      {{ error }}
    </div>

    <div v-else class="max-w-4xl mx-auto bg-white rounded shadow space-y-8 p-6">
      <h1 class="text-3xl font-bold text-bondi-blue mb-6">Participant Status</h1>

      <!-- Registration Info -->
      <section>
        <h2 class="text-2xl font-semibold text-bondi-blue mb-4">Registration Info</h2>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
          <div>
            <dt class="font-medium">ID</dt>
            <dd>{{ status.registration_id }}</dd>
          </div>
          <div>
            <dt class="font-medium">Role</dt>
            <dd>{{ status.participation_role }}</dd>
          </div>
          <div>
            <dt class="font-medium">Paid</dt>
            <dd :class="status.paid ? 'text-green-600' : 'text-red-600'">{{ status.paid ? 'Yes' : 'No' }}</dd>
          </div>
          <div v-if="status.event_title">
            <dt class="font-medium">Event</dt>
            <dd>{{ status.event_title }}</dd>
          </div>
        </dl>
      </section>

      <!-- User Details -->
      <section>
        <h2 class="text-2xl font-semibold text-bondi-blue mb-4">User Details</h2>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
          <div>
            <dt class="font-medium">Name</dt>
            <dd>{{ status.user.firstname }} {{ status.user.lastname }}</dd>
          </div>
          <div>
            <dt class="font-medium">Phone</dt>
            <dd>{{ status.user.phone }}</dd>
          </div>
          <div>
            <dt class="font-medium">Email</dt>
            <dd>{{ status.user.email }}</dd>
          </div>
        </dl>
      </section>

      <!-- Payment Details -->
      <section v-if="status.payment">
        <h2 class="text-2xl font-semibold text-bondi-blue mb-4">Payment Details</h2>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
          <div>
            <dt class="font-medium">Status</dt>
            <dd>{{ status.payment.status || 'N/A' }}</dd>
          </div>
          <div>
            <dt class="font-medium">Amount</dt>
            <dd>{{ status.payment.amount || 'N/A' }}</dd>
          </div>
          <div>
            <dt class="font-medium">Paid At</dt>
            <dd>{{ formatDate(status.payment.paid_at) || 'N/A' }}</dd>
          </div>
        </dl>
      </section>

      <!-- Attendance -->
      <section>
        <h2 class="text-2xl font-semibold text-bondi-blue mb-4">Attendance</h2>
        <p class="mb-4"><strong>Days Attended:</strong> {{ status.attendance.count }}</p>
        <ul class="space-y-2 border rounded p-4 bg-gray-50 text-gray-700 max-h-64 overflow-auto">
          <li v-for="(date, index) in status.attendance.dates" :key="index" class="px-3 py-1 bg-white rounded shadow-sm">
            {{ formatDate(date) }}
          </li>
        </ul>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

const registrationId = 36 // replace as needed or get from route

const status = ref(null)
const loading = ref(true)
const error = ref(null)

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

async function fetchStatus() {
  loading.value = true
  error.value = null
  try {
    const res = await axios.get(`/registrations/participant_status/${registrationId}`)
    status.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load participant status.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStatus()
})
</script>

<style scoped>
.text-bondi-blue {
  color: #0095b6;
}
</style>
