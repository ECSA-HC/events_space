<template>
  <div class="bg-gray-50 text-gray-800 font-sans min-h-screen">
    <!-- Banner/Header -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center">
      <div class="max-w-4xl mx-auto space-y-3">
        <h1 class="text-4xl font-bold tracking-tight">{{ event?.event }}</h1>
        <p class="text-lg tracking-normal">
          {{ formatDate(event?.start_date) }} – {{ formatDate(event?.end_date) }}
          &middot; {{ event?.location }}
        </p>

        <router-link
          v-if="isRegistrationOpen"
          :to="{ name: 'Register', params: { id: event?.id } }"
          class="inline-block bg-white text-bondi-blue font-semibold px-6 py-2 rounded-full shadow hover:shadow-md hover:bg-gray-100 transition"
        >
          Register Now
        </router-link>
        <button
          v-else
          @click="showClosedMessage"
          class="inline-block bg-gray-300 text-gray-500 font-semibold px-6 py-2 rounded-full shadow cursor-not-allowed"
        >
          Register Now
        </button>
      </div>
    </section>

    <!-- Main Content -->
    <section class="max-w-4xl mx-auto px-6 py-10 space-y-12">
      <div v-if="loading" class="text-center">
        <DataLoadingSpinner />
      </div>
      <div v-else-if="error" class="text-center text-red-600">
        {{ error }}
      </div>
      <div v-else class="space-y-8">
        <!-- Event Details -->
        <section class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-semibold text-bondi-blue mb-6">Event Details</h2>
          <dl class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-6 text-gray-700">
            <div>
              <dt class="font-medium mb-1">Theme</dt>
              <dd>{{ event?.theme || 'N/A' }}</dd>
            </div>

            <div>
              <dt class="font-medium mb-1">Organised By</dt>
              <dd>{{ event?.org_unit || 'N/A' }}</dd>
            </div>
          </dl>
        </section>

        <!-- Description -->
        <section class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Event Description</h2>
          <p class="text-gray-700 leading-relaxed whitespace-pre-line">
            {{ event?.description }}
          </p>
        </section>

        <!-- Programme Files -->
        <section class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Downloads</h2>
          <div v-if="isAuthenticated && documents.length">
            <ul class="space-y-3">
              <li
                v-for="file in documents"
                :key="file.id"
                class="flex items-center gap-3 text-bondi-blue hover:underline cursor-pointer"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <a :href="`${baseUrl}/${file.path}`" target="_blank" class="text-base font-medium">
                  {{ file.name }}
                </a>
              </li>
            </ul>
          </div>
          <div v-else-if="!isAuthenticated" class="text-sm text-gray-600 italic">
            Please
            <router-link to="/login" class="text-bondi-blue underline">log in</router-link>
            to view downloads.
          </div>
        </section>

        <!-- Useful Links -->
        <section class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Useful Links</h2>
          <div v-if="isAuthenticated && links.length">
            <ul class="space-y-3">
              <li v-for="link in links" :key="link.id">
                <a :href="link.link" target="_blank" class="text-bondi-blue text-base font-medium hover:underline">
                  {{ link.name }}
                </a>
              </li>
            </ul>
          </div>
          <div v-else-if="!isAuthenticated" class="text-sm text-gray-600 italic">
            Please
            <router-link to="/login" class="text-bondi-blue underline">log in</router-link>
            to view useful links.
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'
import { useAuthStore } from '@/stores/auth'

const baseUrl = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const eventId = Number(route.params.id)

const authStore = useAuthStore()
const isAuthenticated = computed(() => !!authStore.user)

const event = ref(null)
const documents = ref([])
const links = ref([])
const loading = ref(true)
const error = ref(null)

async function loadEventData() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/events/${eventId}`)
    event.value = res.data.event
    documents.value = res.data.documents || []
    links.value = res.data.links || []
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load event'
  } finally {
    loading.value = false
  }
}

const isRegistrationOpen = computed(() => {
  if (!event.value?.start_date) return false
  const today = new Date()
  const eventStart = new Date(event.value.start_date)
  const diffDays = (eventStart - today) / (1000 * 60 * 60 * 24)
  return diffDays >= 7
})

function showClosedMessage() {
  alert('Registration is closed. It’s less than 7 days to the event.')
}

function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

onMounted(() => {
  loadEventData()
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
