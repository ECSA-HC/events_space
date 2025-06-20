<template>
    <div class="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-2xl w-[28rem] relative space-y-4">
        <button @click="$emit('close')" class="absolute top-2 right-2 text-gray-500 hover:text-black text-xl font-bold">
          &times;
        </button>
  
        <h2 class="text-xl font-bold">Add Link</h2>
  
        <form @submit.prevent="submit">
          <input
            type="text"
            v-model="name"
            placeholder="Link Name"
            class="input mb-2 w-full"
            required
          />
          <input
            type="url"
            v-model="link"
            placeholder="URL"
            class="input mb-4 w-full"
            required
          />
  
          <button
            type="submit"
            class="bg-bondi-blue text-white px-4 py-2 rounded-full hover:bg-bondi-blue-700"
          >
            Add Link
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
  
  const name = ref('')
  const link = ref('')
  
  async function submit() {
    try {
      await api.post('/events/add_link/', {
        event_id: props.eventId,
        name: name.value,
        link: link.value,
      })
      emit('uploaded')
      emit('close')
    } catch (err) {
      alert('Failed to add link')
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
  