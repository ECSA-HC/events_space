<script setup>
import AdminBar from '@/components/common/AdminBar.vue'
</script>

<template>
  <div class="flex-1 flex flex-col">
    <!-- Reusable Admin Bar -->
    <AdminBar title="Dashboard">
      <a href="#" class="text-sm text-blue-600 hover:underline">Dashboard</a>
    </AdminBar>

    <!-- Page Title -->
    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Dashboard</h1>
    </div>

    <!-- Page Content -->
    <main class="p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white shadow rounded-lg p-4">
          <h2 class="text-lg font-semibold">Users</h2>
          <p class="mt-2 text-gray-600">1,204 registered</p>
        </div>
        <div class="bg-white shadow rounded-lg p-4">
          <h2 class="text-lg font-semibold">Revenue</h2>
          <p class="mt-2 text-gray-600">$15,320 this month</p>
        </div>
        <div class="bg-white shadow rounded-lg p-4">
          <h2 class="text-lg font-semibold">Performance</h2>
          <p class="mt-2 text-gray-600">85% uptime</p>
        </div>
      </div>
    </main>
  </div>
</template>
