<template>
    <div class="flex flex-col items-center space-y-2">
      <svg
        class="animate-spin h-10 w-10 text-blue-600"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
        ></path>
      </svg>
      <p class="text-gray-600 text-sm font-medium">Loading data...</p>
    </div>
  </template>
  
  <script setup>
  // No props or script needed for this simple spinner
  </script>
  
  <style scoped>
  /* Additional styles if needed */
  </style>
  