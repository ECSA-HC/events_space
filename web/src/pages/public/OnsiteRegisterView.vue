<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-10">
    <div class="w-full max-w-md">

      <!-- Success State -->
      <div v-if="registered" class="bg-white rounded-2xl shadow-lg p-8 text-center">
        <div class="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-2">Registration Complete!</h2>
        <p class="text-gray-600 mb-1">{{ successMessage }}</p>
        <p class="text-sm text-gray-400 mb-6">You have been marked as paid. No further payment required.</p>
        <button
          @click="resetForm"
          class="px-6 py-2 rounded-full font-semibold text-sm text-white transition hover:opacity-90"
          style="background-color: #0095B6;"
        >Register Another Person</button>
      </div>

      <!-- Registration Form -->
      <div v-else class="bg-white rounded-2xl shadow-lg p-8">
        <div class="text-center mb-6">
          <div class="h-14 w-14 rounded-xl flex items-center justify-center mx-auto mb-3" style="background-color: #1B3F6E;">
            <svg class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
            </svg>
          </div>
          <h1 class="text-xl font-bold text-gray-900">On-Site Registration</h1>
          <p class="text-sm text-gray-500 mt-1">{{ eventName }}</p>
        </div>

        <!-- Error -->
        <div v-if="errorMsg" class="mb-4 p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="submitRegistration" class="space-y-4">
          <!-- First Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">First Name <span class="text-red-500">*</span></label>
            <input
              v-model="form.firstname"
              type="text"
              required
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              placeholder="e.g. Davis"
            />
          </div>

          <!-- Last Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Last Name <span class="text-red-500">*</span></label>
            <input
              v-model="form.lastname"
              type="text"
              required
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              placeholder="e.g. Kondo"
            />
          </div>

          <!-- Designation -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Designation</label>
            <input
              v-model="form.designation"
              type="text"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              placeholder="e.g. Director of Health Services"
            />
          </div>

          <!-- Organisation -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Organisation</label>
            <input
              v-model="form.organisation"
              type="text"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              placeholder="e.g. Ministry of Health"
            />
          </div>

          <!-- Email (optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email <span class="text-gray-400">(optional)</span></label>
            <input
              v-model="form.email"
              type="email"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
              placeholder="e.g. davis@example.com"
            />
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="submitting"
            class="w-full py-3 rounded-lg font-semibold text-sm text-white transition hover:opacity-90 disabled:opacity-50 disabled:cursor-wait"
            style="background-color: #0095B6;"
          >
            {{ submitting ? 'Registering…' : 'Register & Mark as Paid' }}
          </button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route = useRoute()

const form = ref({
  firstname: '',
  lastname: '',
  designation: '',
  organisation: '',
  email: '',
})

const eventId = ref(null)
const eventName = ref('')
const registered = ref(false)
const submitting = ref(false)
const errorMsg = ref('')
const successMessage = ref('')

onMounted(async () => {
  eventId.value = route.query.event_id
  if (eventId.value) {
    try {
      const res = await api.get(`/events/${eventId.value}`)
      eventName.value = res.data.event?.event || ''
    } catch (e) {
      console.error('Failed to load event', e)
    }
  }
})

async function submitRegistration() {
  errorMsg.value = ''
  if (!form.value.firstname.trim() || !form.value.lastname.trim()) {
    errorMsg.value = 'First name and last name are required.'
    return
  }
  if (!eventId.value) {
    errorMsg.value = 'No event specified.'
    return
  }

  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('event_id', eventId.value)
    formData.append('firstname', form.value.firstname.trim())
    formData.append('lastname', form.value.lastname.trim())
    if (form.value.designation.trim()) formData.append('designation', form.value.designation.trim())
    if (form.value.organisation.trim()) formData.append('organisation', form.value.organisation.trim())
    if (form.value.email.trim()) formData.append('email', form.value.email.trim())

    const res = await api.post('/events/onsite-register/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    successMessage.value = res.data.message || 'Registration complete.'
    registered.value = true
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = { firstname: '', lastname: '', designation: '', organisation: '', email: '' }
  registered.value = false
  successMessage.value = ''
}
</script>
