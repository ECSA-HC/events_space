<template>
  <div class="space-y-8 flex-1">
    <!-- Page Title -->
    <h1 class="text-2xl font-semibold text-black">My Events</h1>

    <!-- Events Table -->
    <div class="bg-white rounded-2xl shadow p-6 space-y-6">
      <div class="text-sm text-gray-700">
        View all events below. Your registration and payment status will be clearly shown.
      </div>

      <!-- Success message -->
      <div
        v-if="successMessage"
        class="text-green-700 bg-green-50 border border-green-200 px-4 py-2 rounded-md text-sm"
      >
        {{ successMessage }}
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full text-sm text-left border border-gray-200 rounded-xl overflow-hidden">
          <thead class="bg-gray-50 text-gray-700 font-semibold">
            <tr>
              <th class="px-4 py-3 border-b">Event</th>
              <th class="px-4 py-3 border-b">Date</th>
              <th class="px-4 py-3 border-b">Location</th>
              <th class="px-4 py-3 border-b">Registration</th>
              <th class="px-4 py-3 border-b">Payment</th>
              <th class="px-4 py-3 border-b">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(event, index) in events"
              :key="index"
              class="hover:bg-gray-50 transition"
            >
              <td class="px-4 py-3 border-b font-medium text-gray-900">
                {{ event.name }}
              </td>
              <td class="px-4 py-3 border-b">{{ event.date }}</td>
              <td class="px-4 py-3 border-b">{{ event.location }}</td>
              <td class="px-4 py-3 border-b">
                <span
                  :class="[ 'px-2 py-1 rounded-full text-xs font-semibold',
                    event.registered
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-600'
                  ]"
                >
                  {{ event.registered ? 'Registered' : 'Not Registered' }}
                </span>
              </td>
              <td class="px-4 py-3 border-b">
                <span
                  :class="[ 'px-2 py-1 rounded-full text-xs font-semibold',
                    event.registered && event.paid
                      ? 'bg-green-100 text-green-700'
                      : event.registered
                      ? 'bg-yellow-100 text-yellow-700'
                      : 'bg-gray-100 text-gray-500'
                  ]"
                >
                  {{ event.registered ? (event.paid ? 'Paid' : 'Not Paid') : '-' }}
                </span>
              </td>
              <td class="px-4 py-3 border-b">
                <div class="flex flex-wrap gap-3 items-center">
                  <router-link :to="{ name: 'MyEvent', params: { id: event.id } }" class="text-indigo-600 hover:underline text-sm">
                    View
                  </router-link>
                  <button
                    v-if="event.registered && !event.paid"
                    class="text-red-600 hover:underline text-sm"
                    @click="deregisterEvent(event)"
                  >
                    Deregister
                  </button>
                  <button
                    v-if="!event.registered"
                    class="text-blue-600 hover:underline text-sm"
                    @click="openRegisterModal(event)"
                  >
                    Register
                  </button>
                  <button
                    v-if="event.registered && !event.paid"
                    class="text-green-600 hover:underline text-sm"
                    @click="payEvent(event)"
                  >
                    Pay
                  </button>
                  <button
                    v-if="event.registered && event.paid"
                    class="text-purple-600 hover:underline text-sm"
                    @click="viewBadge(event)"
                  >
                    View Badge
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="events.length === 0" class="text-center text-gray-500 py-6">
          No events found.
        </div>
      </div>
    </div>
  </div>

  <!-- Modal -->
<RegisterEventModal
  :visible="showRegisterModal"
  :event="selectedEvent"
  :user-id="auth_user.id"
  @close="showRegisterModal = false"
  @registered="handleRegistered"
/>
  <PayEventModal
  :visible="showPaymentModal"
  :event="selectedEvent"
  @close="showPaymentModal = false"
  @paid="handlePaid"
/>
<ParticipantBadgeModal
  :visible="showBadgeModal"
  :user-id="selectedUserId"
  :event-id="selectedEventId"
  @close="showBadgeModal = false"
/>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'
import { useAuthStore } from '@/stores/auth'
import RegisterEventModal from '@/components/specific/RegisterEventModal.vue'
import PayEventModal from '@/components/specific/PayEventModal.vue'
import ParticipantBadgeModal from '@/components/specific/ParticipantBadgeModal.vue'

const showBadgeModal = ref(false)
const selectedUserId = ref(null)
const selectedEventId = ref(null)

const showPaymentModal = ref(false)

const auth = useAuthStore()
const auth_user = auth.user

const events = ref([])
const loading = ref(false)
const error = ref(null)

const showRegisterModal = ref(false)
const selectedEvent = ref(null)
const successMessage = ref('')
let successTimeout = null

function showSuccess(message) {
  successMessage.value = message
  clearTimeout(successTimeout)
  successTimeout = setTimeout(() => {
    successMessage.value = ''
  }, 5000)
}

function formatDateRange(start, end) {
  const opts = { year: 'numeric', month: 'short', day: 'numeric' }
  const startDate = new Date(start).toLocaleDateString(undefined, opts)
  const endDate = new Date(end).toLocaleDateString(undefined, opts)
  return `${startDate} - ${endDate}`
}

const fetchEvents = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/events/with-registration/${auth_user.id}`)
    const apiData = res.data

    events.value = apiData.map((item) => ({
      id: item.event.id,
      name: item.event.title,
      location: `${item.event.location}, ${item.event.country}`,
      date: formatDateRange(item.event.start_date, item.event.end_date),
      registered: item.registered,
      paid: item.registration_details?.paid ?? false,
      registration_id: item.registration_details?.registration_id ?? null
    }))
  } catch (err) {
    error.value = 'Failed to load events.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openRegisterModal(event) {
  selectedEvent.value = event
  showRegisterModal.value = true
}

function handleRegistered({ registration_id, event_id }) {
  showRegisterModal.value = false
  showSuccess('Successfully registered for event.')
  fetchEvents()
}

function viewBadge(event) {
  selectedUserId.value = auth_user.id
  selectedEventId.value = event.id
  showBadgeModal.value = true
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

function payEvent(event) {
  selectedEvent.value = event
  showPaymentModal.value = true
}

function handlePaid(eventId) {
  showSuccess('Payment completed successfully.')
  fetchEvents()
}

onMounted(() => {
  fetchEvents()
})
</script>
