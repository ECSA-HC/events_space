<template>
  <transition name="modal-fade">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-blur-sm"
      aria-modal="true"
      role="dialog"
    >
      <div
        class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6 mx-4 animate-scale-in"
      >
        <!-- Icon -->
        <div class="flex justify-center mb-4">
          <div class="bg-red-100 text-red-600 p-3 rounded-full">
            <TrashIcon class="w-6 h-6" />
          </div>
        </div>

        <!-- Title -->
        <h2 class="text-xl font-semibold text-gray-800 text-center mb-2">
          Delete {{ itemName }}?
        </h2>

        <!-- Message -->
        <p class="text-center text-sm text-gray-600 mb-6">
          Are you sure you want to permanently delete
          <span class="font-medium text-gray-800">{{ itemName }}</span>?
          This action cannot be undone.
        </p>

        <!-- Actions -->
        <div class="flex justify-center space-x-3">
          <button
            @click="emit('cancel')"
            :disabled="loading"
            class="px-4 py-2 rounded-xl bg-gray-100 text-gray-700 hover:bg-gray-200 transition"
          >
            Cancel
          </button>
          <button
            @click="emit('confirm')"
            :disabled="loading"
            class="px-4 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700 transition flex items-center justify-center"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              ></path>
            </svg>
            <span>{{ loading ? 'Deleting...' : 'Yes, Delete' }}</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { TrashIcon } from "@heroicons/vue/24/outline";

defineProps({
  show: Boolean,
  itemName: {
    type: String,
    default: "this item",
  },
  loading: Boolean,
});

const emit = defineEmits(["confirm", "cancel"]);
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes scaleIn {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
.animate-scale-in {
  animation: scaleIn 0.3s ease-out;
}
</style>
