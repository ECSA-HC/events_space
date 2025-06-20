<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
    <AdminBar title="Add Cluster">
      <a href="#" class="text-sm text-blue-600 hover:underline">Clusters</a>
      <span class="mx-2 text-sm text-gray-500">/</span>
      <span class="text-sm text-gray-700">Add</span>
    </AdminBar>

    <!-- Page Title -->
    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Add Cluster</h1>
    </div>

    <!-- Add Cluster Form -->
    <main class="px-6 pb-6">
      <div class="w-full bg-white shadow rounded-lg p-6">
        <form @submit.prevent="submitCluster" class="space-y-4" novalidate>
          <!-- Name Field -->
          <div class="mb-4 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input
              v-model="newCluster.name"
              type="text"
              required
              autofocus
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            />
            <p v-if="submitted && !newCluster.name" class="text-sm text-red-500 mt-1">Name is required.</p>
          </div>

          <!-- Type Field -->
          <div class="mb-4 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
            <select
              v-model="newCluster.type"
              required
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            >
              <option disabled value="">Select a type</option>
              <option v-for="type in clusterTypes" :key="type" :value="type.toLowerCase()">
                {{ type }}
              </option>
            </select>
            <p v-if="submitted && !newCluster.type" class="text-sm text-red-500 mt-1">Type is required.</p>
          </div>

          <!-- Description Field -->
          <div class="mb-6 w-full md:w-1/2">
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              v-model="newCluster.description"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
            ></textarea>
          </div>
          <!-- Buttons -->
          <div class="flex space-x-4 w-full md:w-1/2">
            <LoadingButton
              :loading="isSubmitting"
              :loadingLabel="'Saving...'"
              @click="submitCluster"
            >
              Save Cluster
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminBar from '@/components/common/AdminBar.vue'
import LoadingButton from '@/components/common/LoadingButton.vue' // adjust the path as needed
import api from '@/plugins/axios'

const router = useRouter()
const newCluster = ref({
  name: '',
  type: '',
  description: ''
})

const clusterTypes = [
  'Secretariat',
  'College',
  'Project',
  'Programme',
  'Directorate',
  'Department'
]

const isSubmitting = ref(false)
const submitted = ref(false)

const submitCluster = async () => {
  submitted.value = true

  if (!newCluster.value.name || !newCluster.value.type) {
    return
  }

  try {
    isSubmitting.value = true
    const payload = { ...newCluster.value }

    await api.post('/org_units/', payload)
    router.push({ name: 'Clusters' })
  } catch (error) {
    console.error('Failed to create cluster:', error.response?.data || error.message)
  } finally {
    isSubmitting.value = false
  }
}
</script>
