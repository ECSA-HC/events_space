<template>
  <div class="bg-gray-50 text-gray-800 font-sans">
    <!-- Banner/Header -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center">
      <div class="max-w-4xl mx-auto space-y-4">
        <div>
          <h1 class="text-4xl font-bold">{{ event?.event }}</h1>
          <p class="text-lg">
            {{ formatDate(event?.start_date) }} – {{ formatDate(event?.end_date) }}
            &middot; {{ event?.location }}
          </p>
        </div>

        <!-- Register Now Button -->
        <div>
          <router-link :to="{ name: 'Register', params: { id: event?.id } }"
            class="inline-block bg-white text-bondi-blue font-semibold px-6 py-3 rounded-full shadow hover:bg-gray-100 transition"
          >
            Register Now
          </router-link>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="max-w-5xl mx-auto px-4 py-10 space-y-12">
      <!-- Loading and Error -->
      <div v-if="loading" class="text-center">
        <DataLoadingSpinner />
      </div>
      <div v-else-if="error" class="text-center text-red-600">
        {{ error }}
      </div>
      <div v-else>
        <!-- Description -->
        <div>
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Event Description</h2>
          <p class="text-gray-700 leading-relaxed whitespace-pre-line">
            {{ event?.description }}
          </p>
        </div>

        <!-- Programme Files -->
        <div v-if="documents.length">
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Downloads</h2>
          <ul class="space-y-2">
            <li v-for="file in documents" :key="file.id">
              <a
                :href="`${baseUrl}/${file.path}`"
                target="_blank"
                class="inline-flex items-center gap-2 text-bondi-blue hover:underline"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                {{ file.name }}
              </a>
            </li>
          </ul>
        </div>

        <!-- Useful Links -->
        <div v-if="links.length">
          <h2 class="text-2xl font-semibold mb-4 text-bondi-blue">Useful Links</h2>
          <ul class="space-y-2">
            <li v-for="link in links" :key="link.id">
              <a :href="link.link" target="_blank" class="text-bondi-blue hover:underline">
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

const baseUrl = import.meta.env.VITE_API_BASE_URL
const route = useRoute()
const eventId = Number(route.params.id)

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



onMounted(() => {
  loadEventData()
})

function formatDate(dateStr) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}
</script>

<style scoped>
.text-bondi-blue {
  color: #0095b6;
}
.bg-bondi-blue {
  background-color: #0095b6;
}
</style>
