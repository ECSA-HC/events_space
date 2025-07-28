<template>
  <div class="flex flex-1 items-center justify-center bg-gray-100 min-h-screen">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-md p-8 space-y-6">
      <h2 class="text-2xl font-bold text-center text-bondi-blue">Create Your Account</h2>

      <!-- Error Alert -->
      <div
        v-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md text-sm text-center"
      >
        {{ error }}
      </div>

      <!-- Success Message -->
      <div
        v-if="success"
        class="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded-md text-sm text-center"
      >
        {{ success }}
      </div>

      <!-- Registration Form -->
      <form v-if="!success" @submit.prevent="register" class="space-y-4" novalidate>
        <!-- First Name -->
        <div>
          <label for="firstname" class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
          <input
            v-model="firstname"
            type="text"
            id="firstname"
            required
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Last Name -->
        <div>
          <label for="lastname" class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
          <input
            v-model="lastname"
            type="text"
            id="lastname"
            required
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email address</label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Phone -->
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Phone</label>
          <input
            v-model="phone"
            type="tel"
            id="phone"
            placeholder="+123456789"
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
            required
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition disabled:opacity-50"
        >
          {{ isSubmitting ? 'Registering...' : 'Register' }}
        </button>
      </form>

      <!-- Login Link -->
      <p class="text-center text-sm text-gray-600" v-if="!success">
        Already have an account?
        <router-link :to="{ name: 'Login'}" class="text-bondi-blue hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'

const router = useRouter()

const firstname = ref('')
const lastname = ref('')
const email = ref('')
const phone = ref('')
const error = ref('')
const success = ref('')
const isSubmitting = ref(false)

const register = async () => {
  error.value = ''
  success.value = ''
  if (isSubmitting.value) return

  isSubmitting.value = true

  try {
    await api.post('/auth/register', {
      firstname: firstname.value,
      lastname: lastname.value,
      email: email.value,
      phone: phone.value,
    })

  success.value = 'Your account has been successfully registered. Please check your email for your username and password.'
  } catch (err) {
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
