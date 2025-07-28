<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center justify-center"
  >
    <div class="bg-white rounded-xl shadow-xl p-6 w-full max-w-md">
      <h2 class="text-lg font-semibold mb-4">Register for {{ event?.name }}</h2>

      <label class="block mb-2 text-sm font-medium text-gray-700">Participation Role</label>
      <select
        v-model="participationRole"
        class="w-full p-2 border rounded-md focus:outline-none focus:ring"
      >
              <option disabled value="">Select category</option>
              <option value="secretariat">ECSA-HC secretariat</option>
              <option value="moh">Country delegate (from Ministry of Health)</option>
              <option value="member_state">Participant from ECSA Member States</option>
              <option value="other_africa">Participant from other African countries</option>
              <option value="world">Participant from the Rest of the World</option>
              <option value="student">Student</option>
              <option value="exibitor">Sponsor/Exhibitor</option>
      </select>

      <div class="mt-6 flex justify-end gap-3">
        <button @click="close" class="text-gray-500 hover:underline">Cancel</button>
        <button
          @click="register"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          :disabled="!participationRole || loading"
        >
          <span v-if="loading">Registering...</span>
          <span v-else>Register</span>
        </button>
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
  userId: Number
})

const emit = defineEmits(['close', 'registered'])

const participationRole = ref('')
const loading = ref(false)

function close() {
  participationRole.value = ''
  emit('close')
}

async function register() {
  if (!props.event || !props.userId) return

  loading.value = true
  try {
    const res = await api.post(`/events/registration/${props.userId}`, {
      event_id: props.event.id,
      participation_role: participationRole.value
    })

    emit('registered', {
      registration_id: res.data.id,
      event_id: props.event.id
    })
    close()
  } catch (err) {
    console.error('Registration failed:', err)
  } finally {
    loading.value = false
  }
}
</script>
