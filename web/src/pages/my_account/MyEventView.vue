<template>
  <div class="space-y-8 flex-1">
    <!-- Event Header -->
    <div class="bg-white p-6 rounded-2xl shadow flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-indigo-700">{{ event.event }}</h1>
        <p class="text-sm text-gray-500">{{ event.theme }}</p>
        <p class="text-sm text-gray-600 mt-1 italic">{{ event.description }}</p>
      </div>
      <div class="text-sm text-right text-gray-700">
        <p><strong>Location:</strong> {{ event.location }}, {{ event.country }}</p>
        <p><strong>Dates:</strong> {{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}</p>
        <p><strong>Organised by:</strong> {{ event.org_unit }}</p>
      </div>
    </div>

    <!-- Loading participation status -->
    <div v-if="loading" class="bg-white p-6 rounded-2xl shadow flex items-center justify-center gap-2 text-gray-400 text-sm">
      <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
      </svg>
      Loading your registration status…
    </div>

    <!-- Logged-in User Participation -->
    <div v-else-if="userParticipant" class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Your Participation</h2>
      <div class="flex items-start gap-4">
        <img
          :src="getPhotoUrl(userParticipant.photo)"
          alt="Profile"
          class="w-16 h-16 rounded-full object-cover border flex-shrink-0"
        />
        <div class="flex-1">
          <p class="font-semibold">{{ userParticipant.firstname }} {{ userParticipant.lastname }}</p>
          <p class="text-sm text-gray-600">{{ userParticipant.organisation }}</p>
          <p class="text-xs text-gray-500 italic">{{ userParticipant.country }} — {{ userParticipant.participation_role }}</p>
          <p class="text-xs text-gray-500">Registered: {{ formatDate(userParticipant.registered_at) }}</p>

          <!-- Payment Status -->
          <div class="mt-3 space-y-3">
            <!-- Paid -->
            <div v-if="userParticipant.paid" class="flex items-center gap-3 flex-wrap">
              <span class="inline-block px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full font-semibold">✅ Payment Verified</span>
              <button
                @click="downloadMyBadge"
                :disabled="downloadingBadge"
                class="inline-flex items-center gap-1 px-3 py-1 text-xs bg-indigo-600 text-white rounded-full hover:bg-indigo-700 font-semibold disabled:opacity-60"
              >
                🪪 {{ downloadingBadge ? 'Generating…' : 'Download My Badge' }}
              </button>
              <button
                v-if="userParticipant.payment_proof"
                @click="openMyProof"
                class="inline-flex items-center gap-1 px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 font-semibold"
              >
                🧾 View My Proof of Payment
              </button>
            </div>

            <!-- Not Paid -->
            <div v-else class="space-y-3">
              <!-- Proof upload status -->
              <div v-if="userParticipant.payment_proof" class="flex items-center gap-2 flex-wrap">
                <span class="inline-block px-3 py-1 text-xs bg-amber-100 text-amber-700 rounded-full font-semibold">
                  ⏳ Proof Uploaded — Awaiting Verification
                </span>
                <button
                  @click="openMyProof"
                  class="text-xs text-indigo-600 hover:underline font-medium"
                >
                  View
                </button>
                <label
                  class="cursor-pointer text-xs text-indigo-600 hover:underline"
                  title="Upload new proof"
                >
                  Replace
                  <input type="file" accept="image/*,.pdf" class="hidden" @change="uploadProof" ref="proofInput" />
                </label>
              </div>

              <div v-else class="flex items-center gap-2 flex-wrap">
                <span class="inline-block px-3 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                  💳 Payment Pending
                </span>
                <label class="cursor-pointer inline-flex items-center gap-1 px-3 py-1 text-xs bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 font-semibold">
                  📎 Upload Proof of Payment
                  <input type="file" accept="image/*,.pdf" class="hidden" @change="uploadProof" />
                </label>
              </div>

              <!-- Upload progress -->
              <p v-if="uploadingProof" class="text-xs text-gray-500 italic">Uploading...</p>

              <!-- Deregister -->
              <button
                @click="deregisterEvent"
                class="inline-flex items-center gap-1 px-3 py-1 text-xs bg-red-100 text-red-700 rounded-full hover:bg-red-200 font-semibold"
              >
                🚫 Deregister
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Not Registered Section -->
    <div v-else class="bg-white p-6 rounded-2xl shadow text-center">
      <h2 class="text-lg font-semibold text-gray-800 mb-2">You are not registered for this event</h2>
      <p class="text-sm text-gray-600 mb-4">Register now to participate in this event.</p>
      <button
        :disabled="showRegisterModal"
        @click="openRegisterModal(event)"
        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
      >
        📩 Register
      </button>
    </div>

    <!-- Documents -->
    <div class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Documents</h2>

      <!-- Loading -->
      <p v-if="loading" class="text-sm text-gray-400 italic">Loading…</p>

      <!-- ✅ Paid — show files -->
      <ul v-else-if="userParticipant?.paid && documents.length" class="space-y-2">
        <li v-for="doc in documents" :key="doc.id" class="flex items-center justify-between bg-gray-50 px-4 py-2 rounded">
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
        </li>
      </ul>

      <!-- ✅ Paid but no documents yet -->
      <p v-else-if="userParticipant?.paid && !documents.length" class="text-sm text-gray-400 italic">
        No documents have been uploaded yet.
      </p>

      <!-- 🔒 Registered but not paid -->
      <div v-else-if="userParticipant && !userParticipant.paid"
        class="flex items-start gap-4 rounded-xl p-4 bg-amber-50 border-2 border-amber-200">
        <div class="h-10 w-10 rounded-xl bg-amber-500 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-amber-800 text-sm">Payment Required</p>
          <p class="text-amber-700 text-sm mt-0.5">
            You are registered for this event but your payment has not been confirmed.
            Documents will be accessible once your payment is complete.
          </p>
        </div>
      </div>

      <!-- 🔒 Not registered -->
      <div v-else class="flex items-start gap-4 rounded-xl p-4 bg-gray-50 border-2 border-gray-200">
        <div class="h-10 w-10 rounded-xl bg-gray-400 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-gray-700 text-sm">Members Only</p>
          <p class="text-gray-500 text-sm mt-0.5">Register and complete payment to access event documents.</p>
        </div>
      </div>
    </div>

    <!-- Links -->
    <div class="bg-white p-6 rounded-2xl shadow">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">Useful Links</h2>

      <!-- Loading -->
      <p v-if="loading" class="text-sm text-gray-400 italic">Loading…</p>

      <!-- ✅ Paid — show links -->
      <ul v-else-if="userParticipant?.paid && links.length" class="list-disc pl-5 space-y-1">
        <li v-for="link in links" :key="link.id">
          <a :href="link.link" target="_blank" class="text-sm text-indigo-600 hover:underline">{{ link.name }}</a>
        </li>
      </ul>

      <!-- ✅ Paid but no links yet -->
      <p v-else-if="userParticipant?.paid && !links.length" class="text-sm text-gray-400 italic">
        No links have been added yet.
      </p>

      <!-- 🔒 Registered but not paid -->
      <div v-else-if="userParticipant && !userParticipant.paid"
        class="flex items-start gap-4 rounded-xl p-4 bg-amber-50 border-2 border-amber-200">
        <div class="h-10 w-10 rounded-xl bg-amber-500 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-amber-800 text-sm">Payment Required</p>
          <p class="text-amber-700 text-sm mt-0.5">
            Useful links will be accessible once your registration payment is confirmed.
          </p>
        </div>
      </div>

      <!-- 🔒 Not registered -->
      <div v-else class="flex items-start gap-4 rounded-xl p-4 bg-gray-50 border-2 border-gray-200">
        <div class="h-10 w-10 rounded-xl bg-gray-400 flex items-center justify-center flex-shrink-0 mt-0.5">
          <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <div>
          <p class="font-semibold text-gray-700 text-sm">Members Only</p>
          <p class="text-gray-500 text-sm mt-0.5">Register and complete payment to access event links.</p>
        </div>
      </div>
    </div>
  </div>

  <RegisterEventModal
    :visible="showRegisterModal"
    :event="selectedEvent"
    @close="showRegisterModal = false"
    @registered="handleRegistered"
  />

  <!-- Preview Modal -->
  <Teleport to="body">
    <div v-if="showPreviewModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showPreviewModal = false">
      <div class="absolute inset-0 bg-black/60" @click="showPreviewModal = false"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[85vh] flex flex-col overflow-hidden">
        <!-- Header -->
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
        <!-- Body -->
        <div class="flex-1 overflow-hidden bg-gray-100 flex items-center justify-center p-2">
          <!-- PDF -->
          <iframe
            v-if="previewingDoc && isPdf(previewingDoc.path)"
            :src="fileUrl(previewingDoc.path)"
            class="w-full h-full rounded border-0"
            style="min-height: 60vh;"
          ></iframe>
          <!-- PowerPoint / Office -->
          <iframe
            v-else-if="previewingDoc && isOffice(previewingDoc.path)"
            :src="officeViewerUrl(previewingDoc.path)"
            class="w-full h-full rounded border-0"
            style="min-height: 60vh;"
          ></iframe>
          <!-- Image -->
          <img
            v-else-if="previewingDoc && isImage(previewingDoc.path)"
            :src="fileUrl(previewingDoc.path)"
            class="max-w-full max-h-full object-contain rounded"
            alt="Preview"
          />
          <!-- Unsupported -->
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
import { ref, onMounted, computed } from 'vue'
import api from '@/plugins/axios'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import RegisterEventModal from '@/components/specific/RegisterEventModal.vue'
import { fileUrl, isImage, isPdf, isOffice, officeViewerUrl } from '@/utils/filePreview'

const showPreviewModal = ref(false)
const previewingDoc = ref(null)

const showRegisterModal = ref(false)
const selectedEvent = ref(null)
const uploadingProof = ref(false)
const downloadingBadge = ref(false)

const route = useRoute()
const router = useRouter()
const eventId = route.params.id
const auth = useAuthStore()
const event = ref({})
const participants = ref([])
const documents = ref([])
const links = ref([])
const errorMessage = ref('')
const loading = ref(true)

// Find logged-in user's participation (if any)
const userParticipant = computed(() => {
  return participants.value.find((p) => p.user_id === auth.user?.id)
})

// ─── Document preview helpers ────────────────────────────────────────────────
function canPreview(doc) {
  const name = doc.file_name || doc.path || ''
  return isPdf(name) || isOffice(name) || isImage(name)
}

function openPreview(doc) {
  previewingDoc.value = doc
  showPreviewModal.value = true
}

function openMyProof() {
  if (!userParticipant.value?.payment_proof) return
  openPreview({
    name: 'Proof of Payment',
    file_name: userParticipant.value.payment_proof.split('/').pop(),
    path: userParticipant.value.payment_proof,
  })
}

// Fetch data
const fetchEvent = async () => {
  loading.value = true
  try {
    const res = await api.get(`/events/${eventId}`)
    const data = res.data
    event.value = data.event
    participants.value = data.participants
    documents.value = data.documents
    links.value = data.links
  } catch (error) {
    errorMessage.value = 'Failed to load event details.'
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchEvent()
})

const formatDate = (dateStr) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateStr).toLocaleDateString(undefined, options)
}

const getPhotoUrl = (photo) => {
  if (typeof photo === 'string') {
    return `${import.meta.env.VITE_API_BASE_URL}/${photo}`
  } else if (photo?.length && photo[0].path) {
    return `${import.meta.env.VITE_API_BASE_URL}/${photo[0].path}`
  }
  return 'https://via.placeholder.com/150?text=Avatar'
}

// Actions
function openRegisterModal(ev) {
  selectedEvent.value = ev
  showRegisterModal.value = true
}

function handleRegistered() {
  showRegisterModal.value = false
  fetchEvent()
}

// Upload proof of payment
async function uploadProof(e) {
  const file = e.target.files?.[0]
  if (!file) return

  uploadingProof.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    await api.post(`/events/upload_payment_proof/${eventId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    alert('Proof of payment uploaded successfully! It will be verified by the admin.')
    await fetchEvent()
  } catch (err) {
    console.error(err)
    alert('Failed to upload proof: ' + (err.response?.data?.detail || err.message))
  } finally {
    uploadingProof.value = false
    e.target.value = ''
  }
}

// Download personal badge PDF
async function downloadMyBadge() {
  downloadingBadge.value = true
  try {
    const res = await api.get(`/events/${eventId}/my-badge`, { responseType: 'blob' })
    const blob = new Blob([res.data], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `badge_${event.value.event?.replace(/\s+/g, '_') || 'badge'}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    alert('Failed to download badge: ' + (err.response?.data?.detail || err.message))
  } finally {
    downloadingBadge.value = false
  }
}

// Deregister from event
async function deregisterEvent() {
  if (!confirm(`Are you sure you want to deregister from "${event.value.event}"? This cannot be undone.`)) return

  try {
    await api.delete(`/events/registration/${eventId}`)
    alert('Successfully deregistered from the event.')
    router.push({ name: 'MyEvents' })
  } catch (err) {
    console.error(err)
    alert('Failed to deregister: ' + (err.response?.data?.detail || err.message))
  }
}
</script>
