<template>
    <div class="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-2xl w-[28rem] relative space-y-4">
        <button @click="$emit('close')" class="absolute top-2 right-2 text-gray-500 hover:text-black text-xl font-bold">
          &times;
        </button>
  
        <h2 class="text-xl font-bold">Upload Document</h2>
  
        <form @submit.prevent="submit">
          <input
            type="text"
            v-model="file_name"
            placeholder="Document Name"
            class="input mb-2 w-full"
            required
          />
  
          <select v-model="doc_type" class="input mb-2 w-full" required>
            <option disabled value="">Select Document Type</option>
            <option value="ProgrammeBooklet">Programme Booklet</option>
            <option value="Presentation">Presentation</option>
            <option value="Photo">Photo</option>
            <option value="Advert">Advert</option>
            <option value="Guidelines">Guidelines</option>
            <option value="Other">Other</option>
          </select>
  
          <select v-model="access_level" class="input mb-4 w-full" required>
            <option disabled value="">Select Access Level</option>
            <option value="Public">Public</option>
            <option value="Private">Private</option>
          </select>
  
          <input type="file" @change="handleFile" required class="mb-4" />
  
          <button
            type="submit"
            :disabled="!file"
            class="bg-bondi-blue text-white px-4 py-2 rounded-full hover:bg-bondi-blue-700 disabled:opacity-50"
          >
            Upload
          </button>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '@/plugins/axios'
  
  const emit = defineEmits(['close', 'uploaded'])
  const props = defineProps({ eventId: Number })
  
  const file_name = ref('')
  const doc_type = ref('')
  const access_level = ref('')
  const file = ref(null)
  
  function handleFile(e) {
    file.value = e.target.files[0]
  }
  
  async function submit() {
    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('file_name', file_name.value)
    formData.append('doc_type', doc_type.value)
    formData.append('access_level', access_level.value)
    formData.append('event_id', props.eventId)
  
    try {
      await api.post('/events/upload_document/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      emit('uploaded')
      emit('close')
    } catch (err) {
      alert('Failed to upload document')
    }
  }
  </script>
  
  <style scoped>
  .input {
    border: 1px solid #ccc;
    padding: 0.5rem;
    border-radius: 0.375rem;
  }
  </style>
  