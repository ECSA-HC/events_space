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

            <!-- ── Visual Report ────────────────────────────────────────── -->
            <div v-if="!loading && participants.length" class="mb-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
              <!-- Total -->
              <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 flex flex-col gap-0.5">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Total</p>
                <p class="text-2xl font-bold text-gray-700">{{ participants.length }}</p>
              </div>
              <!-- Paid -->
              <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 flex flex-col gap-0.5">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Paid</p>
                <p class="text-2xl font-bold" style="color:#0095B6">{{ participants.filter(p => p.paid).length }}</p>
                <div class="w-full bg-gray-100 rounded-full h-1.5 mt-1">
                  <div class="h-1.5 rounded-full transition-all" style="background:#0095B6"
                    :style="{ width: (participants.filter(p=>p.paid).length / participants.length * 100) + '%' }"></div>
                </div>
              </div>
              <!-- Unpaid -->
              <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 flex flex-col gap-0.5">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Unpaid</p>
                <p class="text-2xl font-bold text-orange-500">{{ participants.filter(p => !p.paid).length }}</p>
                <div class="w-full bg-gray-100 rounded-full h-1.5 mt-1">
                  <div class="h-1.5 rounded-full bg-orange-400 transition-all"
                    :style="{ width: (participants.filter(p=>!p.paid).length / participants.length * 100) + '%' }"></div>
                </div>
              </div>
              <!-- Attendance -->
              <div class="bg-white rounded-2xl px-4 py-3 shadow-sm border border-gray-100 flex flex-col gap-0.5">
                <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Checked In</p>
                <p class="text-2xl font-bold text-green-600">{{ attendance.length }}</p>
                <p class="text-xs text-gray-400 mt-0.5">
                  {{ participants.length ? Math.round(attendance.length / participants.length * 100) : 0 }}% of total
                </p>
              </div>
            </div>

            <!-- Role breakdown -->
            <div v-if="!loading && participants.length" class="mb-4 bg-white rounded-2xl shadow-sm border border-gray-100 px-4 py-3">
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">By Role</p>
              <div class="flex flex-wrap gap-2">
                <span v-for="(count, role) in roleBreakdown" :key="role"
                  class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-50 border border-gray-200 text-gray-700 capitalize">
                  {{ role.replace('_', ' ') }}
                  <span class="ml-1 px-1.5 py-0.5 rounded-full text-white text-xs font-bold" style="background:#0095B6;">{{ count }}</span>
                </span>
              </div>
            </div>

            <!-- Search bar -->
            <div class="mb-3 relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
              <input v-model="participantSearch" type="text" placeholder="Search by name, email or country…"
                class="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
              <button v-if="participantSearch" @click="participantSearch = ''"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <div class="flex justify-end mb-3 gap-2 flex-wrap">
              <!-- Add Participant -->
              <button
                @click="openAddParticipantModal"
                class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold text-white transition hover:opacity-90"
                style="background-color:#0095B6;"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                </svg>
                Add Participant
              </button>

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

              <!-- Send Payment Reminders -->
              <button
                @click="sendPaymentReminders"
                :disabled="sendingReminders || unpaidParticipants.length === 0"
                class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-50"
                style="background-color:#F7941D;"
              >
                <svg v-if="!sendingReminders" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
                <span v-if="sendingReminders">Sending…</span>
                <span v-else-if="selectedUnpaid.length > 0">Send to Selected ({{ selectedUnpaid.length }})</span>
                <span v-else>Send to All Not Yet Reminded ({{ unpaidParticipants.length }})</span>
              </button>
            </div>

            <!-- Reminder feedback -->
            <div v-if="reminderMessage" class="mb-3 px-4 py-3 rounded-xl text-sm font-medium"
              :class="reminderError ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'">
              {{ reminderMessage }}
            </div>

            <!-- Stats bar -->
            <div class="mb-2 flex flex-wrap items-center gap-3 text-xs text-gray-500">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-green-50 text-green-700 rounded-full border border-green-200">
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                {{ participants.filter(p => p.paid).length }} Paid
              </span>
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-blue-50 text-blue-700 rounded-full border border-blue-200">
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                {{ participants.filter(p => !p.paid && p.reminder_sent_at).length }} Reminder Sent
              </span>
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-orange-50 text-orange-700 rounded-full border border-orange-200">
                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                {{ unpaidParticipants.length }} Not Yet Reminded
              </span>
            </div>

            <!-- Selection summary bar (only shown when there are pending reminders) -->
            <div v-if="unpaidParticipants.length > 0"
              class="mb-2 flex items-center gap-3 px-3 py-2 bg-orange-50 border border-orange-200 rounded-xl text-sm text-orange-800">
              <input type="checkbox" class="accent-orange-500 w-4 h-4 cursor-pointer"
                :checked="selectedUnpaid.length === unpaidParticipants.length && unpaidParticipants.length > 0"
                :indeterminate="selectedUnpaid.length > 0 && selectedUnpaid.length < unpaidParticipants.length"
                @change="toggleSelectAllUnpaid" />
              <span>
                <span v-if="selectedUnpaid.length === 0">
                  Select participants to send individually, or use <strong>"Send to All Not Yet Reminded"</strong>
                </span>
                <span v-else>
                  <strong>{{ selectedUnpaid.length }}</strong> of {{ unpaidParticipants.length }} selected
                  <button @click="selectedUnpaid = []" class="ml-2 underline text-orange-600 hover:text-orange-800">Clear</button>
                </span>
              </span>
            </div>
            <div v-else-if="participants.filter(p => !p.paid).length > 0"
              class="mb-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-xl text-sm text-blue-700">
              ✅ All unpaid participants have already received a payment reminder.
            </div>

            <div class="bg-white shadow rounded-lg overflow-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-3 py-2 w-8">
                      <input type="checkbox" class="accent-orange-500 w-4 h-4 cursor-pointer"
                        :checked="selectedUnpaid.length === unpaidParticipants.length && unpaidParticipants.length > 0"
                        @change="toggleSelectAllUnpaid"
                        title="Select all unpaid" />
                    </th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">#</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Name</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Country</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Email</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Payment</th>
                    <th class="px-4 py-2 text-left text-xs text-gray-500 uppercase">Reminder</th>
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="filteredParticipants.length === 0">
                    <td colspan="8" class="text-center py-6 text-gray-400 italic text-sm">
                      {{ participantSearch ? 'No participants match your search.' : 'No participants yet.' }}
                    </td>
                  </tr>
                  <tr v-for="(p, idx) in filteredParticipants" :key="p.id"
                    :class="selectedUnpaid.includes(p.id) ? 'bg-orange-50' : p.reminder_sent_at && !p.paid ? 'bg-blue-50/40' : ''">
                    <!-- Checkbox — only for unpaid AND not yet reminded -->
                    <td class="px-3 py-2">
                      <input v-if="!p.paid && !p.reminder_sent_at"
                        type="checkbox" class="accent-orange-500 w-4 h-4 cursor-pointer"
                        :checked="selectedUnpaid.includes(p.id)"
                        @change="toggleParticipant(p.id)" />
                    </td>
                    <td class="px-4 py-2 text-gray-500 text-xs">{{ idx + 1 }}</td>
                    <td class="px-4 py-2 font-medium">{{ p.firstname }} {{ p.lastname }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ p.country }}</td>
                    <td class="px-4 py-2 text-sm text-gray-600">{{ p.email }}</td>
                    <td class="px-4 py-2">
                      <span v-if="p.paid" class="inline-block px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded-full font-semibold">✅ Paid</span>
                      <span v-else-if="p.payment_proof" class="inline-block px-2 py-0.5 text-xs bg-amber-100 text-amber-700 rounded-full font-semibold">⏳ Proof Uploaded</span>
                      <span v-else class="inline-block px-2 py-0.5 text-xs bg-gray-100 text-gray-500 rounded-full">Not Paid</span>
                    </td>
                    <!-- Reminder sent badge -->
                    <td class="px-4 py-2">
                      <span v-if="p.reminder_sent_at"
                        class="inline-flex items-center gap-1 px-2 py-0.5 text-xs bg-blue-50 text-blue-700 rounded-full font-medium"
                        :title="`Reminder sent: ${formatDateTime(p.reminder_sent_at)}`">
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                        </svg>
                        {{ formatDateTime(p.reminder_sent_at) }}
                      </span>
                      <span v-else class="text-xs text-gray-300">—</span>
                    </td>
                    <td class="px-4 py-2">
                      <div class="flex items-center gap-1.5 flex-wrap">
                        <!-- Badge viewer -->
                        <button class="text-blue-500 hover:text-blue-700 p-1 rounded hover:bg-blue-50 transition"
                          @click="viewParticipant(p)" title="View badge">
                          <EyeIcon class="w-4 h-4" />
                        </button>
                        <!-- Payment proof document — only when uploaded -->
                        <button v-if="p.payment_proof"
                          class="p-1 rounded transition"
                          :class="p.paid ? 'text-green-600 hover:text-green-800 hover:bg-green-50' : 'text-amber-500 hover:text-amber-700 hover:bg-amber-50'"
                          @click="viewProof(p)"
                          :title="p.paid ? 'View payment proof (verified)' : 'View payment proof (pending verification)'">
                          <DocumentTextIcon class="w-4 h-4" />
                        </button>
                        <!-- Mark Paid (no proof required) -->
                        <button
                          v-if="!p.paid"
                          class="text-green-600 hover:text-green-800 text-xs font-semibold px-2 py-1 bg-green-50 border border-green-300 rounded-lg transition"
                          @click="verifyPayment(p)"
                          title="Mark as paid"
                        >
                          ✓ Mark Paid
                        </button>
                        <!-- Unmark Payment -->
                        <button
                          v-if="p.paid"
                          class="text-orange-500 hover:text-orange-700 text-xs font-semibold px-2 py-1 bg-orange-50 border border-orange-200 rounded-lg transition"
                          @click="unmarkPayment(p)"
                          title="Mark as unpaid"
                        >
                          ✕ Unmark
                        </button>
                        <!-- Deregister -->
                        <button class="text-red-400 hover:text-red-600 p-1 rounded hover:bg-red-50 transition"
                          @click="deregisterParticipant(p)" title="Deregister">
                          <TrashIcon class="w-4 h-4" />
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
            <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
              <p class="text-sm text-gray-500">
                Showing <span class="font-semibold text-gray-700">{{ attendance.length }}</span> check-in record(s).
              </p>
              <div class="flex gap-2 flex-wrap">
                <button @click="loadAttendance" class="text-xs text-bondi-blue hover:underline">↻ Refresh</button>
                <button
                  @click="exportAttendance"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold text-white transition hover:opacity-90"
                  style="background-color:#1B3F6E;"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                  </svg>
                  Export Excel
                </button>
                <button
                  @click="resetAllAttendance"
                  :disabled="attendance.length === 0"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold text-white transition hover:opacity-90 disabled:opacity-40"
                  style="background-color:#ef4444;"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                  </svg>
                  Reset All
                </button>
              </div>
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
                    <th class="px-4 py-2"></th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-if="attendance.length === 0">
                    <td colspan="8" class="text-center py-6 text-gray-400 italic text-sm">No attendance records yet.</td>
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
                    <td class="px-4 py-2">
                      <button
                        @click="resetSingleAttendance(a)"
                        class="text-red-400 hover:text-red-600 p-1 rounded hover:bg-red-50 transition"
                        title="Reset attendance"
                      >
                        <TrashIcon class="w-4 h-4" />
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
        class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
        @click.self="showProofModal = false"
      >
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl flex flex-col max-h-[92vh]">

          <!-- Header -->
          <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0"
                :style="{ backgroundColor: proofParticipant.paid ? '#dcfce7' : '#fef9c3' }">
                <DocumentTextIcon class="w-5 h-5" :class="proofParticipant.paid ? 'text-green-600' : 'text-amber-500'" />
              </div>
              <div>
                <p class="font-bold text-gray-800 text-sm">Payment Proof Document</p>
                <p class="text-xs text-gray-400">
                  {{ proofParticipant.firstname }} {{ proofParticipant.lastname }}
                  &middot; {{ proofParticipant.email }}
                </p>
              </div>
            </div>
            <button @click="showProofModal = false"
              class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Status bar -->
          <div class="px-5 py-2.5 flex items-center gap-2 text-xs border-b"
            :class="proofParticipant.paid ? 'bg-green-50 border-green-100' : 'bg-amber-50 border-amber-100'">
            <span v-if="proofParticipant.paid"
              class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-100 text-green-700 font-semibold">
              ✅ Payment Verified
            </span>
            <span v-else
              class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 font-semibold">
              ⏳ Awaiting Verification
            </span>
            <span class="text-gray-400">·</span>
            <span class="text-gray-500">{{ proofParticipant.country || 'N/A' }}</span>
            <span class="text-gray-400">·</span>
            <span class="text-gray-500 capitalize">{{ proofParticipant.participation_role?.name || proofParticipant.participation_role || '—' }}</span>
          </div>

          <!-- Document viewer -->
          <div class="flex-1 overflow-auto p-5 min-h-0">

            <!-- Image proof -->
            <div v-if="isImageProof(proofParticipant.payment_proof)"
              class="rounded-xl overflow-hidden border border-gray-200 bg-gray-50 flex items-center justify-center min-h-[300px]">
              <img
                :src="proofUrl(proofParticipant.payment_proof)"
                alt="Payment proof"
                class="max-w-full max-h-[60vh] object-contain"
              />
            </div>

            <!-- PDF proof — embedded viewer -->
            <div v-else-if="proofParticipant.payment_proof?.toLowerCase().endsWith('.pdf')"
              class="rounded-xl overflow-hidden border border-gray-200 bg-gray-50" style="height: 60vh;">
              <iframe
                :src="proofUrl(proofParticipant.payment_proof)"
                class="w-full h-full"
                frameborder="0"
              ></iframe>
            </div>

            <!-- Other file type — download link -->
            <div v-else
              class="rounded-xl border border-dashed border-gray-200 bg-gray-50 flex flex-col items-center justify-center py-12 gap-3">
              <DocumentTextIcon class="w-12 h-12 text-gray-300" />
              <p class="text-sm text-gray-500">Preview not available for this file type.</p>
              <a :href="proofUrl(proofParticipant.payment_proof)" target="_blank"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition hover:opacity-90"
                style="background-color:#0095B6;">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                Download File
              </a>
            </div>

          </div>

          <!-- Footer actions -->
          <div class="flex items-center justify-between px-5 py-4 border-t border-gray-100 flex-shrink-0 gap-3">
            <a :href="proofUrl(proofParticipant.payment_proof)" target="_blank"
              class="inline-flex items-center gap-1.5 text-sm text-bondi-blue hover:underline font-medium">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
              </svg>
              Open in new tab
            </a>
            <div class="flex gap-2">
              <button @click="showProofModal = false"
                class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 transition font-medium">
                Close
              </button>
              <button
                v-if="!proofParticipant.paid"
                @click="verifyPayment(proofParticipant); showProofModal = false"
                class="inline-flex items-center gap-2 px-5 py-2 text-sm bg-green-600 text-white rounded-xl hover:bg-green-700 font-semibold transition">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Verify Payment
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Add Participant Modal ────────────────────────────────────────── -->
      <div
        v-if="showAddParticipantModal"
        class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
        @click.self="closeAddParticipantModal"
      >
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg flex flex-col max-h-[92vh]">

          <!-- Header -->
          <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="h-9 w-9 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-[#0095B6]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                </svg>
              </div>
              <div>
                <p class="font-bold text-gray-800 text-sm">Add Participant</p>
                <p class="text-xs text-gray-400">Register a participant and optionally send an invitation</p>
              </div>
            </div>
            <button @click="closeAddParticipantModal"
              class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="p-5 space-y-4 overflow-y-auto flex-1">

            <!-- User picker -->
            <div class="relative">
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">
                Select Participant *
              </label>

              <!-- Trigger button -->
              <button type="button" @click="userPickerOpen = !userPickerOpen"
                class="w-full flex items-center gap-2 px-3 py-2.5 border rounded-xl text-sm text-left transition focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
                :class="selectedUser ? 'border-[#0095B6] bg-[#e6f7fb]' : 'border-gray-300 bg-white'">
                <template v-if="selectedUser">
                  <div class="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 uppercase"
                    style="background-color:#0095B6;">
                    {{ (selectedUser.firstname?.[0] || '') + (selectedUser.lastname?.[0] || '') }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <span class="font-medium text-gray-800">{{ selectedUser.firstname }} {{ selectedUser.lastname }}</span>
                    <span class="text-gray-400 ml-1.5 text-xs">{{ selectedUser.email }}</span>
                  </div>
                  <button type="button" @click.stop="clearSelectedUser"
                    class="text-gray-400 hover:text-gray-600 ml-auto flex-shrink-0 p-0.5 rounded hover:bg-white">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </template>
                <template v-else>
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                  </svg>
                  <span class="text-gray-400 flex-1">Search by name or email…</span>
                  <svg class="w-4 h-4 text-gray-400 flex-shrink-0 transition-transform"
                    :class="userPickerOpen ? 'rotate-180' : ''"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </template>
              </button>

              <!-- Dropdown -->
              <div v-if="userPickerOpen"
                class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden z-20">
                <!-- Search input -->
                <div class="p-2 border-b border-gray-100">
                  <input
                    v-model="userPickerSearch"
                    type="text"
                    placeholder="Type to filter…"
                    class="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
                  />
                </div>
                <!-- User list -->
                <div class="max-h-52 overflow-y-auto">
                  <div v-if="loadingUsers" class="p-4 text-center text-sm text-gray-400">Loading users…</div>
                  <div v-else-if="filteredAvailableUsers.length === 0" class="p-4 text-center text-sm text-gray-400">
                    No unregistered users found
                  </div>
                  <button v-else v-for="u in filteredAvailableUsers" :key="u.id"
                    type="button"
                    @click="selectUser(u)"
                    class="w-full flex items-center gap-3 px-4 py-2.5 hover:bg-[#e6f7fb] transition text-left border-b border-gray-50 last:border-0">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 uppercase"
                      style="background-color:#0095B6;">
                      {{ (u.firstname?.[0] || '') + (u.lastname?.[0] || '') }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="font-medium text-gray-800 text-sm truncate">{{ u.firstname }} {{ u.lastname }}</p>
                      <p class="text-xs text-gray-400 truncate">{{ u.email }}</p>
                    </div>
                  </button>
                </div>
              </div>
            </div>

            <!-- Participation Role -->
            <div>
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">
                Participation Role *
              </label>
              <select v-model="addForm.participation_role"
                class="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]">
                <option value="" disabled>Select a role…</option>
                <option value="secretariat">ECSA-HC Secretariat</option>
                <option value="moh">Country Delegate (Ministry of Health)</option>
                <option value="member_state">Participant – ECSA Member State</option>
                <option value="other_africa">Participant – Other African Country</option>
                <option value="world">International Participant</option>
                <option value="delegate">Delegate</option>
                <option value="presenter">Presenter</option>
                <option value="speaker">Speaker</option>
                <option value="moderator">Moderator</option>
                <option value="participant">General Participant</option>
                <option value="student">Student</option>
                <option value="exhibitor">Sponsor / Exhibitor</option>
                <option value="sponsor">Sponsor</option>
              </select>
            </div>

            <!-- Send invitation toggle -->
            <label class="flex items-center gap-3 cursor-pointer p-3 rounded-xl bg-gray-50 border border-gray-200 select-none">
              <input type="checkbox" v-model="addForm.send_invitation" class="w-4 h-4 accent-[#0095B6] rounded" />
              <div>
                <p class="text-sm font-semibold text-gray-700">Send invitation email</p>
                <p class="text-xs text-gray-400 mt-0.5">
                  Email the participant their login details and event information.
                  Always sent for new accounts.
                </p>
              </div>
            </label>

            <!-- Error / Success -->
            <div v-if="addParticipantError"
              class="flex items-start gap-2 p-3 rounded-xl text-sm text-red-700 bg-red-50 border border-red-200">
              ❌ {{ addParticipantError }}
            </div>
            <div v-if="addParticipantSuccess"
              class="flex items-start gap-2 p-3 rounded-xl text-sm text-green-700 bg-green-50 border border-green-200">
              ✅ {{ addParticipantSuccess }}
            </div>
          </div>

          <!-- Footer -->
          <div class="flex items-center justify-end gap-3 px-5 py-4 border-t border-gray-100 flex-shrink-0">
            <button @click="closeAddParticipantModal"
              class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 transition font-medium">
              Cancel
            </button>
            <button
              @click="submitAddParticipant"
              :disabled="addingParticipant || !selectedUser || !addForm.participation_role"
              class="inline-flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white rounded-xl transition hover:opacity-90 disabled:opacity-50"
              style="background-color:#0095B6;"
            >
              <svg v-if="addingParticipant" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
              </svg>
              {{ addingParticipant ? 'Adding…' : 'Add to Event' }}
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
import { ref, computed, onMounted } from 'vue'
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue'
import { EyeIcon, TrashIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'
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
const sendingReminders = ref(false)
const reminderMessage = ref('')
const reminderError = ref(false)
const selectedUnpaid = ref([])
const participantSearch = ref('')

const filteredParticipants = computed(() => {
  const q = participantSearch.value.toLowerCase().trim()
  if (!q) return participants.value
  return participants.value.filter(p =>
    `${p.firstname} ${p.lastname} ${p.email} ${p.country}`.toLowerCase().includes(q)
  )
})

const roleBreakdown = computed(() => {
  const counts = {}
  for (const p of participants.value) {
    const role = (typeof p.participation_role === 'object' ? p.participation_role?.name : p.participation_role) || 'unknown'
    counts[role] = (counts[role] || 0) + 1
  }
  return counts
})

// Pending = unpaid AND not yet reminded — these are the ones eligible for a new reminder
const unpaidParticipants = computed(() =>
  participants.value.filter(p => !p.paid && !p.reminder_sent_at)
)

function toggleParticipant(id) {
  const idx = selectedUnpaid.value.indexOf(id)
  if (idx === -1) selectedUnpaid.value.push(id)
  else selectedUnpaid.value.splice(idx, 1)
}

function toggleSelectAllUnpaid() {
  if (selectedUnpaid.value.length === unpaidParticipants.value.length) {
    selectedUnpaid.value = []
  } else {
    selectedUnpaid.value = unpaidParticipants.value.map(p => p.id)
  }
}

const loadingAttendance = ref(false)
const error = ref(null)

const selectedParticipant = ref(null)
const showBadge = ref(false)
const showUploadModal = ref(false)
const showAddLinkModal = ref(false)

// Payment proof modal
const showProofModal = ref(false)
const proofParticipant = ref(null)

// Add Participant modal
const showAddParticipantModal = ref(false)
const lookupResult = ref(null)
const addingParticipant = ref(false)
const addParticipantError = ref('')
const addParticipantSuccess = ref('')
const addForm = ref({
  email: '',
  firstname: '',
  lastname: '',
  participation_role: '',
  send_invitation: true,
})

// User picker state
const allUsers = ref([])
const loadingUsers = ref(false)
const userPickerSearch = ref('')
const userPickerOpen = ref(false)
const selectedUser = ref(null)

// Users already registered — used to exclude them from the picker
const alreadyRegisteredEmails = computed(() =>
  new Set(participants.value.map(p => (p.email || '').toLowerCase()))
)

// Filtered list: exclude registered users, filter by search text
const filteredAvailableUsers = computed(() => {
  const search = userPickerSearch.value.toLowerCase().trim()
  return allUsers.value
    .filter(u => !alreadyRegisteredEmails.value.has((u.email || '').toLowerCase()))
    .filter(u => {
      if (!search) return true
      const full = `${u.firstname || ''} ${u.lastname || ''} ${u.email || ''}`.toLowerCase()
      return full.includes(search)
    })
})

function viewParticipant(participant) {
  selectedParticipant.value = participant
  showBadge.value = true
}

function viewProof(participant) {
  proofParticipant.value = participant
  showProofModal.value = true
}

function isImageProof(path) {
  if (!path) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(path)
}

function proofUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${baseUrl}/${path}`
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
  if (!confirm(`Mark ${p.firstname} ${p.lastname} as paid? This will grant them full access.`)) return
  try {
    await api.put(`/events/verify_payment/${p.id}`)
    p.paid = true
  } catch (err) {
    alert('Failed to mark as paid: ' + (err.response?.data?.detail || err.message))
  }
}

async function unmarkPayment(p) {
  if (!confirm(`Mark ${p.firstname} ${p.lastname} as unpaid?`)) return
  try {
    await api.put(`/events/unverify_payment/${p.id}`)
    p.paid = false
  } catch (err) {
    alert('Failed to mark as unpaid: ' + (err.response?.data?.detail || err.message))
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

async function resetSingleAttendance(a) {
  if (!confirm(`Remove check-in record for ${a.firstname} ${a.lastname}?`)) return
  try {
    await api.delete(`/events/attendance/${a.id}`)
    attendance.value = attendance.value.filter(r => r.id !== a.id)
  } catch (err) {
    alert('Failed to reset attendance: ' + (err.response?.data?.detail || err.message))
  }
}

async function resetAllAttendance() {
  if (!confirm(`Reset ALL ${attendance.value.length} attendance record(s) for this event? This cannot be undone.`)) return
  try {
    await api.delete(`/events/${eventId}/attendance`)
    attendance.value = []
  } catch (err) {
    alert('Failed to reset attendance: ' + (err.response?.data?.detail || err.message))
  }
}

async function exportAttendance() {
  try {
    const res = await api.get(`/events/${eventId}/attendance/export`, { responseType: 'blob' })
    const cd = res.headers['content-disposition'] || ''
    const match = cd.match(/filename=([^;]+)/)
    const filename = match ? match[1].trim() : `attendance_event_${eventId}.xlsx`
    const blob = new Blob([res.data], { type: res.headers['content-type'] })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.click()
    URL.revokeObjectURL(link.href)
  } catch (err) {
    alert('Failed to export attendance: ' + (err.response?.data?.detail || err.message))
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

async function sendPaymentReminders() {
  const isSelective = selectedUnpaid.value.length > 0
  const count = isSelective ? selectedUnpaid.value.length : unpaidParticipants.value.length

  if (count === 0) {
    reminderError.value = false
    reminderMessage.value = 'All participants have already paid — no reminders to send.'
    setTimeout(() => reminderMessage.value = '', 5000)
    return
  }

  const label = isSelective
    ? `${count} selected participant(s)`
    : `all ${count} unpaid participant(s)`
  if (!confirm(`Send payment reminder email to ${label}?`)) return

  sendingReminders.value = true
  reminderMessage.value = ''
  try {
    const body = isSelective ? { registration_ids: selectedUnpaid.value } : { registration_ids: [] }
    const res = await api.post(`/events/${eventId}/send-payment-reminders`, body)
    reminderError.value = false
    reminderMessage.value = `✅ ${res.data.message}`
    selectedUnpaid.value = []
    // Refresh participant list so reminder timestamps update
    const refreshed = await api.get(`/events/${eventId}`)
    participants.value = refreshed.data.participants
  } catch (e) {
    reminderError.value = true
    reminderMessage.value = e.response?.data?.detail || 'Failed to send reminders. Please try again.'
  } finally {
    sendingReminders.value = false
    setTimeout(() => reminderMessage.value = '', 8000)
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

function closeAddParticipantModal() {
  showAddParticipantModal.value = false
  lookupResult.value = null
  addParticipantError.value = ''
  addParticipantSuccess.value = ''
  addForm.value = { email: '', firstname: '', lastname: '', participation_role: '', send_invitation: true }
  // Reset user picker
  allUsers.value = []
  userPickerSearch.value = ''
  userPickerOpen.value = false
  selectedUser.value = null
}

async function openAddParticipantModal() {
  showAddParticipantModal.value = true
  loadingUsers.value = true
  try {
    const res = await api.get('/users/?skip=0&limit=500')
    allUsers.value = res.data.data || res.data || []
  } catch (e) {
    console.error('Failed to load users for picker', e)
  } finally {
    loadingUsers.value = false
  }
}

function selectUser(u) {
  selectedUser.value = u
  addForm.value.email = u.email || ''
  addForm.value.firstname = u.firstname || ''
  addForm.value.lastname = u.lastname || ''
  lookupResult.value = { exists: true, already_registered: false, firstname: u.firstname, lastname: u.lastname }
  userPickerOpen.value = false
  userPickerSearch.value = ''
}

function clearSelectedUser() {
  selectedUser.value = null
  addForm.value.email = ''
  addForm.value.firstname = ''
  addForm.value.lastname = ''
  lookupResult.value = null
  userPickerSearch.value = ''
}

async function submitAddParticipant() {
  if (!addForm.value.email || !addForm.value.participation_role || !selectedUser.value) return
  addingParticipant.value = true
  addParticipantError.value = ''
  addParticipantSuccess.value = ''
  try {
    const res = await api.post(`/events/${eventId}/admin-add-participant`, {
      email: addForm.value.email,
      firstname: addForm.value.firstname,
      lastname: addForm.value.lastname,
      participation_role: addForm.value.participation_role,
      send_invitation: addForm.value.send_invitation,
    })
    addParticipantSuccess.value = res.data.message
    // Refresh participants list
    const refreshed = await api.get(`/events/${eventId}`)
    participants.value = refreshed.data.participants
    // Auto-close after 2.5 s
    setTimeout(() => closeAddParticipantModal(), 2500)
  } catch (e) {
    addParticipantError.value = e.response?.data?.detail || 'Failed to add participant.'
  } finally {
    addingParticipant.value = false
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
