<template>
  <div class="flex w-full min-h-screen bg-white font-body">
    <Sidebar :minimized="sidebarMinimized" @toggle="toggleSidebar" />
    <main class="flex flex-1 bg-white">
      <router-view />
    </main>
  </div>
</template>

<script>
import Sidebar from '@/components/common/Sidebar.vue'

export default {
  components: { Sidebar },
  data() {
    return {
      sidebarMinimized: false,
    }
  },
  mounted() {
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    toggleSidebar() {
      this.sidebarMinimized = !this.sidebarMinimized
    },
    handleResize() {
      // Auto-collapse on screens < 768px (Tailwind md breakpoint)
      this.sidebarMinimized = window.innerWidth < 768
    }
  }
}
</script>

<style scoped>

</style>
