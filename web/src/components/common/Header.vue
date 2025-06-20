<template>
  <header class="bg-white text-gray-800 p-4 shadow font-roboto">
    <div class="mx-auto max-w-7xl flex flex-wrap md:flex-nowrap items-center justify-between gap-4">
      <!-- Logo + Title + Search -->
      <div class="flex items-center flex-wrap gap-4">
        <!-- Logo + Title -->
        <router-link :to="{ name: 'Home' }" class="flex items-center space-x-3">
          <img
            src="@/assets/ecsalogo.png"
            alt="ECSA Logo"
            class="h-16 w-16 object-contain"
          />
          <span class="font-title font-black text-xl bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text">
            Event Spaces
          </span>
        </router-link>

        <!-- Search Button -->
        <button
          @click="isSearchOpen = true"
          class="flex items-center gap-2 text-sm text-gray-600 hover:text-bondi-blue px-3 py-2 border border-gray-300 rounded-full transition"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
          Search events
        </button>
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
        <router-link :to="{ name: 'Login' }" class="bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition">
          Sign In
        </router-link>
      </nav>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="isMenuOpen" class="md:hidden mt-4 space-y-4 text-center transition-all">
      <router-link :to="{ name: 'Home' }" class="block hover:text-bondi-blue">Home</router-link>
      <router-link :to="{ name: 'Events' }" class="block hover:text-bondi-blue">All Events</router-link>
      <button
        class="bg-white text-bondi-blue font-semibold px-4 py-2 rounded-full border-2 border-bondi-blue hover:bg-bondi-blue/10 transition"
      >
        Sign In
      </button>
    </div>

    <!-- Search Modal -->
    <SearchModal v-if="isSearchOpen" @close="isSearchOpen = false" />
  </header>
</template>

<script setup>
import { ref } from 'vue'
import SearchModal from '@/components/specific/SearchModal.vue'

const isMenuOpen = ref(false)
const isSearchOpen = ref(false)
</script>
