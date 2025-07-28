<template>
  <div class="space-y-8 flex-1">
    <!-- Event Header -->
    <div class="bg-white p-6 rounded-2xl shadow flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-indigo-700">{{ event.event }}</h1>
        <p class="text-sm text-gray-500">{{ event.theme }}</p>
        <p class="text-sm text-gray-600 mt-1 italic">{{ event.description }}</p>
      </div>
      <div class="text-sm text-right text-gray-700">
        <p><strong>Location:</strong> {{ event.location }}, {{ event.country }}</p>
        <p><strong>Dates:</strong> {{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}</p>
        <p><strong>Organised by:</strong> {{ event.org_unit }}</p>
      </div>
    </div>

    <!-- Logged-in User Participation -->
    <div v-if="userParticipant" class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Your Participation</h2>
      <div class="flex items-center gap-4">
        <img
          :src="getPhotoUrl(userParticipant.photo)"
          alt="Profile"
          class="w-16 h-16 rounded-full object-cover border"
        />
        <div>
          <p class="font-semibold">{{ userParticipant.firstname }} {{ userParticipant.lastname }}</p>
          <p class="text-sm text-gray-600">{{ userParticipant.organisation }}</p>
          <p class="text-xs text-gray-500 italic">{{ userParticipant.country }} — {{ userParticipant.participation_role }}</p>
          <p class="text-xs text-gray-500">Registered: {{ formatDate(userParticipant.registered_at) }}</p>

          <!-- Payment Status -->
          <div class="mt-2">
            <span
              v-if="userParticipant.paid"
              class="inline-block px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full"
            >✅ Paid</span>

            <button
              v-else
              @click="deregisterEvent(event)"
              class="inline-block px-3 py-1 text-xs bg-red-100 text-red-700 rounded-full hover:bg-red-200"
            >
              🔁 Deregister
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Registered Section -->
    <div v-else class="bg-white p-6 rounded-2xl shadow text-center">
      <h2 class="text-lg font-semibold text-gray-800 mb-2">You are not registered for this event</h2>
      <p class="text-sm text-gray-600 mb-4">Register now to participate in this event.</p>
<button
  :disabled="showRegisterModal"
  @click="openRegisterModal(event)"
  class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
>
  📩 Register
</button>

    </div>

    <!-- Documents -->
    <div v-if="documents.length" class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Documents</h2>
      <ul class="space-y-2">
        <li v-for="doc in documents" :key="doc.id" class="flex items-center justify-between bg-gray-50 px-4 py-2 rounded">
          <div>
            <p class="font-medium text-indigo-700">{{ doc.name }}</p>
            <p class="text-xs text-gray-500">{{ doc.file_name }}</p>
          </div>
          <a
            :href="fileUrl(doc.path)"
            target="_blank"
            class="text-sm text-indigo-600 hover:underline"
          >Download</a>
        </li>
      </ul>
    </div>

    <!-- Links -->
    <div v-if="links.length" class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Links</h2>
      <ul class="list-disc pl-5 space-y-1">
        <li v-for="link in links" :key="link.id">
          <a :href="link.link" target="_blank" class="text-sm text-indigo-600 hover:underline">{{ link.name }}</a>
        </li>
      </ul>
    </div>
  </div>
    <RegisterEventModal
    :visible="showRegisterModal"
    :event="selectedEvent"
    @close="showRegisterModal = false"
    @registered="handleRegistered"
  />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/plugins/axios'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import RegisterEventModal from '@/components/specific/RegisterEventModal.vue'

const showRegisterModal = ref(false)
const selectedEvent = ref(null)

const route = useRoute()
const eventId = route.params.id
const auth = useAuthStore()
const auth_user = auth.user

const event = ref({})
const participants = ref([])
const documents = ref([])
const links = ref([])

const errorMessage = ref('')

// Find logged-in user's participation (if any)
const userParticipant = computed(() => {
  return participants.value.find((p) => p.user_id === auth_user.id)
})

// Fetch data
const fetchEvent = async () => {
  try {
    const res = await api.get(`/events/${eventId}`)
    const data = res.data
    event.value = data.event
    participants.value = data.participants
    documents.value = data.documents
    links.value = data.links
  } catch (error) {
    errorMessage.value = 'Failed to load event details.'
    console.error(error)
  }
}

onMounted(() => {
  fetchEvent()
})

const formatDate = (dateStr) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

const getPhotoUrl = (photo) => {
  if (typeof photo === 'string') {
    return `${import.meta.env.VITE_API_BASE_URL}/${photo}`
  } else if (photo?.length && photo[0].path) {
    return `${import.meta.env.VITE_API_BASE_URL}/${photo[0].path}`
  }
  return 'https://via.placeholder.com/150?text=Avatar'
}


const fileUrl = (path) => `${import.meta.env.VITE_API_BASE_URL}/${path}`

// Actions
function openRegisterModal(event) {
  selectedEvent.value = event
  showRegisterModal.value = true
}

function handleRegistered({ registration_id, event_id }) {
  showRegisterModal.value = false
  showSuccess('Successfully registered for event.')
  fetchEvent() // <-- fix here
}
function showSuccess(message) {
  alert(message)
}

async function deregisterEvent(event) {
  if (!event.registration_id) return

  if (confirm(`Are you sure you want to deregister from ${event.name}?`)) {
    try {
      await api.delete(`events/registration/${event.id}`)
      showSuccess(`Successfully deregistered from ${event.name}`)
      fetchEvents()
    } catch (err) {
      console.error(err)
      alert(`Failed to deregister from ${event.name}`)
    }
  }
}

const deregister = async () => {
  alert('Deregister functionality goes here...')
  // await api.delete(`/events/${eventId}/deregister`)
}
</script>
