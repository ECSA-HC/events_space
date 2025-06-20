<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
    <AdminBar title="Edit Cluster">
      <router-link :to="{ name: 'Clusters' }" class="text-sm text-blue-600 hover:underline">Clusters</router-link>
      <span class="mx-2 text-sm text-gray-500">/</span>
      <span class="text-sm text-gray-700">Edit</span>
    </AdminBar>

    <!-- Page Title -->
    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Edit Cluster</h1>
    </div>

    <!-- Edit Cluster Form -->
    <main class="px-6 pb-6">
      <div class="w-full bg-white shadow rounded-lg p-6">
        <form @submit.prevent="updateCluster" class="space-y-4">
          <!-- Name Field -->
          <div class="mb-4 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              v-model="cluster.name"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            />
          </div>

          <!-- Type Field -->
          <div class="mb-4 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              v-model="cluster.type"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            >
              <option disabled value="">Select a type</option>
              <option value="secretariat">Secretariat</option>
              <option value="college">College</option>
              <option value="project">Project</option>
              <option value="programme">Programme</option>
              <option value="directorate">Directorate</option>
              <option value="department">Department</option>
            </select>
          </div>

          <!-- Description Field -->
          <div class="mb-6 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              v-model="cluster.description"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            ></textarea>
          </div>

          <!-- Buttons -->
          <div class="flex space-x-4 w-full md:w-1/2">
            <LoadingButton
              :loading="isSubmitting"
              :loadingLabel="'Updating...'"
              @click="updateCluster"
            >
              Update Cluster
            </LoadingButton>

            <router-link
              :to="{ name: 'Clusters' }"
              class="bg-gray-300 hover:bg-gray-400 text-gray-700 px-6 py-2 rounded-xl transition"
            >
              Cancel
            </router-link>
          </div>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminBar from '@/components/common/AdminBar.vue'
import LoadingButton from '@/components/common/LoadingButton.vue' // import your LoadingButton
import api from '@/plugins/axios'

const route = useRoute()
const router = useRouter()
const clusterId = route.params.id

const cluster = ref({
  name: '',
  type: '',
  description: ''
})

const isSubmitting = ref(false)

const fetchCluster = async () => {
  try {
    const response = await api.get(`/org_units/${clusterId}`)
    cluster.value = {
      ...response.data,
      type: response.data.type?.toLowerCase() || ''
    }
  } catch (error) {
    console.error('Error fetching cluster:', error.response?.data || error.message)
  }
}

const updateCluster = async () => {
  try {
    isSubmitting.value = true
    const payload = {
      ...cluster.value,
      type: cluster.value.type.toLowerCase()
    }
    await api.put(`/org_units/${clusterId}`, payload)
    router.push({ name: 'Clusters' })
  } catch (error) {
    console.error('Error updating cluster:', error.response?.data || error.message)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(fetchCluster)
</script>
