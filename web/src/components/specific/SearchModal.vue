<!-- src/components/SearchModal.vue -->
<template>
    <div
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      @click.self="$emit('close')"
    >
      <div class="bg-white w-full max-w-md p-6 rounded-lg shadow">
        <h2 class="text-lg font-semibold mb-4">Search Events</h2>
        <input
          type="text"
          placeholder="Type to search..."
          class="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-bondi-blue"
        />
        <div class="mt-4 text-right">
          <button
            @click="$emit('close')"
            class="text-sm text-gray-600 hover:text-bondi-blue"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </template>
  