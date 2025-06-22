<template>
  <div class="bg-gray-50 text-gray-800 font-sans">
    <!-- Banner/Header -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center" v-if="event">
      <div class="max-w-4xl mx-auto space-y-4">
        <h1 class="text-4xl font-bold">{{ event.event }}</h1>
        <p class="text-lg">
          {{ formatDate(event.start_date) }} – {{ formatDate(event.end_date) }} · {{ event.location }}
        </p>
      </div>
    </section>

    <!-- Loading/Error Fallback -->
    <section v-else class="text-center py-10">
      <DataLoadingSpinner v-if="loading" />
      <p v-else class="text-red-600">{{ error }}</p>
    </section>

    <!-- Registration Form -->
    <section v-if="event" class="max-w-5xl mx-auto px-4 py-10 space-y-12">
      <div class="space-y-6">
        <h2 class="text-2xl font-semibold text-bondi-blue">Register for this Event</h2>

        <!-- Error Alert -->
        <div v-if="registrationError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          {{ registrationError }}
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Personal Details -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Title *</label>
              <input v-model="title" required class="input-style" placeholder="Mr., Ms., Dr." />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name *</label>
              <input v-model="firstName" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Middle Name</label>
              <input v-model="middleName" class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name *</label>
              <input v-model="lastName" required class="input-style" />
            </div>
          </div>

          <!-- Gender & Profession -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Gender *</label>
              <select v-model="gender" required class="input-style">
                <option disabled value="">Select gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Profession *</label>
              <input v-model="profession" required class="input-style" />
            </div>
          </div>

          <!-- Organization & Position -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Organisation *</label>
              <input v-model="organisation" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Position</label>
              <input v-model="position" class="input-style" />
            </div>
          </div>

          <!-- Country -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Country *</label>
            <select v-model="country_id" required class="input-style">
              <option disabled value="">Select country</option>
              <option v-for="c in countries" :key="c.id" :value="c.id">
                {{ c.country }}
              </option>
            </select>
          </div>

          <!-- Contact -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input v-model="email" type="email" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
              <input v-model="phone" type="tel" required placeholder="+255..." class="input-style" />
            </div>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Organization's Participation Category *
            </label>
            <select v-model="participation_role" required class="input-style">
              <option disabled value="">Select category</option>
              <option>ECSA-HC secretariat</option>
              <option>Country delegate (from Ministry of Health)</option>
              <option>Participant from ECSA Member States</option>
              <option>Participant from other African countries</option>
              <option>Participant from the Rest of the World</option>
              <option>Student</option>
              <option>Sponsor/Exhibitor</option>
            </select>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition"
          >
            <span v-if="isSubmitting">Registering...</span>
            <span v-else>Register</span>
          </button>
        </form>

        <!-- Login Link -->
        <p class="text-center text-sm text-gray-600 pt-4">
          Already have an account?
          <router-link to="/login" class="text-bondi-blue hover:underline">Login</router-link>
        </p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

// Routing
const route = useRoute()
const router = useRouter()
const eventId = Number(route.params.id)

// State
const event = ref(null)
const loading = ref(true)
const error = ref(null)
const countries = ref([])
const registrationError = ref(null)
const isSubmitting = ref(false)

// Form fields
const title = ref('')
const firstName = ref('')
const middleName = ref('')
const lastName = ref('')
const gender = ref('')
const profession = ref('')
const organisation = ref('')
const position = ref('')
const country_id = ref('')
const email = ref('')
const phone = ref('')
const participation_role = ref('')

// Load event
const loadEventData = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/events/${eventId}`)
    event.value = res.data.event
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load event'
  } finally {
    loading.value = false
  }
}

// Fetch countries
const fetchCountries = async () => {
  try {
    const response = await api.get('/countries/', { params: { skip: 0, limit: 100 } })
    countries.value = response.data.data
  } catch (err) {
    console.error('Failed to fetch countries:', err)
  }
}

// Format date
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

// Form submit
const handleRegister = async () => {
  const payload = {
    event_id: eventId,
    title: title.value,
    first_name: firstName.value,
    middle_name: middleName.value,
    last_name: lastName.value,
    gender: gender.value,
    profession: profession.value,
    organisation: organisation.value,
    position: position.value,
    country_id: country_id.value,
    email: email.value,
    phone: phone.value,
    participation_role: participation_role.value,
  }

  registrationError.value = null
  isSubmitting.value = true

  try {
    await api.post('/events/registration/', payload)
    router.push({ name: 'EventPayment' }) // adjust route name if needed
  } catch (error) {
    console.error('Failed to register:', error)
    registrationError.value = error.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

// On mount
onMounted(() => {
  loadEventData()
  fetchCountries()
})
</script>

<style scoped>
.input-style {
  @apply w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent;
}
.text-bondi-blue {
  color: #0095b6;
}
.bg-bondi-blue {
  background-color: #0095b6;
}
</style>
