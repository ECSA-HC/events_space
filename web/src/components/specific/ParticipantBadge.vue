<template>
  <div class="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded-2xl shadow-2xl w-[28rem] relative text-center border-2 border-bondi-blue-500 space-y-4">

      <!-- Close button -->
      <button @click="$emit('close')" class="absolute top-2 right-2 text-gray-500 hover:text-black text-xl font-bold">
        &times;
      </button>

      <!-- Top row: Logo + ECSA-HC | QR Code -->
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-2">
          <img src="@/assets/ecsalogo.png" alt="Logo" class="w-16 h-16" />
          <span class="font-title font-black text-xl bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text">
            ECSA-HC
          </span>
        </div>
        <div>
          <img
            :src="`https://api.qrserver.com/v1/create-qr-code/?data=${participant.email}`"
            alt="QR Code"
            class="w-16 h-16"
          />
        </div>
      </div>

      <!-- Profile Picture -->
      <div>
        <img
          v-if="participant.photo?.length"
          :src="`${baseUrl}/${participant.photo[0].path}`"
          alt="Profile"
          class="w-32 h-32 object-cover rounded-full mx-auto border border-gray-300"
        />
        <div v-else class="w-24 h-24 bg-gray-100 rounded-full mx-auto flex items-center justify-center text-gray-400">
          No Photo
        </div>
      </div>

      <!-- Name -->
      <div>
        <h2 class="text-4xl font-bold bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text">
          {{ participant.firstname }}
        </h2>
        <p class="text-base text-gray-600 font-medium uppercase tracking-wide">{{ participant.lastname }}</p>
        <p class="text-base font-semibold mt-1 bg-gradient-to-r from-bondi-blue to-yellow-orange text-transparent bg-clip-text">
          {{ event?.event || 'Conference Title' }}
        </p>
      </div>

      <!-- Organisation + Country -->
      <div>
        <p class="text-lg font-bold text-gray-700">{{ participant.organisation }}</p>
        <p class="text-sm text-gray-600">{{ participant.country }}</p>
      </div>

      <!-- Contact Info -->
      <div>
        <h2 class="text-2xl font-bold text-gray-800">#:00{{ participant.id }}</h2>
      </div>

      <!-- Role Bar -->
      <div
        class="text-white font-bold text-xl py-4 mt-4"
        :class="getRoleColor(participant.participation_role)"
      >
        {{ participant.participation_role.toUpperCase() }}
      </div>

    </div>
  </div>
</template>

<script setup>
const baseUrl = import.meta.env.VITE_API_BASE_URL;

defineProps({
  participant: Object,
  event: Object
});

defineEmits(['close']);

const getRoleColor = (role) => {
  const colorMap = {
    secretariat: 'bg-bondi-blue',
    speaker: 'bg-green-600',
    participant: 'bg-gray-700',
    moderator: 'bg-purple-600',
  };
  return colorMap[role?.toLowerCase()] || 'bg-gray-500';
};
</script>
