<template>
  <div ref="pdfContent" class="p-6 hidden-for-print space-y-10">
    <div
      v-for="(group, index) in badgeGroups"
      :key="index"
      class="grid grid-cols-2 gap-6 page-break"
      style="height: 1000px;" 
    >
      <div
        v-for="participant in group"
        :key="participant.id"
        class="border border-gray-300 rounded-xl text-center flex flex-col items-center justify-center p-4"
        style="height: 450px; width: 100%;"
      >
      
        <img
          v-if="participant.photo?.length"
          :src="`${baseUrl}/${participant.photo[0].path}`"
          alt="Profile"
          class="w-24 h-24 object-cover rounded-full"
        />
        <div v-else class="w-24 h-24 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
          No Photo
        </div>


        <h2 class="text-lg font-bold mt-3">{{ participant.firstname }} {{ participant.lastname }}</h2>
        <p class="text-sm text-gray-600">{{ event?.event || 'Conference' }}</p>
        <p class="text-sm text-gray-600">{{ participant.organisation }}</p>
        <p class="text-xs text-gray-400">#:00{{ participant.id }}</p>


        <div class="mt-2 text-white font-bold py-1 px-2 rounded text-sm"
             :class="getRoleColor(participant.participation_role)">
          {{ participant.participation_role }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  participants: Array,
  event: Object,
});

const baseUrl = import.meta.env.VITE_API_BASE_URL;
const pdfContent = ref(null);

const getRoleColor = (role) => {
  const map = {
    secretariat: 'bg-bondi-blue',
    speaker: 'bg-green-600',
    participant: 'bg-gray-700',
    moderator: 'bg-purple-600',
  };
  return map[role?.toLowerCase()] || 'bg-gray-400';
};

// Groups of 4 per page
const badgeGroups = computed(() => {
  const size = 4;
  const result = [];
  for (let i = 0; i < props.participants.length; i += size) {
    result.push(props.participants.slice(i, i + size));
  }
  return result;
});

defineExpose({ pdfContent });
</script>

<style scoped>
.page-break {
  page-break-after: always;
}
.hidden-for-print {
  display: none;
}
</style>
