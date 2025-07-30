<template>
  <div class="space-y-8 flex-1">
    <h1 class="text-2xl font-semibold text-black">My Profile</h1>

    <!-- Profile Picture Upload -->
    <div class="bg-white rounded-2xl shadow p-6 flex flex-col md:flex-row items-center gap-6">
      <!-- Preview & Dropzone -->
      <div
        class="w-32 h-32 rounded-full border border-gray-300 overflow-hidden relative cursor-pointer
               flex items-center justify-center bg-gray-50 hover:bg-gray-100 transition"
        @click="triggerFileSelect"
        @dragover.prevent="dragActive = true"
        @dragleave.prevent="dragActive = false"
        @drop.prevent="handleDrop"
        :class="{ 'border-blue-500 bg-blue-50': dragActive }"
      >
        <img
          v-if="profilePicture"
          :src="profilePicture"
          alt="Profile Picture"
          class="w-full h-full object-cover"
        />
        <div v-else class="text-gray-400 text-center px-2 select-none">
          <svg
            class="mx-auto mb-1 w-8 h-8 text-gray-300"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12 5v14m7-7H5" />
          </svg>
          <span class="text-xs">Click or drag & drop to upload</span>
        </div>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="onFileChange"
        />
      </div>

      <div class="space-y-2 max-w-xs">
        <p class="text-sm text-gray-700">Add or update your profile picture</p>
        <button
          type="button"
          @click="triggerFileSelect"
          class="px-4 py-2 bg-bondi-blue text-white rounded-lg hover:bg-indigo-700 transition"
        >
          Select File
        </button>
      </div>
    </div>

    <!-- Bio Form -->
    <div class="bg-white rounded-2xl shadow p-6 space-y-6">
      <h2 class="text-lg font-semibold">Bio Data</h2>

      <!-- Success/Error Message -->
      <div v-if="successMessage" class="text-green-600 text-sm border border-green-300 rounded p-2 bg-green-50">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="text-red-600 text-sm border border-red-300 rounded p-2 bg-red-50">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="updateProfile" class="grid md:grid-cols-2 gap-4">
        <!-- Title -->
        <div>
          <label class="block text-sm font-medium mb-1">Title</label>
          <select v-model="title" class="w-full input">
            <option value="" disabled>Select title</option>
            <option value="Mr">Mr</option>
            <option value="Mrs">Mrs</option>
            <option value="Ms">Ms</option>
            <option value="Dr">Dr</option>
            <option value="Prof">Prof</option>
          </select>
        </div>

        <!-- Firstname -->
        <div>
          <label class="block text-sm font-medium mb-1">First Name</label>
          <input v-model="firstName" type="text" class="w-full input" required />
        </div>

        <!-- Middle Name -->
        <div>
          <label class="block text-sm font-medium mb-1">Middle Name</label>
          <input v-model="middleName" type="text" class="w-full input" />
        </div>

        <!-- Lastname -->
        <div>
          <label class="block text-sm font-medium mb-1">Last Name</label>
          <input v-model="lastName" type="text" class="w-full input" required />
        </div>

        <!-- Gender -->
        <div>
          <label class="block text-sm font-medium mb-1">Gender</label>
          <select v-model="gender" required class="w-full input">
            <option disabled value="">Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium mb-1">Email</label>
          <input v-model="email" type="email" class="w-full input" required />
        </div>

        <!-- Phone -->
        <div>
          <label class="block text-sm font-medium mb-1">Phone</label>
          <input v-model="phone" type="tel" class="w-full input" />
        </div>

        <!-- Profession -->
        <div>
          <label class="block text-sm font-medium mb-1">Profession</label>
          <input v-model="profession" type="text" class="w-full input" />
        </div>   

        <!-- Position -->
        <div>
          <label class="block text-sm font-medium mb-1">Position</label>
          <input v-model="position" type="text" class="w-full input" />
        </div>  

        <!-- Organisation -->
        <div>
          <label class="block text-sm font-medium mb-1">Organisation</label>
          <input v-model="organisation" type="text" class="w-full input" />
        </div>

        <!-- Country -->
        <div>
          <label class="block text-sm font-medium mb-1">Country</label>
          <select v-model="country" class="w-full input" required>
            <option value="" disabled>Select country</option>
            <option v-for="c in countries" :key="c.id" :value="c.id">{{ c.country }}</option>
          </select>
        </div>

        <!-- Submit Button -->
        <div class="col-span-full mt-4">
          <button
            type="submit"
            class="px-4 py-2 bg-bondi-blue text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Update Profile
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/plugins/axios'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const auth_user = auth.user

const countries = ref([])
const profilePicture = ref(null)
const profileFile = ref(null)
const dragActive = ref(false)
const fileInput = ref(null)
const defaultAvatar = 'https://via.placeholder.com/150?text=Avatar'

// Form data
const user_id = ref('')
const profile_id = ref('')
const title = ref('')
const firstName = ref('')
const middleName = ref('')
const lastName = ref('')
const email = ref('')
const phone = ref('')
const gender = ref('')
const country = ref('')
const organisation = ref('')
const position = ref('')
const profession = ref('')
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

// Messages
const successMessage = ref('')
const errorMessage = ref('')

// Trigger hidden input click
function triggerFileSelect() {
  fileInput.value?.click()
}

// Handle file selection
const onFileChange = (event) => {
  const file = event.target.files[0]
  processFile(file)
}

// Handle drag and drop file
function handleDrop(event) {
  dragActive.value = false
  const file = event.dataTransfer.files[0]
  processFile(file)
}

// Process file and show preview
function processFile(file) {
  if (!file) return
  profileFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => {
    profilePicture.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const fetchUser = async () => {
  try {
    const res = await api.get(`/users/${auth_user.id}`)
    const data = res.data

    title.value = data.profile?.title || ''
    firstName.value = data.user?.firstname || ''
    middleName.value = data.profile?.middle_name || ''
    lastName.value = data.user?.lastname || ''
    email.value = data.user?.email || ''
    phone.value = data.user?.phone || ''
    gender.value = data.profile?.gender || ''
    country.value = data.profile?.country_id || ''
    organisation.value = data.profile?.organisation || ''
    position.value = data.profile?.position || ''
    profession.value = data.profile?.profession || ''
    user_id.value = data.user?.id || ''
    profile_id.value = data.profile?.id || ''

    if (data.profile_picture) {
      profilePicture.value = `${apiBaseUrl}/${data.profile_picture.profile_picture}`
    }
  } catch (error) {
    errorMessage.value = 'Failed to load user details.'
    console.error(error)
  }
}

const fetchCountries = async () => {
  try {
    const res = await api.get('/countries')
    countries.value = res.data.data
  } catch (err) {
    console.error('Failed to load countries:', err)
  }
}

const updateProfile = async () => {
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const userPayload = {
      firstname: firstName.value,
      lastname: lastName.value,
      email: email.value,
      phone: phone.value,
    }

    const profilePayload = {
      title: title.value,
      middle_name: middleName.value,
      country_id: country.value,
      gender: gender.value,
      organisation: organisation.value,
      position: position.value,
      profession: profession.value,
    }

    await api.put(`/users/${user_id.value}`, userPayload)
    await api.put(`/users/profile/${profile_id.value}`, profilePayload)

    if (profileFile.value) {
      const formData = new FormData()
      formData.append('file', profileFile.value)

      await api.post('/users/upload_user_photo/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
    }

    successMessage.value = 'Profile updated successfully!'
    fetchUser()
  } catch (err) {
    console.error('Update error:', err)
    errorMessage.value = 'An error occurred while updating your profile.'
  }
}

onMounted(() => {
  fetchUser()
  fetchCountries()
})
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring focus:border-indigo-500;
}
</style>
