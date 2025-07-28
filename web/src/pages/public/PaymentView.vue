<template>
  <div class="bg-gray-50 text-gray-800 font-sans">
    <!-- Header -->
    <section class="bg-bondi-blue text-white py-12 px-6 text-center" v-if="event">
      <div class="max-w-4xl mx-auto space-y-4">
        <h1 class="text-3xl font-bold">Payment for {{ event.event }}</h1>
        <p class="text-lg">
          {{ formatDate(event.start_date) }} – {{ formatDate(event.end_date) }} · {{ event.location }}
        </p>
      </div>
    </section>

    <!-- Loading/Error -->
    <section v-if="loading" class="text-center py-10">
      <DataLoadingSpinner />
    </section>
    <section v-if="error" class="text-center py-10 text-red-600">
      {{ error }}
    </section>

    <!-- Payment Form -->
    <section v-if="event && registration" class="max-w-3xl mx-auto px-4 py-10 space-y-6">
      <div v-if="!registration.paid" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative text-center">
        Your registration was successful. Please make payment to complete your registration.
      </div>

      <div v-else class="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative text-center">
        Payment has already been completed. You can now <router-link to="/login" class="text-bondi-blue underline">log in</router-link>.
      </div>

      <div v-if="!registration.paid">
        <h2 class="text-2xl font-semibold text-bondi-blue text-center">Make Payment</h2>

        <div v-if="paymentError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          {{ paymentError }}
        </div>

        <form @submit.prevent="handlePayment" class="space-y-4">
          <!-- Method -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Method *</label>
            <select v-model="payment_method" required class="input-style">
              <option disabled value="">Select method</option>
              <option>Bank Transfer</option>
              <option>Mobile Money</option>
              <option>Credit Card</option>
              <option>Cash</option>
            </select>
          </div>

          <!-- Reference -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Payment Reference *</label>
            <input v-model="payment_reference" required class="input-style" placeholder="Transaction ID / Receipt No." />
          </div>

          <!-- Amount -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Amount (USD) *</label>
            <input v-model="payment_amount" type="number" required class="input-style" />
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full bg-bondi-blue text-white py-3 rounded-2xl font-semibold hover:bg-bondi-blue/90 transition"
          >
            <span v-if="isSubmitting">Processing...</span>
            <span v-else>Submit Payment</span>
          </button>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const eventId = Number(route.params.event_id)
const registrationId = Number(route.params.registration_id)

// Reactive state
const event = ref(null)
const registration = ref(null)
const loading = ref(true)
const error = ref(null)
const paymentError = ref(null)
const isSubmitting = ref(false)

const payment_method = ref('')
const payment_reference = ref('')
const payment_amount = ref(0)

// Format date nicely
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

// Load event & registration details
const loadData = async () => {
  loading.value = true
  try {
    const [eventRes, regRes] = await Promise.all([
      api.get(`/events/${eventId}`),
      api.get(`/events/registration/${registrationId}`)
    ])
    event.value = eventRes.data.event
    registration.value = regRes.data.registration
    payment_amount.value = registration.value.amount || 0
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.detail || 'Failed to load data'
  } finally {
    loading.value = false
  }
}

// Submit payment
const handlePayment = async () => {
  paymentError.value = null
  isSubmitting.value = true
  try {
    await api.post('/events/payment/', {
      registration_id: registrationId,
      event_id: eventId,
      payment_method: payment_method.value,
      payment_reference: payment_reference.value,
      payment_amount: payment_amount.value
    })
    router.push({ name: 'EventPaymentSuccess' }) // or route to dashboard
  } catch (err) {
    console.error(err)
    paymentError.value = err.response?.data?.detail || 'Payment failed. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.input-style {
  @apply w-full border border-gray-300 rounded-2xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-bondi-blue focus:border-transparent;
}
.text-bondi-blue {
  color: #0095b6;
}
.bg-bondi-blue {
  background-color: #0095b6;
}
</style>
