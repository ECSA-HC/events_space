<template>
  <div class="space-y-8 flex-1">
    <!-- Title -->
    <h1 class="text-2xl text-black">
      Welcome back, <span class="font-semibold text-black">{{ user.name }}</span>!
    </h1>

    <!-- Error message -->
    <p v-if="error" class="text-red-600">{{ error }}</p>

    <!-- Loading -->
    <p v-if="loading" class="text-gray-600">Loading user data...</p>

    <!-- Profile Summary -->
    <div
      v-if="!loading && !error"
      class="bg-white rounded-2xl shadow p-6 flex flex-col md:flex-row gap-6 items-start"
    >
      <img
        :src="user.pictureUrl || defaultAvatar"
        alt="Profile Picture"
        class="w-28 h-28 rounded-full object-cover border border-gray-300"
      />
      <div>
        <h2 class="text-xl font-semibold text-black mb-2">{{ user.name }}</h2>
        <p class="text-gray-700">📧 {{ user.email }}</p>
        <p class="text-gray-700">📱 {{ user.phone }}</p>
      </div>
    </div>

    <!-- Events Registered -->
    <div v-if="!loading && !error" class="mt-6">
      <h3 class="text-lg font-semibold text-black mb-4">Registered Events</h3>
      <div v-if="user.events.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="event in user.events"
          :key="event.id"
          class="bg-white p-4 rounded-xl shadow hover:shadow-md transition"
        >
          <router-link :to="{ name: 'MyEvent', params: { id: event.id } }" class="text-md font-semibold text-gray-900 mb-1">{{ event.event }}</router-link>
          <p class="text-sm text-gray-600 mb-2">
            From: {{ formatDate(event.start_date) }} <br />
            To: {{ formatDate(event.end_date) }}
          </p>
          <span
            :class="event.paid ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'"
            class="inline-block px-2 py-1 rounded-full text-xs font-semibold"
          >
            {{ event.paid ? 'Paid' : 'Not Paid' }}
          </span>

          <!-- Show "Pay Now" if not paid and event is upcoming -->
          <div v-if="!event.paid && isUpcoming(event.start_date)" class="mt-2">
                  <button
                    class="text-green-600 hover:underline text-sm"
                    @click="payEvent(event)"
                  >
                    Pay Now
                  </button>
          </div>
        </div>
      </div>
      <p v-else class="text-gray-500 italic">You haven’t registered for any events yet.</p>
    </div>
  </div>
    <PayEventModal
  :visible="showPaymentModal"
  :event="selectedEvent"
  @close="showPaymentModal = false"
  @paid="handlePaid"
/>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'
import { useAuthStore } from '@/stores/auth'
import PayEventModal from '@/components/specific/PayEventModal.vue'

const showPaymentModal = ref(false)
const selectedEvent = ref(null) // ← this was missing!


const auth = useAuthStore()
const auth_user = auth.user

const user = ref({
  name: '',
  email: '',
  phone: '',
  pictureUrl: '',
  events: []
})

const loading = ref(false)
const error = ref(null)
const defaultAvatar = 'https://via.placeholder.com/150?text=Avatar'
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

const fetchUser = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/users/${auth_user.id}`)
    const data = res.data

    // Add paid status defaulting to false if missing
    const eventsWithPaid = (data.events || []).map(event => ({
      ...event,
      paid: event.paid ?? false
    }))

    user.value = {
      name: `${data.user.firstname} ${data.user.lastname}`,
      email: data.user.email,
      phone: data.user.phone,
      pictureUrl: data.profile_picture?.profile_picture
        ? `${apiBaseUrl}/${data.profile_picture.profile_picture}`
        : defaultAvatar,
      events: eventsWithPaid
    }
  } catch (err) {
    error.value = 'Failed to load user details.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Returns true if the event start date is in the future (upcoming)
const isUpcoming = (startDate) => {
  if (!startDate) return false
  const now = new Date()
  const eventStart = new Date(startDate)
  return eventStart > now
}

// Construct a payment URL (customize to your app's payment page or route)
const payLink = (eventId) => {
  return `/payment?event_id=${eventId}` // Update as needed
}

const formatDate = (isoDate) => {
  if (!isoDate) return ''
  const date = new Date(isoDate)
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function payEvent(event) {
  selectedEvent.value = event
  showPaymentModal.value = true
}

function handlePaid(eventId) {
  showSuccess('Payment completed successfully.')
  fetchEvents()
}

onMounted(() => {
  fetchUser()
})
</script>

<style scoped>
/* Optional styling */
</style>
