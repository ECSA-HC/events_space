<template>
  <div class="bg-gray-50 text-gray-800 font-sans">
    <!-- Banner/Header -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center" v-if="event">
      <div class="max-w-4xl mx-auto space-y-4">
        <router-link :to="{ name: 'Event', params: { id: event.id } }" class="text-4xl font-bold">{{ event.event }}</router-link>
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
              <select v-model="title" class="input-style">
                <option value="" disabled>Select title</option>
                <option value="Mr">Mr</option>
                <option value="Mrs">Mrs</option>
                <option value="Ms">Ms</option>
                <option value="Dr">Dr</option>
                <option value="Prof">Prof</option>
              </select>
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
          <div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Gender *</label>
              <select v-model="gender" required class="input-style">
                <option disabled value="">Select gender</option>
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </div>
          </div>

          <!-- Organization & Position -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input v-model="email" type="email" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone *</label>
              <input v-model="phone" type="text" required class="input-style" />
            </div>
          </div>

          <!-- Organization & Position -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Profession *</label>
              <input v-model="profession" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Position</label>
              <input v-model="position" class="input-style" />
            </div>
          </div>

          <!-- Country -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Organisation *</label>
              <input v-model="organisation" required class="input-style" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Country *</label>
              <select v-model="country_id" required class="input-style">
                <option disabled value="">Select country</option>
                <option v-for="c in countries" :key="c.id" :value="c.id">
                  {{ c.country }}
                </option>
              </select>
            </div>
          </div>
          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Organization's Participation Category *
            </label>
            <select v-model="participation_role" required class="input-style">
              <option disabled value="">Select category</option>
              <option value="secretariat">ECSA-HC secretariat</option>
              <option value="moh">Country delegate (from Ministry of Health)</option>
              <option value="member_state">Participant from ECSA Member States</option>
              <option value="other_africa">Participant from other African countries</option>
              <option value="world">Participant from the Rest of the World</option>
              <option value="student">Student</option>
              <option value="exibitor">Sponsor/Exhibitor</option>
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

// Router & Route
const route = useRoute()
const router = useRouter()
const eventId = route.params.id

// UI state
const successMessage = ref('')
const errorMessage = ref('')
const registrationError = ref(null)
const isSubmitting = ref(false)
const loading = ref(true)
const error = ref(null)

// Data
const event = ref(null)
const countries = ref([])

// Form fields
const user_id = ref('')
const title = ref('')
const firstName = ref('')
const middleName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const organisation = ref('')
const position = ref('')
const profession = ref('')
const gender = ref('')
const country_id = ref('')
const participation_role = ref('')

// Load event details
const loadEventData = async () => {
  try {
    const res = await api.get(`/events/${eventId}`)
    event.value = res.data.event
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load event'
  } finally {
    loading.value = false
  }
}

// Fetch country list
const fetchCountries = async () => {
  try {
    const res = await api.get('/countries/', { params: { skip: 0, limit: 100 } })
    countries.value = res.data.data
  } catch (err) {
    console.error('Failed to fetch countries:', err)
  }
}

// Format date for display
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

// Register flow
const handleRegister = async () => {
  try {
    isSubmitting.value = true
    errorMessage.value = ''

    const userPayload = {
      firstname: firstName.value,
      lastname: lastName.value,
      email: email.value,
      phone: phone.value,
    }

    const userProfilePayload = {
      title: title.value,
      middle_name: middleName.value,
      country_id: country_id.value,
      profession: profession.value,
      gender: gender.value,
      organisation: organisation.value,
      position: position.value,
    }

    const eventPayload = {
      event_id: eventId,
      participation_role: participation_role.value,
    }

    // Register the user
    const registerRes = await api.post("/auth/register", userPayload)
    if (!registerRes.data.user_id) throw new Error('User registration failed')

    user_id.value = registerRes.data.user_id

    // Create or update profile
    await api.post(`/users/profile/${user_id.value}`, userProfilePayload)

    // Register for event
    const eventRes = await api.post(`/events/registration/${user_id.value}`, eventPayload)
    const registrationId = eventRes.data.registration_id

    successMessage.value = 'Registration completed successfully!'

    // Navigate to payment page
    router.push({
      name: 'EventPayment',
      params: {
        event_id: eventId,
        registration_id: registrationId
      }
    })

  } catch (err) {
    console.error('Registration of user failed:', err)
    errorMessage.value = err.response?.data?.detail || 'An error occurred while completing your registration.'
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
