<template>
  <header class="bg-white text-gray-800 p-4 shadow font-roboto">
    <div class="mx-auto max-w-7xl flex flex-wrap md:flex-nowrap items-center justify-between gap-4">
      <!-- Logo + Title -->
      <div class="flex items-center gap-4">
        <router-link :to="{ name: 'Home' }" class="flex items-center space-x-3">
          <img src="@/assets/ecsalogo.png" alt="ECSA Logo" class="h-auto w-16 object-contain" />
          <span class="font-title font-black text-3xl text-bondi-blue bg-clip-text">
            ECSA EVENTS
          </span>
        </router-link>
      </div>

      <!-- Mobile Menu Toggle -->
      <button
        class="md:hidden text-3xl"
        @click="isMenuOpen = !isMenuOpen"
        aria-label="Toggle navigation"
      >
        ☰
      </button>

      <!-- Desktop Navigation -->
      <nav class="hidden md:flex items-center space-x-6">
        <router-link
          :to="{ name: 'Home' }"
          class="pb-0.5 hover:text-bondi-blue transition-colors"
          exact-active-class="text-bondi-blue font-semibold border-b-2 border-bondi-blue"
        >Home</router-link>

        <router-link
          :to="{ name: 'Events' }"
          class="pb-0.5 hover:text-bondi-blue transition-colors"
          :class="isEventsActive ? 'text-bondi-blue font-semibold border-b-2 border-bondi-blue' : ''"
        >All Events</router-link>

        <router-link
          :to="{ name: 'Contact' }"
          class="pb-0.5 hover:text-bondi-blue transition-colors"
          active-class="text-bondi-blue font-semibold border-b-2 border-bondi-blue"
        >Contact Us</router-link>

        <template v-if="auth.isAuthenticated">
          <router-link
            :to="{ name: 'MyDashboard' }"
            class="font-semibold px-4 py-2 rounded-full border-2 transition"
            :class="isMyAccountActive
              ? 'bg-bondi-blue text-white border-bondi-blue'
              : 'text-bondi-blue border-bondi-blue hover:bg-bondi-blue/10'"
          >
            {{ auth.user?.first_name || 'My Account' }}
          </router-link>
        </template>
        <template v-else>
          <router-link
            :to="{ name: 'Login' }"
            class="bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
          >
            Event Portal
          </router-link>
        </template>
      </nav>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="isMenuOpen" class="md:hidden mt-4 space-y-4 text-center">
      <router-link
        :to="{ name: 'Home' }"
        class="block hover:text-bondi-blue transition-colors py-1"
        exact-active-class="text-bondi-blue font-semibold"
      >Home</router-link>

      <router-link
        :to="{ name: 'Events' }"
        class="block hover:text-bondi-blue transition-colors py-1"
        :class="isEventsActive ? 'text-bondi-blue font-semibold' : ''"
      >All Events</router-link>

      <router-link
        :to="{ name: 'Contact' }"
        class="block hover:text-bondi-blue transition-colors py-1"
        active-class="text-bondi-blue font-semibold"
      >Contact Us</router-link>

      <template v-if="auth.isAuthenticated">
        <router-link
          :to="{ name: 'MyDashboard' }"
          class="inline-block font-semibold px-4 py-2 rounded-full border-2 transition"
          :class="isMyAccountActive
            ? 'bg-bondi-blue text-white border-bondi-blue'
            : 'text-bondi-blue border-bondi-blue hover:bg-bondi-blue/10'"
        >
          {{ auth.user?.first_name || 'My Account' }}
        </router-link>
      </template>
      <template v-else>
        <router-link
          :to="{ name: 'Login' }"
          class="inline-block bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
        >
          Event Portal
        </router-link>
      </template>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const isMenuOpen = ref(false)
const auth = useAuthStore()
const route = useRoute()

// "All Events" stays active for the list AND any single event page
const isEventsActive = computed(() =>
  ['Events', 'Event'].includes(String(route.name))
)

// "My Account" button stays filled/active on any /my-account sub-page
const isMyAccountActive = computed(() =>
  String(route.path).startsWith('/my-account')
)

onMounted(() => {
  auth.loadFromStorage()
})
</script>
