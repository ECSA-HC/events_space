<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-10">
    <div class="w-full max-w-md">

      <!-- Success State -->
      <div v-if="registered" class="bg-white rounded-2xl shadow-lg p-8 text-center">
        <!-- One coherent state, not two contradictory ones: an already-
             registered match gets its own amber framing entirely (no green
             "Registration Complete!" checkmark implying a fresh sign-up). -->
        <template v-if="alreadyRegistered">
          <div class="h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-4" style="background:#fef3c7;">
            <span class="text-3xl leading-none">⚠️</span>
          </div>
          <h2 class="text-xl font-bold text-gray-900 mb-2">Already Registered</h2>
          <p class="text-gray-600 mb-1">This person already had a registration for this event — we've updated it, not created a new one.</p>
          <p class="text-sm text-gray-400 mb-6">They are now marked as paid. No further payment required.</p>
        </template>
        <template v-else>
          <div class="h-16 w-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <h2 class="text-xl font-bold text-gray-900 mb-2">Registration Complete!</h2>
          <p class="text-gray-600 mb-1">{{ successMessage }}</p>
          <p class="text-sm text-gray-400 mb-6">You have been marked as paid. No further payment required.</p>
        </template>
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

        <!-- Event picker — shown only when the QR link didn't carry an event_id -->
        <div v-if="needsEventPicker" class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Event <span class="text-red-500">*</span></label>
          <select
            v-model="eventId"
            required
            @change="onEventPicked"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
          >
            <option disabled :value="null">Select the event</option>
            <option v-for="ev in availableEvents" :key="ev.id" :value="ev.id">{{ ev.event }}</option>
          </select>
        </div>

        <form @submit.prevent="submitRegistration" class="space-y-4">
          <!-- Role -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Role <span class="text-red-500">*</span></label>
            <select
              v-model="form.participation_role"
              required
              @change="onRoleChange"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 text-sm"
            >
              <option disabled value="">Select your role</option>
              <option v-for="r in ONSITE_ROLES" :key="r.value" :value="r.value">{{ r.label }}</option>
            </select>
            <p v-if="autoFilledRole" class="text-xs text-gray-400 mt-1">
              Designation and organisation filled in for you — edit below if needed.
            </p>
          </div>

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

          <!-- Country (optional) -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Country <span class="text-gray-400">(if available)</span></label>
            <CountrySelect v-model="form.country_id" />
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
            {{ submitting ? 'Registering…' : 'Register' }}
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
import { PARTICIPATION_ROLES } from '@/constants/participationRoles'
import CountrySelect from '@/components/common/CountrySelect.vue'

const route = useRoute()

// Roles someone might plausibly walk up and register as on the day —
// the full admin list also has pre-registration-only categories
// (Presenter, Speaker, Student, etc.) that don't make sense here.
const ONSITE_ROLE_KEYS = [
  'secretariat', 'local_secretariat', 'usher', 'driver', 'medical_staff', 'media',
  'exhibitor', 'sponsor', 'delegate', 'member_state', 'other_africa',
  'world', 'moh', 'participant',
]
const ONSITE_ROLES = PARTICIPATION_ROLES.filter(r => ONSITE_ROLE_KEYS.includes(r.value))

// Known internal/support roles have a fixed designation & organisation —
// fill them in automatically so whoever's staffing the desk doesn't have
// to type the same thing for every usher/driver/medical staff member.
const AUTO_FILL = {
  secretariat:       { designation: 'ECSA-HC Secretariat', organisation: 'ECSA-HC' },
  local_secretariat: { designation: 'Local Secretariat',    organisation: 'ECSA-HC' },
  usher:             { designation: 'Usher',                organisation: 'ECSA-HC' },
  driver:            { designation: 'Driver',                organisation: 'ECSA-HC' },
  medical_staff:     { designation: 'Medical Staff',         organisation: 'ECSA-HC' },
}

const form = ref({
  participation_role: '',
  firstname: '',
  lastname: '',
  designation: '',
  organisation: '',
  country_id: null,
  email: '',
})

const autoFilledRole = ref(false)
const eventId = ref(null)
const eventName = ref('')
const registered = ref(false)
const submitting = ref(false)
const errorMsg = ref('')
const successMessage = ref('')
const alreadyRegistered = ref(false)
const needsEventPicker = ref(false)
const availableEvents = ref([])

function onEventPicked() {
  errorMsg.value = ''
  const ev = availableEvents.value.find(e => e.id === eventId.value)
  eventName.value = ev?.event || ''
}

function onRoleChange() {
  const preset = AUTO_FILL[form.value.participation_role]
  if (preset) {
    form.value.designation = preset.designation
    form.value.organisation = preset.organisation
    autoFilledRole.value = true
  } else {
    // Only clear the fields if what's in them right now is our own
    // auto-fill from a previous role — never wipe something the person
    // actually typed themselves.
    if (autoFilledRole.value) {
      form.value.designation = ''
      form.value.organisation = ''
    }
    autoFilledRole.value = false
  }
}

onMounted(async () => {
  if (route.query.event_id) {
    eventId.value = Number(route.query.event_id)
    try {
      const res = await api.get(`/events/${eventId.value}`)
      eventName.value = res.data.event?.event || ''
    } catch (e) {
      console.error('Failed to load event', e)
    }
    return
  }

  // The QR link didn't carry an event_id (stale link, bookmark, manual visit).
  // Fall back to letting whoever's staffing the desk pick the event —
  // auto-select it silently if there's exactly one currently running.
  try {
    const res = await api.get('/events/', { params: { limit: 100 } })
    const events = res.data?.data || []
    availableEvents.value = events

    const today = new Date()
    const current = events.filter(ev => {
      if (!ev.start_date || !ev.end_date) return false
      return new Date(ev.start_date) <= today && today <= new Date(ev.end_date)
    })

    if (current.length === 1) {
      eventId.value = current[0].id
      eventName.value = current[0].event
    } else if (events.length === 1) {
      eventId.value = events[0].id
      eventName.value = events[0].event
    } else {
      needsEventPicker.value = true
    }
  } catch (e) {
    console.error('Failed to load events list', e)
    needsEventPicker.value = true
  }
})

async function submitRegistration() {
  errorMsg.value = ''
  if (!form.value.participation_role) {
    errorMsg.value = 'Please select your role.'
    return
  }
  if (!form.value.firstname.trim() || !form.value.lastname.trim()) {
    errorMsg.value = 'First name and last name are required.'
    return
  }
  if (!eventId.value) {
    errorMsg.value = needsEventPicker.value ? 'Please select the event.' : 'No event specified.'
    return
  }

  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('event_id', eventId.value)
    formData.append('participation_role', form.value.participation_role)
    formData.append('firstname', form.value.firstname.trim())
    formData.append('lastname', form.value.lastname.trim())
    if (form.value.designation.trim()) formData.append('designation', form.value.designation.trim())
    if (form.value.organisation.trim()) formData.append('organisation', form.value.organisation.trim())
    if (form.value.country_id) formData.append('country_id', form.value.country_id)
    if (form.value.email.trim()) formData.append('email', form.value.email.trim())

    const res = await api.post('/events/onsite-register/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    successMessage.value = res.data.message || 'Registration complete.'
    alreadyRegistered.value = !!res.data.already_registered
    registered.value = true
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.value = { participation_role: '', firstname: '', lastname: '', designation: '', organisation: '', country_id: null, email: '' }
  autoFilledRole.value = false
  registered.value = false
  successMessage.value = ''
  alreadyRegistered.value = false
}
</script>
