<template>
  <header class="bg-white text-gray-800 p-4 shadow font-roboto">
    <div class="mx-auto max-w-7xl flex flex-wrap md:flex-nowrap items-center justify-between gap-4">
      <!-- Logo + Title -->
      <div class="flex items-center gap-4">
        <router-link :to="{ name: 'Home' }" class="flex items-center space-x-3">
          <img src="@/assets/ecsalogo.png" alt="ECSA Logo" class="h-auto w-16 object-contain" />
          <span class="font-title font-black text-3xl text-bondi-blue bg-clip-text">
            ECSA-HC Event Spaces
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
        <router-link :to="{ name: 'Home' }" class="hover:text-bondi-blue">Home</router-link>
        <router-link :to="{ name: 'Events' }" class="hover:text-bondi-blue">All Events</router-link>

        <template v-if="auth.isAuthenticated">
          <router-link
            :to="{ name: 'MyDashboard' }"
            class="text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
          >
            {{ auth.user?.first_name || 'My Account' }}
          </router-link>
        </template>
        <template v-else>
          <router-link
            :to="{ name: 'Login' }"
            class="bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
          >
            Sign In
          </router-link>
        </template>
      </nav>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="isMenuOpen" class="md:hidden mt-4 space-y-4 text-center">
      <router-link :to="{ name: 'Home' }" class="block hover:text-bondi-blue">Home</router-link>
      <router-link :to="{ name: 'Events' }" class="block hover:text-bondi-blue">All Events</router-link>

      <template v-if="auth.isAuthenticated">
        <router-link
          :to="{ name: 'MyDashboard' }"
          class="inline-block text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
        >
          {{ auth.user?.first_name || 'My Account' }}
        </router-link>
      </template>
      <template v-else>
        <router-link
          :to="{ name: 'Login' }"
          class="inline-block bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
        >
          Sign In
        </router-link>
      </template>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const isMenuOpen = ref(false)
const auth = useAuthStore()

onMounted(() => {
  auth.loadFromStorage()
})
</script>
