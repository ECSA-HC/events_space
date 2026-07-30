<template>
  <div class="space-y-8 flex-1">
    <!-- Title -->
    <h1 class="text-2xl text-black">
      Welcome back, <span class="font-semibold text-black">{{ user.name }}</span>!
    </h1>

    <!-- Error message -->
    <p v-if="error" class="text-red-600">{{ error }}</p>

    <!-- Loading -->
    <p v-if="loading" class="text-gray-600">Loading user data...</p>

    <!-- Profile Summary -->
    <div
      v-if="!loading && !error"
      class="bg-white rounded-2xl shadow p-6 flex flex-col md:flex-row gap-6 items-start"
    >
      <img
        :src="user.pictureUrl || defaultAvatar"
        alt="Profile Picture"
        class="w-28 h-28 rounded-full object-cover border border-gray-300"
        @error="$event.target.src = defaultAvatar"
      />
      <div>
        <h2 class="text-xl font-semibold text-black mb-2">{{ user.name }}</h2>
        <p class="text-gray-700">📧 {{ user.email }}</p>
        <p class="text-gray-700">📱 {{ user.phone }}</p>
      </div>
    </div>

    <!-- Conference Documents -->
    <div v-if="!loading && paidEvents.length > 0" class="bg-white rounded-2xl shadow p-6">
      <div class="flex items-center gap-3 mb-4">
        <div class="h-10 w-10 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-black">Conference Documents</h3>
          <p class="text-sm text-gray-500">Welcome to the conference! Please find the abstract book, programme timetable and other documents below.</p>
        </div>
      </div>

      <!-- Abstract Book -->
      <div v-for="ev in paidEvents" :key="'ab-'+ev.id" class="flex items-center justify-between bg-gray-50 px-4 py-3 rounded mb-3">
        <div>
          <p class="font-medium text-indigo-700">Abstract Book</p>
          <p class="text-xs text-gray-500">{{ ev.event }}</p>
        </div>
        <div class="flex items-center gap-3">
          <a :href="`${apiBaseUrl}/abstracts/export/pdf?event_id=${ev.id}`" target="_blank" class="text-sm text-indigo-600 hover:underline">Download</a>
        </div>
      </div>

      <!-- Programme Timetable -->
      <div class="flex items-center justify-between bg-gray-50 px-4 py-3 rounded mb-3">
        <div>
          <p class="font-medium text-indigo-700">Programme Timetable</p>
          <p class="text-xs text-gray-500">programme_16th.pdf</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="openProgrammePreview" class="text-sm text-indigo-600 hover:underline">Preview</button>
          <a :href="programmeUrl" target="_blank" class="text-sm text-indigo-600 hover:underline">Download</a>
        </div>
      </div>

      <div v-for="ev in paidEvents" :key="ev.id" class="mb-4 last:mb-0">
        <p class="text-sm font-semibold text-gray-700 mb-2">{{ ev.event }}</p>
        <div v-if="ev.documents && ev.documents.length" class="space-y-2">
          <div v-for="doc in ev.documents" :key="doc.id" class="flex items-center justify-between bg-gray-50 px-4 py-2 rounded">
            <div>
              <p class="font-medium text-indigo-700">{{ doc.name }}</p>
              <p class="text-xs text-gray-500">{{ doc.file_name }}</p>
            </div>
            <div class="flex items-center gap-3">
              <button
                v-if="canPreview(doc)"
                @click="openPreview(doc)"
                class="text-sm text-indigo-600 hover:underline"
              >Preview</button>
              <a :href="fileUrl(doc.path)" target="_blank" class="text-sm text-indigo-600 hover:underline">Download</a>
            </div>
          </div>
        </div>
        <p v-else class="text-sm text-gray-400 italic">No documents uploaded yet.</p>
      </div>
    </div>

    <!-- Events Registered -->
    <div v-if="!loading && !error" class="mt-6">
      <h3 class="text-lg font-semibold text-black mb-4">Registered Events</h3>
      <div v-if="user.events.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="event in user.events"
          :key="event.id"
          class="bg-white p-4 rounded-xl shadow hover:shadow-md transition"
        >
          <router-link :to="{ name: 'MyEvent', params: { id: event.id } }" class="text-md font-semibold text-gray-900 mb-1">{{ event.event }}</router-link>
          <p class="text-sm text-gray-600 mb-2">
            From: {{ formatDate(event.start_date) }} <br />
            To: {{ formatDate(event.end_date) }}
          </p>
          <span
            :class="event.paid ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'"
            class="inline-block px-2 py-1 rounded-full text-xs font-semibold"
          >
            {{ event.paid ? 'Paid' : 'Not Paid' }}
          </span>

          <!-- Actions for unpaid upcoming events -->
          <div v-if="!event.paid && isUpcoming(event.start_date)" class="mt-3 flex flex-col gap-2">
            <button
              @click="goToPaymentPage(event)"
              class="w-full text-sm font-semibold text-white rounded-lg py-1.5 px-3 transition hover:opacity-90"
              style="background-color:#0095B6;">
              Go to Payment Page
            </button>
            <button
              @click="uploadProof(event)"
              class="w-full text-sm font-semibold rounded-lg py-1.5 px-3 border-2 transition hover:bg-gray-50"
              style="color:#0095B6; border-color:#0095B6; background:#fff;">
              Upload Proof of Payment
            </button>
          </div>
        </div>
      </div>
      <p v-else class="text-gray-500 italic">You haven’t registered for any events yet.</p>
    </div>
  </div>

  <!-- Preview Modal -->
  <Teleport to="body">
    <div v-if="showPreviewModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showPreviewModal = false">
      <div class="absolute inset-0 bg-black/60" @click="showPreviewModal = false"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] flex flex-col overflow-hidden">
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div>
            <h3 class="font-semibold text-gray-800">{{ previewingDoc?.name }}</h3>
            <p class="text-xs text-gray-500">{{ previewingDoc?.file_name }}</p>
          </div>
          <button @click="showPreviewModal = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <div class="flex-1 overflow-hidden bg-gray-100 flex items-center justify-center p-2">
          <iframe
            v-if="previewingDoc && isPdf(previewingDoc.path)"
            :src="fileUrl(previewingDoc.path)"
            class="w-full h-full rounded border-0"
            style="min-height: 60vh;"
          ></iframe>
          <iframe
            v-else-if="previewingDoc && isOffice(previewingDoc.path)"
            :src="officeViewerUrl(previewingDoc.path)"
            class="w-full h-full rounded border-0"
            style="min-height: 60vh;"
          ></iframe>
          <img
            v-else-if="previewingDoc && isImage(previewingDoc.path)"
            :src="fileUrl(previewingDoc.path)"
            class="max-w-full max-h-full object-contain rounded"
            alt="Preview"
          />
          <div v-else class="text-center text-gray-500 py-12">
            <svg class="mx-auto h-12 w-12 mb-3 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            <p class="text-sm">Preview not available for this file type.</p>
            <a :href="fileUrl(previewingDoc.path)" target="_blank" class="mt-3 inline-block text-sm text-indigo-600 hover:underline">Download instead</a>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'
import { useAuthStore } from '@/stores/auth'
import defaultAvatarImg from '@/assets/default-avatar.svg'
import { fileUrl, isImage, isPdf, isOffice, officeViewerUrl } from '@/utils/filePreview'

const router = useRouter()
const auth = useAuthStore()

const user = ref({
  name: '',
  email: '',
  phone: '',
  pictureUrl: '',
  events: []
})

const loading = ref(false)
const error = ref(null)
const defaultAvatar = defaultAvatarImg
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL

// ─── Preview state ──────────────────────────────────────────────────────────
const showPreviewModal = ref(false)
const previewingDoc = ref(null)

function canPreview(doc) {
  const name = doc.file_name || doc.path || ''
  return isPdf(name) || isOffice(name) || isImage(name)
}

function openPreview(doc) {
  previewingDoc.value = doc
  showPreviewModal.value = true
}

// ─── Programme PDF ───────────────────────────────────────────────────────────
const programmeUrl = `${apiBaseUrl}/assets/programme_16th.pdf`

function openProgrammePreview() {
  previewingDoc.value = { name: 'Programme Timetable', file_name: 'programme_16th.pdf', path: 'assets/programme_16th.pdf' }
  showPreviewModal.value = true
}

// ─── Paid events with documents ─────────────────────────────────────────────
const paidEvents = computed(() => {
  return user.value.events.filter(e => e.paid)
})

const fetchUser = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/users/${auth.user?.id}`)
    const data = res.data

    // Add paid status defaulting to false if missing
    const eventsWithPaid = (data.events || []).map(event => ({
      ...event,
      paid: event.paid ?? false,
      documents: []
    }))

    user.value = {
      name: `${data.user.firstname} ${data.user.lastname}`,
      email: data.user.email,
      phone: data.user.phone,
      pictureUrl: data.profile_picture?.profile_picture
        ? `${apiBaseUrl}/${data.profile_picture.profile_picture}`
        : defaultAvatar,
      events: eventsWithPaid
    }

    // Fetch documents for paid events
    for (const event of user.value.events) {
      if (event.paid) {
        try {
          const evRes = await api.get(`/events/${event.id}`)
          event.documents = evRes.data.documents || []
        } catch (e) {
          console.error(`Failed to fetch documents for event ${event.id}`, e)
        }
      }
    }
  } catch (err) {
    error.value = 'Failed to load user details.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Returns true if the event start date is in the future (upcoming)
const isUpcoming = (startDate) => {
  if (!startDate) return false
  const now = new Date()
  const eventStart = new Date(startDate)
  return eventStart > now
}

const formatDate = (isoDate) => {
  if (!isoDate) return ''
  const date = new Date(isoDate)
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function goToPaymentPage(event) {
  router.push(`/payment/${event.id}/${event.registration_id}?action=pay`)
}

function uploadProof(event) {
  router.push(`/payment/${event.id}/${event.registration_id}`)
}

onMounted(() => {
  fetchUser()
})
</script>

<style scoped>
/* Optional styling */
</style>
