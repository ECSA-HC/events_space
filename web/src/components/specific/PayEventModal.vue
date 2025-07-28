<template>
  <div v-if="visible" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
    <div class="bg-white rounded-xl shadow-lg w-full max-w-md p-6 relative">
      <!-- Close button -->
      <button @click="$emit('close')" class="absolute top-3 right-4 text-gray-500 hover:text-black">
        &times;
      </button>

      <h2 class="text-lg font-semibold mb-4">Pay for {{ event?.name }}</h2>

      <div class="space-y-4">
        <div class="text-gray-700 text-sm">
          Amount: <span class="font-medium text-black">USD {{ amount }}</span>
        </div>

        <!-- Simulated card form -->
        <div class="space-y-3">
          <input
            v-model="cardNumber"
            type="text"
            placeholder="Card Number"
            class="w-full px-3 py-2 border rounded-md text-sm"
          />
          <div class="flex gap-2">
            <input
              v-model="expiry"
              type="text"
              placeholder="MM/YY"
              class="w-1/2 px-3 py-2 border rounded-md text-sm"
            />
            <input
              v-model="cvv"
              type="text"
              placeholder="CVV"
              class="w-1/2 px-3 py-2 border rounded-md text-sm"
            />
          </div>
        </div>

        <div class="pt-4">
          <button
            @click="handlePayment"
            :disabled="loading"
            class="bg-green-600 hover:bg-green-700 text-white w-full py-2 rounded-md text-sm font-medium"
          >
            {{ loading ? 'Processing...' : 'Pay Now' }}
          </button>
        </div>

        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '@/plugins/axios'

const props = defineProps({
  visible: Boolean,
  event: Object,
})

const emit = defineEmits(['close', 'paid'])

const loading = ref(false)
const error = ref('')
const cardNumber = ref('')
const expiry = ref('')
const cvv = ref('')

const amount = 50.00 // Replace with actual dynamic value if needed

const handlePayment = async () => {
  if (!props.event?.registration_id) {
    error.value = 'Missing registration.'
    return
  }

  if (!cardNumber.value || !expiry.value || !cvv.value) {
    error.value = 'Fill in all card details.'
    return
  }

  try {
    loading.value = true
    error.value = ''

    // Simulate payment API
    await api.post(`/payments/pay-for-registration/${props.event.registration_id}`, {
      // Optional: Send card details (not secure unless via real payment gateway)
    })

    emit('paid', props.event.id)
    emit('close')
  } catch (err) {
    console.error(err)
    error.value = 'Payment failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
