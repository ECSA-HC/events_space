<!-- src/pages/errors/ForbiddenView.vue -->
<template>
    <div class="flex justify-center items-center min-h-screen bg-gray-100">
      <div class="text-center space-y-4">
        <h1 class="text-5xl font-bold text-red-600">403</h1>
        <p class="text-lg text-gray-700">Access Denied: You do not have permission.</p>
        <router-link
          to="/dashboard"
          class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-500"
        >
          Go Home
        </router-link>
      </div>
    </div>
  </template>
  