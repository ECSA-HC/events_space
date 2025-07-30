<template>
  <div class="flex flex-1 items-center justify-center bg-gray-100">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-md p-8 space-y-6">
      <h2 class="text-2xl font-bold text-center text-bondi-blue">Sign In to Your Account</h2>

      <!-- Error Alert -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md text-sm text-center">
        {{ error }}
      </div>

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
          <router-link :to="{ name: 'PasswordResetLink'}" class="text-sm text-bondi-blue hover:underline">
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
      </form>

      <!-- Register Link -->
      <p class="text-center text-sm text-gray-600">
        Don’t have an account?
        <router-link :to="{ name: 'RegisterAccount'}" class="text-bondi-blue hover:underline">Register</router-link>
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

    auth.setAuth({
      user: data.user,
      token: data.access_token,
      permissions: data.permissions,
    })

    router.push({ name: 'MyDashboard' })
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Invalid email or password.'
    } else {
      error.value = 'Something went wrong. Please try again later.'
    }
  }
}
</script>
