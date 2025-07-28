<template>
  <div class="flex flex-1 items-center justify-center bg-gray-100 min-h-screen px-4">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-md p-8 space-y-6">
      <h2 class="text-2xl font-bold text-center text-bondi-blue">Reset Your Password</h2>

      <!-- Error Alert -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md text-sm text-center">
        {{ error }}
      </div>

      <!-- Success Message -->
      <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded-md text-sm text-center">
        {{ successMessage }}
      </div>

      <form @submit.prevent="sendResetLink" class="space-y-4" v-if="!successMessage">
        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email address</label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            placeholder="you@example.com"
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition"
        >
          Send Password Reset Link
        </button>
      </form>

      <!-- Register Link -->
      <p class="text-center text-sm text-gray-600">
        Don’t have an account?
        <router-link to="/register" class="text-bondi-blue hover:underline">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/plugins/axios'

const email = ref('')
const error = ref('')
const successMessage = ref('')

const sendResetLink = async () => {
  error.value = ''
  successMessage.value = ''

  const payload = { email: email.value.trim() }

  try {
    await api.post('/auth/password-reset-link', payload)
    successMessage.value =
      'A password reset link has been sent to your email address. Please check your inbox to continue.'
  } catch (err) {
    if (err.response?.status === 404) {
      error.value = 'Email address not found. Please check and try again.'
    } else {
      error.value = 'Something went wrong. Please try again later.'
    }
  }
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
