<template>
  <div class="flex flex-1 items-center justify-center bg-gray-100">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-md p-8 space-y-6">
      <h2 class="text-2xl font-bold text-center text-bondi-blue">Sign In to Your Account</h2>

      <form @submit.prevent="login" class="space-y-4">
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

        <!-- Password -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Forgot Password -->
        <div class="text-right">
          <router-link to="/forgot-password" class="text-sm text-bondi-blue hover:underline">
            Forgot password?
          </router-link>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition"
        >
          Login
        </button>
        <p v-if="error" class="text-red-600 text-sm text-center mt-2">{{ error }}</p>
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/plugins/axios'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')

const login = async () => {
  error.value = ''
  const form = new URLSearchParams()
  form.append('grant_type', 'password')
  form.append('username', email.value)
  form.append('password', password.value)
  form.append('client_id', 'string')
  form.append('client_secret', 'string')

  try {
    const { data } = await api.post('/auth/login', form)
    // Check if the response contains the expected data
    // Save auth info to store
    auth.setAuth({
      user: data.user,
      token: data.access_token,
      permissions: data.permissions,
    })

    // Redirect to home or dashboard
    router.push({ name: 'AdminDashboard' })
  } catch (err) {
    error.value = 'Invalid email or password.'
  }
}
</script>
