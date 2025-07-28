<template>
  <section class="max-w-7xl px-4 py-6 space-y-12">
    <!-- Featured Event -->
    <div
      v-if="featuredEvent"
      class="bg-white shadow-lg rounded-2xl p-6 sm:p-10 space-y-6 text-center"
    >
      <router-link :to="{ name: 'Event', params: { id: featuredEvent.id } }"
        class="text-3xl sm:text-4xl font-black font-title bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text"
      >
        {{ featuredEvent.event }}
      </router-link>

      <p class="text-lg sm:text-xl text-gray-700 font-medium">
        {{ featuredEvent.theme }}
      </p>

      <div class="flex justify-center items-center gap-2 text-gray-600 text-sm sm:text-base">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-bondi-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>{{ formatDate(featuredEvent.start_date) }} - {{ formatDate(featuredEvent.end_date) }}</span>
      </div>

      <div class="flex justify-center items-center gap-2 text-gray-600 text-sm sm:text-base">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-orange" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5 8a5 5 0 1110 0c0 3-5 9-5 9S5 11 5 8zm5-2a2 2 0 100 4 2 2 0 000-4z" clip-rule="evenodd" />
        </svg>
        <span class="text-bondi-blue font-medium">{{ featuredEvent.location }}</span>
      </div>

      <div class="text-sm text-gray-600">
        Organised by <span class="text-bondi-blue font-bold">{{ featuredEvent.org_unit.name }}</span>
      </div>
<div></div>
      <router-link :to="{ name: 'Register', params: { id: featuredEvent.id } }" class="mt-4 bg-bondi-blue text-white px-6 py-3 rounded-full text-sm sm:text-base font-normal hover:bg-bondi-blue/90 transition">
        Register Now
      </router-link>
    </div>

    <!-- All Events -->
    <div v-if="events.length > 0">
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-6">All Upcoming Events</h2>

      <DataLoadingSpinner v-if="isLoading" />

      <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="event in paginatedEvents"
          :key="event.id"
          class="bg-white rounded-xl shadow p-5 space-y-4"
        >
          <h3 class="text-xl font-semibold text-gray-800">{{ event.event }}</h3>

          <div class="flex items-center gap-2 text-gray-600 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-bondi-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ formatDate(event.start_date) }}</span>
          </div>

          <div class="flex items-center gap-2 text-gray-600 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-orange" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 8a5 5 0 1110 0c0 3-5 9-5 9S5 11 5 8zm5-2a2 2 0 100 4 2 2 0 000-4z" clip-rule="evenodd" />
            </svg>
            <span>{{ event.location }}</span>
          </div>

          <div class="text-sm text-gray-600">
            Organised by <span class="text-bondi-blue font-bold">{{ event.org_unit.name }}</span>
          </div>

          <router-link :to="{ name: 'Event', params: { id: event.id } }" class="mt-2 bg-white border border-bondi-blue text-bondi-blue px-4 py-2 rounded-full text-sm font-normal hover:bg-bondi-blue/10 transition">
            View Event Details
          </router-link>
        </div>
      </div>

      <!-- Pagination Controls -->
      <div class="mt-8 flex justify-center items-center space-x-2">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-xl border border-gray-300 text-gray-600 hover:bg-gray-100 disabled:opacity-50"
        >
          Prev
        </button>

        <button
          v-for="page in totalPages"
          :key="page"
          @click="goToPage(page)"
          :class="[ 'px-4 py-2 rounded-xl border', currentPage === page
            ? 'bg-bondi-blue text-white border-bondi-blue'
            : 'border-gray-300 text-gray-600 hover:bg-gray-100' ]"
        >
          {{ page }}
        </button>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 rounded-xl border border-gray-300 text-gray-600 hover:bg-gray-100 disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  </section>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '@/plugins/axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

export default {
  name: 'EventsView',
  components: { DataLoadingSpinner },
  setup() {
    const isLoading = ref(false)
    const events = ref([])
    const featuredEvent = ref(null)
    const currentPage = ref(1)
    const perPage = ref(6)

    const fetchEvents = async () => {
      isLoading.value = true
      try {
        const response = await api.get('/events/')
        const allEvents = response.data.data || []

        const sorted = allEvents.sort((a, b) => new Date(a.start_date) - new Date(b.start_date))
        featuredEvent.value = sorted[0] || null
        events.value = sorted.slice(1)
      } catch (error) {
        console.error('Error fetching events:', error.response?.data || error.message)
      } finally {
        isLoading.value = false
      }
    }

    const paginatedEvents = computed(() => {
      const start = (currentPage.value - 1) * perPage.value
      return events.value.slice(start, start + perPage.value)
    })

    const totalPages = computed(() => Math.ceil(events.value.length / perPage.value))

    const goToPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }

    const formatDate = (dateStr) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateStr).toLocaleDateString(undefined, options)
    }

    onMounted(fetchEvents)

    return {
      isLoading,
      featuredEvent,
      events,
      paginatedEvents,
      currentPage,
      perPage,
      totalPages,
      goToPage,
      formatDate,
    }
  },
}
</script>

<style scoped>
.font-title {
  font-family: 'Roboto Black', sans-serif;
}
</style>
