<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center justify-center"
  >
    <!-- Modal View -->
    <div class="bg-white rounded-xl shadow-xl p-4 w-full max-w-sm relative">
      <button class="absolute top-2 right-3 text-gray-400 hover:text-black" @click="close">✕</button>

      <!-- Visible Badge -->
      <div class="p-3 border border-dashed border-gray-300 text-center flex flex-col items-center">
        <!-- Logos -->
        <img src="@/assets/moh_sz.png" alt="Kingdom of Eswatini MoH" class="h-16 w-auto" /></div>