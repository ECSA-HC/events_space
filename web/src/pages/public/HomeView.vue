<template>
  <section class="max-w-7xl px-4 py-6 space-y-12">
    <!-- Featured Event -->
    <div class="bg-white shadow-lg rounded-2xl p-6 sm:p-10 space-y-6 text-center">
      <h1 class="text-4xl sm:text-5xl font-black font-title bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text">
        African Digital Health Summit 2025
      </h1>

      <p class="text-lg sm:text-xl text-gray-700 font-medium">
        “Innovating Health Systems through Digital Transformation”
      </p>

      <div class="flex justify-center items-center gap-2 text-gray-600 text-sm sm:text-base">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-bondi-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <span>July 15–17, 2025</span>
      </div>

      <div class="flex justify-center items-center gap-2 text-gray-600 text-sm sm:text-base">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-orange" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M5 8a5 5 0 1110 0c0 3-5 9-5 9S5 11 5 8zm5-2a2 2 0 100 4 2 2 0 000-4z" clip-rule="evenodd" />
        </svg>
        <span class="text-bondi-blue font-medium">Arusha International Conference Centre, Tanzania</span>
      </div>

      <div class="text-sm text-gray-600">
        Organised by <span class="text-bondi-blue font-bold">ECSA-HC</span>
      </div>

      <button class="mt-4 bg-bondi-blue text-white px-6 py-3 rounded-full text-sm sm:text-base font-normal hover:bg-bondi-blue/90 transition">
        Register Now
      </button>
    </div>

    <!-- All Events -->
    <div>
      <h2 class="text-2xl sm:text-3xl font-bold text-gray-800 mb-6">All Upcoming Events</h2>

      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="event in paginatedEvents"
          :key="event.id"
          class="bg-white rounded-xl shadow p-5 space-y-4"
        >
          <h3 class="text-xl font-semibold text-gray-800">{{ event.title }}</h3>

          <div class="flex items-center gap-2 text-gray-600 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-bondi-blue" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ event.date }}</span>
          </div>

          <div class="flex items-center gap-2 text-gray-600 text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-yellow-orange" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 8a5 5 0 1110 0c0 3-5 9-5 9S5 11 5 8zm5-2a2 2 0 100 4 2 2 0 000-4z" clip-rule="evenodd" />
            </svg>
            <span>{{ event.location }}</span>
          </div>

          <div class="text-sm text-gray-600">
            Organised by <span class="text-bondi-blue font-bold">{{ event.organiser }}</span>
          </div>

          <button class="mt-2 bg-white border border-bondi-blue text-bondi-blue px-4 py-2 rounded-full text-sm font-normal hover:bg-bondi-blue/10 transition">
            View Details
          </button>
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

<script setup>
import { ref, computed } from 'vue'

const events = [
  {
    id: 1,
    title: 'Regional Health Innovation Fair',
    date: 'August 10, 2025',
    location: 'Nairobi, Kenya',
    organiser: 'ECSA-HC'
  },
  {
    id: 2,
    title: 'Digital Health Policy Workshop',
    date: 'September 5, 2025',
    location: 'Kigali, Rwanda',
    organiser: 'COSECSA'
  },
  {
    id: 3,
    title: 'Community eHealth Outreach',
    date: 'October 20, 2025',
    location: 'Lilongwe, Malawi',
    organiser: 'CANESCA'
  },
  {
    id: 4,
    title: 'mHealth Design Sprint',
    date: 'November 12, 2025',
    location: 'Lusaka, Zambia',
    organiser: 'ECSACOG'
  },
  {
    id: 5,
    title: 'Telemedicine Training Bootcamp',
    date: 'December 2, 2025',
    location: 'Dar es Salaam, Tanzania',
    organiser: 'ECSACOP'
  },
  {
    id: 6,
    title: 'eHealth Developers Hackathon',
    date: 'January 15, 2026',
    location: 'Addis Ababa, Ethiopia',
    organiser: 'ECSA-HC'
  },
  {
    id: 7,
    title: 'Health Tech Expo 2026',
    date: 'March 10, 2026',
    location: 'Gaborone, Botswana',
    organiser: 'COSECSA'
  },
]

const currentPage = ref(1)
const perPage = 3

const totalPages = computed(() => Math.ceil(events.length / perPage))

const paginatedEvents = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return events.slice(start, start + perPage)
})

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}
</script>

<style scoped>
.font-title {
  font-family: 'Roboto Black', sans-serif;
}
</style>
