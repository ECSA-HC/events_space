<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <Header />

    <!-- Main Content Section -->

      <main class="flex flex-1 p-4 sm:p-6 lg:p-8">
        <div class="flex flex-1 flex-col sm:space-y-0 space-y-8 sm:flex-row space-x-0 sm:space-x-8 max-w-7xl mx-auto w-full">
          <MyAccountSidebar />
          <router-view />
        </div>
      </main>


    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/common/Header.vue'
import Footer from '@/components/common/Footer.vue'
import MyAccountSidebar from '@/components/common/MyAccountSidebar.vue'
</script>