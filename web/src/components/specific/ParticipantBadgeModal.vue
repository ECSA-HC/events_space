<template>
  <div v-if="visible" class="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center justify-center">
    <div class="bg-white rounded-xl shadow-xl p-4 w-full max-w-sm relative">
      <button class="absolute top-2 right-3 text-gray-400 hover:text-black" @click="close">✕</button>

      <!-- Badge Content -->
      <div class="p-3 border border-dashed border-gray-300 text-center flex flex-col items-center">
        <!-- Logos -->
        <div class="w-full flex justify-between items-center mb-4">
          <img src="@/assets/ecsalogo.png" alt="Left Logo" class="h-14 w-auto" />
          <img src="@/assets/mauritius.png" alt="Right Logo" class="h-14 w-auto" />
        </div>

        <!-- Profile Picture -->
        <img
          :src="profilePicture"
          alt="Profile Picture"
          class="h-28 w-28 rounded-full border border-gray-300 object-cover mb-3"
        />

        <!-- Full Name -->
        <h2 class="text-xl font-semibold text-gray-800">{{ fullName }}</h2>

        <!-- Role + Org -->
        <p class="text-sm font-medium text-gray-700">{{ user.participation_role?.toUpperCase() }}</p>
        <p class="text-sm font-medium text-gray-700">{{ user.organisation }}</p>

        <!-- Country -->
        <p class="text-sm text-gray-500">{{ user.country }}</p>

        <!-- Badge ID -->
        <p class="text-xs text-gray-500 mt-1">Participant ID: BPF-{{ user.id }}</p>

        <!-- Event -->
        <div class="mt-3 text-sm text-gray-600 text-center space-y-1">
          <p class="font-semibold uppercase text-indigo-700">{{ event.event }}</p>
          <p>{{ event.country }} – {{ event.location }}</p>
          <p class="italic text-gray-500">Theme: {{ event.theme }}</p>
        </div>

        <!-- QR Code -->
        <div class="mt-4">
          <img :src="qrCodeUrl" alt="QR Code" class="w-20 h-20" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: Boolean,
  user: Object,
  event: Object,
})

const emit = defineEmits(['close'])
const close = () => emit('close')

const fullName = computed(() =>
  [props.user?.firstname, props.user?.lastname].filter(Boolean).join(' ')
)

const profilePicture = computed(() => {
  const pic = props.user?.photo?.[0]?.path
  return pic ? `${import.meta.env.VITE_API_BASE_URL}/${pic}` : 'https://via.placeholder.com/150?text=Avatar'
})

const qrCodeUrl = computed(() =>
  `https://api.qrserver.com/v1/create-qr-code/?data=U-${props.user?.id}&size=100x100`
)
</script>
