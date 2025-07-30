<template>
  <div class="flex flex-1 items-center justify-center bg-gray-100 px-4">
    <div class="w-full max-w-xl bg-white rounded-3xl shadow-md p-8 space-y-6">
      <h2 class="text-2xl font-bold text-center text-bondi-blue">Reset Your Password</h2>

      <!-- Error Alert -->
      <div
        v-if="error"
        class="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded-md text-sm text-center"
      >
        {{ error }}
      </div>

      <!-- Success Message -->
      <div
        v-if="successMessage"
        class="bg-green-100 border border-green-400 text-green-700 px-4 py-2 rounded-md text-sm text-center"
      >
        {{ successMessage }}
      </div>

      <form @submit.prevent="resetPassword" class="space-y-4" v-if="!successMessage">
        <!-- Password -->
        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 mb-1"
            >New Password</label
          >
          <input
            v-model="password"
            type="password"
            id="password"
            required
            placeholder="Enter new password"
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Repeat Password -->
        <div>
          <label
            for="repeatPassword"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Repeat New Password</label
          >
          <input
            v-model="repeatPassword"
            type="password"
            id="repeatPassword"
            required
            placeholder="Repeat new password"
            class="w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition"
          :disabled="loading"
        >
          Reset Password
        </button>
      </form>

      <!-- Register Link -->
      <p class="text-center text-sm text-gray-600" v-if="!successMessage">
        Don’t have an account?
        <router-link to="/register" class="text-bondi-blue hover:underline">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "@/plugins/axios";

const password = ref("");
const repeatPassword = ref("");
const error = ref("");
const successMessage = ref("");
const loading = ref(false);
const route = useRoute();

const resetToken = ref("");

onMounted(() => {
  resetToken.value = route.params.token || "";
});

const resetPassword = async () => {
  error.value = ''
  successMessage.value = ''

  if (!resetToken.value) {
    error.value = 'Reset token is missing from the URL.'
    return
  }

  if (password.value !== repeatPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters long.'
    return
  }

  loading.value = true

  try {
    await api.post('/auth/reset_password', {
      password: password.value,
      rest_token: resetToken.value,
    })
    successMessage.value = 'Your password has been reset successfully!'
  } catch (err) {
    if (err.response?.status === 400) {
      error.value = err.response.data.detail || 'Invalid or expired token.'
    } else {
      error.value = 'Something went wrong. Please try again later.'
    }
  } finally {
    loading.value = false
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
