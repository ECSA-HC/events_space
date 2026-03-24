<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
    <AdminBar title="View Event">
      <router-link :to="{ name: 'Events' }" class="text-sm text-blue-600 hover:underline">
        Events
      </router-link>
      <span class="mx-2 text-sm text-gray-500">/</span>
      <span class="text-sm text-gray-700">View</span>
    </AdminBar>

    <!-- Event Details -->
    <div class="px-4 pt-4">
      <h1 class="text-xl font-bold text-gray-800 mb-4">Event Details</h1>

      <div v-if="loading" class="bg-white shadow-lg rounded-2xl p-8 flex justify-center items-center">
        <DataLoadingSpinner />
      </div>

      <div v-else-if="error" class="bg-red-100 text-red-700 p-6 rounded-lg">
        Error loading event: {{ error }}
      </div>

      <div v-else class="bg-white shadow-lg rounded-2xl p-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <DetailItem label="Event Name" :value="event.event" />
          <DetailItem label="Country" :value="event.country" />
          <DetailItem label="Location" :value="event.location" />
          <DetailItem label="Organization" :value="event.org_unit" />
          <DetailItem label="Start Date" :value="formatDate(event.start_date)" />
          <DetailItem label="End Date" :value="formatDate(event.end_date)" />
          <DetailItem label="Theme" :value="event.theme" />
        </div>
        <div class="mt-6">
          <h2 class="text-sm text-gray-600 mb-1 font-bold uppercase tracking-wide">Description</h2>
          <p class="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">{{ event.description }}</p>
        </div>
      </div>
    </div>

    <!-- Tabs for Participants, Documents, Links -->
    <div class="px-4 pt-4 pb-10">
      <TabGroup>
        <TabList class="flex space-x-2 border-b">
          <Tab v-slot="{ selected }" as="template">
            <button :class="['py-2 px-4', selected ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600']">
              Participants
              <span v-if="participants.length" class="ml-1 text-xs bg-gray-200 text-gray-700 rounded-full px-2">{{ participants.length }}</span>
            </button>
          </Tab>
          <Tab v-slot="{ selected }" as="template">
            <button :class="['py-2 px-4', selected ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600']">
              Attendance
              <span v-if="attendance.length" class="ml-1 text-xs bg-green-100 text-green-700 rounded-full px-2">{{ attendance.length }}</span>
            </button>
          </Tab>
          <Tab v-slot="{ selected }" as="template">
            <button :class="['py-2 px-4', selected ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600']">Documents</button>
          </Tab>
          <Tab v-slot="{ selected }" as="template">
            <button :class="['py-2 px-4', selected ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600']">Links</button>
          </Tab>
        </TabList>

        <TabPanels class="pt-4">
          <!-- Participants -->
          <TabPanel>
            <div class="flex justify-end mb-3 space-x-2">
              <select
                @change="downloadParticipants($event.target.value)"
                class="bg-bondi-blue text-white px-4 pr-4 py-2 rounded-full hover:bg-bondi-blue-700"
              >
                <option disabled selected>Download List</option>
                <option value="all">All</option>
                <option value="true">Paid</option>
                <option value="false">Not Paid</option>
              </select>

              <select
                @change="downloadBadgesAsPDF($event.target.value)"
                class="bg-bondi-blue text-white px-4 pr-4 py-2 rounded-full hover:bg-bondi-blue-700"
              >
                <option disabled selected>Download Badge List</option>
                <option value="all">All</option>
                <option value="true">Paid</option>
                <option value="false">Not Paid</option>
              </select>
            </div>

            <div class="bg-white shadow rounded-lg overflow-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">#</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Country</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Email</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Payment</th>
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="(p, idx) in participants" :key="p.id">
                    <td class="px-4 py-2 text-gray-500 text-xs">{{ idx + 1 }}</td>
                    <td class="px-4 py-2 font-medium">{{ p.firstname }} {{ p.lastname }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ p.country }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ p.email }}</td>
                    <td class="px-4 py-2">
                      <span v-if="p.paid" class="inline-block px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded-full font-semibold">✅ Paid</span>
                      <span v-else-if="p.payment_proof" class="inline-block px-2 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-full font-semibold">⏳ Proof Uploaded</span>
                      <span v-else class="inline-block px-2 py-0.5 text-xs bg-gray-100 text-gray-500 rounded-full">Not Paid</span>
                    </td>
                    <td class="px-4 py-2">
                      <div class="flex items-center space-x-2">
                        <button class="text-blue-500 hover:text-blue-700" @click="viewParticipant(p)" title="View details">
                          <EyeIcon class="w-5 h-5" />
                        </button>
                        <button
                          v-if="!p.paid && p.payment_proof"
                          class="text-green-600 hover:text-green-800 text-xs font-semibold px-2 py-1 bg-green-50 border border-green-300 rounded-lg"
                          @click="verifyPayment(p)"
                          title="Verify payment"
                        >
                          ✓ Verify
                        </button>
                        <button class="text-red-500 hover:text-red-700" @click="deregisterParticipant(p)" title="Deregister">
                          <TrashIcon class="w-5 h-5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </TabPanel>

          <!-- Attendance -->
          <TabPanel>
            <div class="flex justify-between items-center mb-3">
              <p class="text-sm text-gray-500">
                Showing <span class="font-semibold text-gray-700">{{ attendance.length }}</span> check-in record(s).
              </p>
              <button @click="loadAttendance" class="text-xs text-bondi-blue hover:underline">↻ Refresh</button>
            </div>

            <div v-if="loadingAttendance" class="flex justify-center py-8">
              <DataLoadingSpinner />
            </div>

            <div v-else class="bg-white shadow rounded-lg overflow-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">#</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Organisation</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Country</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Role</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Checked In</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Payment</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="attendance.length === 0">
                    <td colspan="7" class="text-center py-6 text-gray-400 italic text-sm">No attendance records yet.</td>
                  </tr>
                  <tr v-for="(a, idx) in attendance" :key="a.id" class="hover:bg-gray-50">
                    <td class="px-4 py-2 text-xs text-gray-400 font-mono">{{ idx + 1 }}</td>
                    <td class="px-4 py-2 font-medium text-sm">{{ a.firstname }} {{ a.lastname }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ a.organisation || '—' }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ a.country || '—' }}</td>
                    <td class="px-4 py-2 text-xs text-gray-500 capitalize">{{ a.participation_role }}</td>
                    <td class="px-4 py-2 text-sm text-gray-700">{{ formatDateTime(a.attendance_date) }}</td>
                    <td class="px-4 py-2">
                      <span v-if="a.paid" class="inline-block px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded-full">✅ Paid</span>
                      <span v-else class="inline-block px-2 py-0.5 text-xs bg-gray-100 text-gray-500 rounded-full">Unpaid</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </TabPanel>

          <!-- Documents -->
          <TabPanel>
            <div class="flex justify-end mb-3">
              <button
                @click="showUploadModal = true"
                class="bg-bondi-blue text-white px-4 py-2 rounded-full hover:bg-bondi-blue-700"
              >
                Upload Document
              </button>
            </div>
            <div class="bg-white shadow rounded-lg overflow-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Type</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">File</th>
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="d in documents" :key="d.id">
                    <td class="px-4 py-2">{{ d.name }}</td>
                    <td class="px-4 py-2">{{ d.document_type }}</td>
                    <td class="px-4 py-2">
                      <a :href="`${baseUrl}/${d.path}`" class="text-blue-600 hover:underline" target="_blank">{{ d.file_name }}</a>
                    </td>
                    <td class="px-4 py-2 flex space-x-2">
                      <button class="text-blue-500 hover:text-blue-700">
                        <EyeIcon class="w-5 h-5" />
                      </button>
                      <button
                        class="text-red-500 hover:text-red-700"
                        @click="deleteDocument(d)"
                      >
                        <TrashIcon class="w-5 h-5" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </TabPanel>

          <!-- Links -->
          <TabPanel>
            <div class="flex justify-end mb-3">
              <button
                @click="showAddLinkModal = true"
                class="bg-bondi-blue text-white px-4 py-2 rounded-full hover:bg-bondi-blue-700"
              >
                Add Link
              </button>
            </div>
            <div class="bg-white shadow rounded-lg overflow-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Link</th>
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="l in links" :key="l.id">
                    <td class="px-4 py-2">{{ l.name }}</td>
                    <td class="px-4 py-2">
                      <a :href="l.link" class="text-blue-600 hover:underline" target="_blank">{{ l.link }}</a>
                    </td>
                    <td class="px-4 py-2 flex space-x-2">
                      <button class="text-blue-500 hover:text-blue-700">
                        <EyeIcon class="w-5 h-5" />
                      </button>
                      <button
                        class="text-red-500 hover:text-red-700"
                        @click="deleteLink(l)"
                      >
                        <TrashIcon class="w-5 h-5" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </TabPanel>
        </TabPanels>
      </TabGroup>

      <!-- Participant Detail Modal -->
      <ParticipantBadgeModal
        v-if="selectedParticipant && showBadge"
        :visible="showBadge"
        :user="selectedParticipant"
        :event="event"
        @close="showBadge = false"
      />

      <!-- Payment Proof Modal -->
      <div
        v-if="showProofModal && proofParticipant"
        class="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
        @click.self="showProofModal = false"
      >
        <div class="bg-white rounded-2xl shadow-xl p-6 max-w-lg w-full mx-4">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-bold text-gray-800">Payment Proof</h3>
            <button @click="showProofModal = false" class="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
          </div>
          <p class="text-sm text-gray-600 mb-3">
            <span class="font-semibold">{{ proofParticipant.firstname }} {{ proofParticipant.lastname }}</span>
          </p>

          <!-- Image preview -->
          <div v-if="isImageProof(proofParticipant.payment_proof)" class="rounded-lg overflow-hidden border mb-4">
            <img
              :src="`${baseUrl}/${proofParticipant.payment_proof}`"
              alt="Payment proof"
              class="max-w-full max-h-80 object-contain mx-auto block"
            />
          </div>
          <!-- PDF / other file -->
          <div v-else class="mb-4">
            <a
              :href="`${baseUrl}/${proofParticipant.payment_proof}`"
              target="_blank"
              class="inline-flex items-center gap-2 text-indigo-600 hover:underline text-sm"
            >
              📄 View / Download Proof File
            </a>
          </div>

          <div class="flex gap-3 justify-end">
            <button @click="showProofModal = false" class="px-4 py-2 text-sm border rounded-lg text-gray-600 hover:bg-gray-50">
              Close
            </button>
            <button
              v-if="!proofParticipant.paid"
              @click="verifyPayment(proofParticipant); showProofModal = false"
              class="px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
            >
              ✓ Verify Payment
            </button>
          </div>
        </div>
      </div>

      <!-- Upload Document Modal -->
      <UploadDocumentModal
        v-if="showUploadModal"
        :eventId="eventId"
        @close="showUploadModal = false"
        @uploaded="refreshDocuments"
      />

      <!-- Add Link Modal -->
      <AddLinkModal
        v-if="showAddLinkModal"
        :eventId="eventId"
        @close="showAddLinkModal = false"
        @uploaded="refreshLinks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import { EyeIcon, TrashIcon } from '@heroicons/vue/24/outline'
import { useRoute } from 'vue-router'
import AdminBar from '@/components/common/AdminBar.vue'
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'
import api from '@/plugins/axios'
import ParticipantBadgeModal from '@/components/specific/ParticipantBadgeModal.vue'
import DetailItem from '@/components/specific/DetailItem.vue'
import UploadDocumentModal from '@/components/specific/UploadDocumentModal.vue'
import AddLinkModal from '@/components/specific/AddLinkModal.vue'

const baseUrl = import.meta.env.VITE_API_BASE_URL

const route = useRoute()
const eventId = Number(route.params.id)

const event = ref(null)
const participants = ref([])
const documents = ref([])
const links = ref([])
const attendance = ref([])
const loading = ref(true)
const loadingAttendance = ref(false)
const error = ref(null)

const selectedParticipant = ref(null)
const showBadge = ref(false)
const showUploadModal = ref(false)
const showAddLinkModal = ref(false)

// Payment proof modal
const showProofModal = ref(false)
const proofParticipant = ref(null)

function viewParticipant(participant) {
  if (participant.payment_proof) {
    // Show the proof modal with verify option
    proofParticipant.value = participant
    showProofModal.value = true
  } else {
    selectedParticipant.value = participant
    showBadge.value = true
  }
}

function isImageProof(path) {
  if (!path) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(path)
}

async function loadEventData() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/events/${eventId}`)
    event.value = res.data.event
    participants.value = res.data.participants
    documents.value = res.data.documents
    links.value = res.data.links
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load event'
  } finally {
    loading.value = false
  }
}

async function deregisterParticipant(p) {
  if (!confirm(`Deregister ${p.firstname} ${p.lastname} from this event? This cannot be undone.`)) return
  try {
    await api.delete(`/events/deregister_participant/${p.id}`)
    await loadEventData()
  } catch (err) {
    alert('Failed to deregister: ' + (err.response?.data?.detail || err.message))
  }
}

async function verifyPayment(p) {
  if (!confirm(`Verify payment for ${p.firstname} ${p.lastname}? This will grant them full access.`)) return
  try {
    await api.put(`/events/verify_payment/${p.id}`)
    alert(`Payment verified for ${p.firstname} ${p.lastname}.`)
    await loadEventData()
  } catch (err) {
    alert('Failed to verify payment: ' + (err.response?.data?.detail || err.message))
  }
}

async function downloadBadgesAsPDF(paidFilter) {
  if (!paidFilter) return

  try {
    const url = `/events/${eventId}/participants/badges?paid=${paidFilter}`
    const response = await api.get(url, { responseType: 'blob' })

    const contentDisposition = response.headers['content-disposition'] || ''
    let filename = 'participant_badges.pdf'
    const filenameMatch = contentDisposition.match(/filename\*?=.*['"]?([^;'"]+)/)
    if (filenameMatch && filenameMatch[1]) {
      filename = decodeURIComponent(filenameMatch[1])
    }

    const blob = new Blob([response.data], { type: 'application/pdf' })
    const link = document.createElement('a')
    const objectUrl = URL.createObjectURL(blob)

    link.href = objectUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(objectUrl)
  } catch (error) {
    console.error('Failed to download badges PDF:', error)
    alert('Failed to download participant badges PDF.')
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString()
}

function formatDateTime(dateStr) {
  return new Date(dateStr).toLocaleString(undefined, {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

async function loadAttendance() {
  loadingAttendance.value = true
  try {
    const res = await api.get(`/events/${eventId}/attendance`)
    attendance.value = res.data.data
  } catch (err) {
    console.error('Failed to load attendance:', err)
  } finally {
    loadingAttendance.value = false
  }
}

function refreshDocuments() {
  api.get(`/events/${eventId}`).then((res) => {
    documents.value = res.data.documents
  })
}

function refreshLinks() {
  api.get(`/events/${eventId}`).then((res) => {
    links.value = res.data.links
  })
}

async function deleteLink(link) {
  if (!confirm(`Are you sure you want to delete link "${link.name}"?`)) return
  try {
    await api.delete(`/events/delete_link/${link.id}`)
    refreshLinks()
  } catch (err) {
    alert('Failed to delete link: ' + (err.response?.data?.detail || err.message))
  }
}

async function deleteDocument(doc) {
  if (!confirm(`Are you sure you want to delete document "${doc.name}"?`)) return
  try {
    await api.delete(`/events/delete_document/${doc.id}`)
    refreshDocuments()
  } catch (err) {
    alert('Failed to delete document: ' + (err.response?.data?.detail || err.message))
  }
}

async function downloadParticipants(paidFilter) {
  const url = `/events/${eventId}/participants/download?paid=${paidFilter}`

  try {
    const response = await api.get(url, { responseType: 'blob' })
    const contentDisposition = response.headers['content-disposition']
    const match = contentDisposition?.match(/filename\*?=.*['"]?([^;'"]+)/)
    const filename = match ? decodeURIComponent(match[1]) : 'participants.xlsx'

    const blob = new Blob([response.data], { type: response.headers['content-type'] })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.click()
    URL.revokeObjectURL(link.href)
  } catch (error) {
    console.error('Download error:', error)
    alert('An error occurred while downloading participants.')
  }
}

onMounted(() => {
  loadEventData()
  loadAttendance()
})
</script>

<style scoped>
/* Add any custom styles here if needed */
</style>
