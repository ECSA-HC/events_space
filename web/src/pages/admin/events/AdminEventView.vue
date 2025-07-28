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
            <button :class="['py-2 px-4', selected ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600']">Participants</button>
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
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">#ID</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Country</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Phone</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Email</th>
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="p in participants" :key="p.id">
                    <td class="px-4 py-2">{{ p.id }}</td>
                    <td class="px-4 py-2">{{ p.firstname }} {{ p.lastname }}</td>
                    <td class="px-4 py-2">{{ p.country }}</td>
                    <td class="px-4 py-2">{{ p.phone }}</td>
                    <td class="px-4 py-2">{{ p.email }}</td>
                    <td class="px-4 py-2 flex space-x-2">
                      <button class="text-blue-500 hover:text-blue-700" @click="viewParticipant(p)">
                        <EyeIcon class="w-5 h-5" />
                      </button>
                      <button class="text-red-500 hover:text-red-700">
                        <TrashIcon class="w-5 h-5" />
                      </button>
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

<ParticipantBadgeModal
  v-if="selectedParticipant && showBadge"
  :visible="showBadge"
  :user="selectedParticipant"
  :event="event"
  @close="showBadge = false"
/>





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
const loading = ref(true)
const error = ref(null)

const selectedParticipant = ref(null)
const showBadge = ref(false)
const showUploadModal = ref(false)
const showAddLinkModal = ref(false)

function viewParticipant(participant) {
  selectedParticipant.value = participant
  showBadge.value = true
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

async function downloadBadgesAsPDF(paidFilter) {
  if (!paidFilter) return;

  try {
    const url = `/events/${eventId}/participants/badges?paid=${paidFilter}`;
    const response = await api.get(url, { responseType: 'blob' });

    const contentDisposition = response.headers['content-disposition'] || '';
    let filename = 'participant_badges.pdf';
    const filenameMatch = contentDisposition.match(/filename\*?=.*['"]?([^;'"]+)/);
    if (filenameMatch && filenameMatch[1]) {
      filename = decodeURIComponent(filenameMatch[1]);
    }

    const blob = new Blob([response.data], { type: 'application/pdf' });
    const link = document.createElement('a');
    const objectUrl = URL.createObjectURL(blob);

    link.href = objectUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();

    // Clean up
    document.body.removeChild(link);
    URL.revokeObjectURL(objectUrl);

  } catch (error) {
    console.error('Failed to download badges PDF:', error);
    alert('Failed to download participant badges PDF.');
  }
}


function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString()
}

function refreshDocuments() {
  api.get(`/events/${eventId}`)
    .then(res => {
      documents.value = res.data.documents
    })
}

function refreshLinks() {
  api.get(`/events/${eventId}`)
    .then(res => {
      links.value = res.data.links
    })
}

async function deleteLink(link) {
  if (!confirm(`Are you sure you want to delete link "${link.name}"?`)) return;
  try {
    await api.delete(`/events/delete_link/${link.id}`);
    refreshLinks();
  } catch (err) {
    alert('Failed to delete link: ' + (err.response?.data?.detail || err.message));
  }
}

async function deleteDocument(doc) {
  if (!confirm(`Are you sure you want to delete document "${doc.name}"?`)) return;
  try {
    await api.delete(`/events/delete_document/${doc.id}`);
    refreshDocuments();
  } catch (err) {
    alert('Failed to delete document: ' + (err.response?.data?.detail || err.message));
  }
}

async function downloadParticipants(paidFilter) {
  const url = `/events/${eventId}/participants/download?paid=${paidFilter}`

  try {
    const response = await api.get(url, {
      responseType: 'blob', // important for binary content like Excel
    });

    // Get filename from header
    const contentDisposition = response.headers['content-disposition'];
    const match = contentDisposition?.match(/filename\*?=.*['"]?([^;'"]+)/);
    const filename = match ? decodeURIComponent(match[1]) : 'participants.xlsx';

    // Create a temporary download link
    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error('Download error:', error);
    alert('An error occurred while downloading participants.');
  }
}


onMounted(() => {
  loadEventData()
})
</script>

<style scoped>
/* Add any custom styles here if needed */
</style>
