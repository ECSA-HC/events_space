<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
    <AdminBar title="Edit Event">
      <a href="#" class="text-sm text-blue-600 hover:underline">Events</a>
      <span class="mx-2 text-sm text-gray-500">/</span>
      <span class="text-sm text-gray-700">Edit</span>
    </AdminBar>

    <!-- Page Title -->
    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Edit Event</h1>
    </div>

    <!-- Edit Event Form -->
    <main class="px-6 pb-6">
      <div class="w-full bg-white shadow rounded-lg p-6">
        <form @submit.prevent="submitEvent" class="space-y-4" novalidate>
          <!-- Event Name -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Event</label>
            <input
              v-model="newEvent.event"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            />
            <p v-if="submitted && !newEvent.event" class="text-sm text-red-500 mt-1">Event name is required.</p>
          </div>

          <!-- Theme -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Theme</label>
            <input
              v-model="newEvent.theme"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            />
          </div>

          <!-- Description -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              v-model="newEvent.description"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            ></textarea>
          </div>

          <!-- Start Date -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <input
              v-model="newEvent.start_date"
              type="date"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            />
          </div>

          <!-- End Date -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
            <input
              v-model="newEvent.end_date"
              type="date"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            />
          </div>

          <!-- Location -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <input
              v-model="newEvent.location"
              type="text"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            />
          </div>

          <!-- Org Unit -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Organizational Unit</label>
            <select
              v-model="newEvent.org_unit_id"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            >
              <option disabled value="0">Select Org Unit</option>
              <option v-for="unit in orgUnits" :key="unit.id" :value="unit.id">
                {{ unit.name }}
              </option>
            </select>
          </div>

          <!-- Country -->
          <div class="w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Country</label>
            <select
              v-model="newEvent.country_id"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-[#0095B6]"
            >
              <option disabled value="0">Select Country</option>
              <option v-for="country in countries" :key="country.id" :value="country.id">
                {{ country.country }}
              </option>
            </select>
          </div>

          <!-- Buttons -->
          <div class="flex space-x-4 w-full md:w-1/2">
            <LoadingButton
              :loading="isSubmitting"
              :loadingLabel="'Saving...'"
              @click="submitEvent"
            >
              Update Event
            </LoadingButton>

            <router-link
              :to="{ name: 'AdminEvents' }"
              class="bg-gray-300 hover:bg-gray-400 text-gray-700 px-6 py-2 rounded-xl transition"
            >
              Cancel
            </router-link>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios'
import AdminBar from '@/components/common/AdminBar.vue'
import LoadingButton from '@/components/common/LoadingButton.vue'

const route = useRoute()
const router = useRouter()
const eventId = route.params.id

// Form state
const newEvent = ref({
  event: '',
  theme: '',
  description: '',
  start_date: '',
  end_date: '',
  location: '',
  org_unit_id: 0,
  country_id: 0
})

const orgUnits = ref([])
const countries = ref([])
const isSubmitting = ref(false)
const submitted = ref(false)

// Fetch event details for editing
const fetchEvent = async () => {
  try {
    const response = await api.get(`/events/${eventId}`)
    const eventData = response.data.event
    eventData.start_date = eventData.start_date?.split('T')[0] || ''
    eventData.end_date = eventData.end_date?.split('T')[0] || ''
    newEvent.value = eventData
  } catch (err) {
    console.error('Failed to fetch event:', err)
  }
}

// Submit update
const submitEvent = async () => {
  submitted.value = true

  if (!newEvent.value.event || newEvent.value.org_unit_id === 0 || newEvent.value.country_id === 0) {
    return
  }

  try {
    isSubmitting.value = true
    await api.put(`/events/${eventId}`, newEvent.value)
    router.push({ name: 'AdminEvents' })
  } catch (error) {
    console.error('Failed to update event:', error.response?.data || error.message)
  } finally {
    isSubmitting.value = false
  }
}

// Fetch org units and countries
const fetchOrgUnits = async () => {
  try {
    const response = await api.get('/org_units/', { params: { skip: 0, limit: 100 } })
    orgUnits.value = response.data.data
  } catch (err) {
    console.error('Failed to fetch org units:', err)
  }
}

const fetchCountries = async () => {
  try {
    const response = await api.get('/countries/', { params: { skip: 0, limit: 100 } })
    countries.value = response.data.data
  } catch (err) {
    console.error('Failed to fetch countries:', err)
  }
}

onMounted(() => {
  fetchOrgUnits()
  fetchCountries()
  fetchEvent()
})
</script>
