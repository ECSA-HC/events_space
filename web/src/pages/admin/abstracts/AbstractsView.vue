<template>
  <div class="flex-1 flex flex-col w-full max-w-7xl mx-auto p-6 space-y-6 overflow-x-hidden">

    <!-- Page header -->
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-black">Abstract Submissions</h1>
        <p v-if="!loading" class="text-sm text-gray-400 mt-0.5">
          {{ total }} {{ total === 1 ? 'abstract' : 'abstracts' }}
          <span v-if="filterEvent || filterStatus || filterTrack || filterType || search"> (filtered)</span>
        </p>
      </div>
      <div class="flex items-center gap-2">
        <!-- Notify Accepted Authors -->
        <button @click="notifyModal.open = true"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition hover:opacity-90"
          style="background-color:#d1fae5; color:#065f46; border:1.5px solid #6ee7b7;">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          Notify Accepted Authors
        </button>

        <!-- PDF Book of Abstracts -->
        <button @click="exportPdf" :disabled="exportingPdf || loading || total === 0"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition hover:opacity-90 disabled:opacity-50"
          style="background-color:#fff; color:#0095B6; border:1.5px solid #0095B6;">
          <svg v-if="!exportingPdf" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          {{ exportingPdf ? 'Generating…' : 'Book of Abstracts PDF' }}
        </button>

        <!-- Excel export -->
        <button @click="exportExcel" :disabled="exporting || loading || total === 0"
          class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition hover:opacity-90 disabled:opacity-50"
          style="background-color:#0095B6;">
          <svg v-if="!exporting" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          {{ exporting ? 'Exporting…' : `Export${total > 0 ? ' ' + total : ''} to Excel` }}
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-2xl shadow p-4 flex flex-wrap gap-3">
      <input v-model="search" type="text" placeholder="Search by title..."
        class="input flex-1 min-w-[180px]" />
      <select v-model="filterEvent" class="input w-44">
        <option value="">All Events</option>
        <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
      </select>
      <select v-model="filterStatus" class="input w-40">
        <option value="">All Statuses</option>
        <option value="submitted">Submitted</option>
        <option value="under_review">Under Review</option>
        <option value="accepted">Accepted</option>
        <option value="rejected">Rejected</option>
        <option value="revision_required">Revision Required</option>
      </select>
      <select v-model.number="filterTrack" class="input w-44">
        <option value="">All Tracks</option>
        <option v-for="t in tracks" :key="t.id" :value="t.id">{{ t.code }}</option>
      </select>
      <select v-model="filterType" class="input w-40">
        <option value="">All Types</option>
        <option value="oral">Oral</option>
        <option value="poster">Poster</option>
      </select>
    </div>

    <!-- Active track filter badge -->
    <div v-if="filterTrack && activeTrackName"
      class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm border"
      style="background-color:#e6f7fb; border-color:#b3e4f0;">
      <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color:#0095B6;">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A2 2 0 013 12V7a2 2 0 012-2z"/>
      </svg>
      <span class="font-medium truncate" style="color:#006f87;">{{ activeTrackName }}</span>
      <button @click="filterTrack = ''"
        class="ml-auto flex-shrink-0 text-gray-400 hover:text-red-500 transition"
        title="Clear track filter">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- ── Floating bulk-action bar (appears when rows selected) ──────────── -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2">
      <div v-if="selectedIds.size > 0"
        class="sticky top-4 z-30 mx-auto w-full text-white rounded-2xl shadow-xl px-5 py-3 flex items-center gap-4 flex-wrap"
        style="background-color:#006f87;">
        <div class="flex items-center gap-2 flex-1">
          <input type="checkbox" class="w-4 h-4 accent-white cursor-pointer"
            :checked="selectedIds.size === paginated.length"
            :indeterminate="selectedIds.size > 0 && selectedIds.size < paginated.length"
            @change="toggleSelectAll" />
          <span class="font-semibold text-sm">
            {{ selectedIds.size }} abstract{{ selectedIds.size !== 1 ? 's' : '' }} selected
          </span>
          <button @click="selectedItems = new Map()"
            class="text-white/60 hover:text-white text-xs underline ml-1">Clear</button>
        </div>
        <button @click="openBulkModal"
          class="inline-flex items-center gap-2 px-4 py-2 bg-white font-semibold text-sm rounded-xl hover:bg-gray-50 transition flex-shrink-0"
          style="color:#0095B6;">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
          </svg>
          Assign Reviewers to Selected
        </button>
      </div>
    </transition>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow overflow-hidden">
      <div v-if="loading" class="p-8 text-center text-gray-500">Loading abstracts...</div>
      <div v-else-if="abstracts.length === 0" class="p-8 text-center text-gray-400">No abstracts found.</div>

      <table v-else class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-600 text-xs uppercase">
          <tr>
            <!-- Select-all checkbox -->
            <th class="px-3 py-3 w-8">
              <input type="checkbox" class="w-4 h-4 cursor-pointer"
                style="accent-color:#0095B6;"
                :checked="paginated.length > 0 && selectedIds.size === paginated.length"
                :indeterminate="selectedIds.size > 0 && selectedIds.size < paginated.length"
                @change="toggleSelectAll" />
            </th>
            <th class="px-4 py-3 text-left">Title</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell" title="Hover a track badge to see full title">Track</th>
            <th class="px-4 py-3 text-left hidden md:table-cell">First Author</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell">Type</th>
            <th class="px-4 py-3 text-left">Status</th>
            <th class="px-4 py-3 text-left hidden lg:table-cell">Reviewers</th>
            <th class="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="abs in paginated" :key="abs.id"
            class="hover:bg-gray-50 transition"
            :class="selectedIds.has(abs.id) ? 'bg-[#e6f7fb]' : ''">
            <!-- Row checkbox -->
            <td class="px-3 py-3">
              <input type="checkbox" class="w-4 h-4 cursor-pointer"
                style="accent-color:#0095B6;"
                :checked="selectedIds.has(abs.id)"
                @change="toggleRow(abs)" />
            </td>
            <td class="px-4 py-3 font-medium text-gray-800 max-w-[200px] truncate">{{ abs.title }}</td>
            <td class="px-4 py-3 hidden lg:table-cell">
              <router-link v-if="abs.track_code"
                :to="{ name: 'AdminTracks', query: { event_id: abs.event_id } }"
                class="inline-flex items-center text-xs font-bold px-2 py-0.5 rounded-full border transition-opacity hover:opacity-75"
                style="background-color:#e6f7fb; color:#006f87; border-color:#b3e4f0;"
                :title="abs.track_title ? abs.track_code + ': ' + abs.track_title : abs.track_code">
                {{ abs.track_code }}
              </router-link>
              <span v-else class="text-gray-300 text-xs">—</span>
            </td>
            <td class="px-4 py-3 text-gray-600 hidden md:table-cell">
              {{ abs.authors?.[0] ? `${abs.authors[0].firstname} ${abs.authors[0].lastname}` : '—' }}
            </td>
            <td class="px-4 py-3 text-gray-500 capitalize hidden lg:table-cell">{{ abs.presentation_type }}</td>
            <td class="px-4 py-3">
              <span :class="statusClass(abs.status)" class="px-2 py-1 rounded-full text-xs font-semibold capitalize">
                {{ abs.status?.replace('_', ' ') }}
              </span>
            </td>
            <!-- Reviewer count pill with hover tooltip -->
            <td class="px-4 py-3 hidden lg:table-cell">
              <div v-if="abs.reviewer_assignments?.length" class="relative inline-block group">
                <span class="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full font-medium border cursor-default"
                  style="color:#0095B6; background-color:#e6f7fb; border-color:#b3e4f0;">
                  <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  {{ abs.reviewer_assignments.length }}
                </span>
                <!-- Hover tooltip listing reviewer names -->
                <div class="absolute z-50 left-0 top-full mt-1 hidden group-hover:block
                            bg-white border border-gray-200 rounded-xl shadow-lg py-2 min-w-[180px]">
                  <p class="text-xs font-semibold text-gray-400 uppercase px-3 pb-1">Reviewers</p>
                  <div v-for="ra in abs.reviewer_assignments" :key="ra.id"
                       class="px-3 py-1 text-xs text-gray-700 hover:bg-gray-50">
                    {{ ra.reviewer_name }}
                    <span class="block text-gray-400 truncate">{{ ra.reviewer_email }}</span>
                  </div>
                </div>
              </div>
              <span v-else class="text-gray-300 text-xs">—</span>
            </td>
            <!-- Actions -->
            <td class="px-4 py-3 text-right">
              <div class="flex items-center justify-end gap-2">
                <button @click.stop="openQuickAssign(abs)"
                  class="inline-flex items-center gap-1 px-2 py-1 text-xs font-semibold rounded-lg border transition"
                  :class="abs.reviewer_assignments?.length
                    ? 'border-gray-200 hover:bg-[#e6f7fb]'
                    : 'border-gray-200 text-gray-500 hover:bg-gray-50'"
                  :style="abs.reviewer_assignments?.length ? 'color:#0095B6;' : ''"
                  title="Assign reviewer">
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/>
                  </svg>
                  Assign
                </button>
                <router-link :to="{ name: 'AdminAbstract', params: { id: abs.id } }"
                  class="text-bondi-blue hover:underline text-xs font-medium">View</router-link>
                <button @click="deleteAbstract(abs)"
                  class="text-red-400 hover:text-red-600 text-xs font-medium">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div v-if="total > pageSize"
        class="flex items-center justify-between px-4 py-3 border-t text-sm text-gray-500 flex-wrap gap-2">
        <span>{{ ((page - 1) * pageSize) + 1 }}–{{ Math.min(page * pageSize, total) }} of {{ total }}</span>
        <div class="flex items-center gap-1">
          <button @click="goToPage(1)" :disabled="page === 1"
            class="px-2 py-1 rounded border disabled:opacity-40 text-xs">«</button>
          <button @click="goToPage(page - 1)" :disabled="page === 1"
            class="px-3 py-1 rounded border disabled:opacity-40">Prev</button>
          <template v-for="p in pageNumbers" :key="p">
            <span v-if="p === '...'" class="px-2 py-1 text-gray-400">…</span>
            <button v-else @click="goToPage(p)"
              class="px-3 py-1 rounded border transition"
              :class="p === page ? 'text-white border-[#0095B6]' : 'hover:bg-gray-50'"
              :style="p === page ? 'background-color:#0095B6;' : ''">
              {{ p }}
            </button>
          </template>
          <button @click="goToPage(page + 1)" :disabled="page === totalPages"
            class="px-3 py-1 rounded border disabled:opacity-40">Next</button>
          <button @click="goToPage(totalPages)" :disabled="page === totalPages"
            class="px-2 py-1 rounded border disabled:opacity-40 text-xs">»</button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         QUICK ASSIGN MODAL  (single abstract, multiple reviewers one-by-one)
    ════════════════════════════════════════════════════════════════════════ -->
    <div v-if="quickModal.open"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
      @click.self="quickModal.open = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md flex flex-col max-h-[90vh]">

        <div class="flex items-center justify-between px-5 py-4 border-b flex-shrink-0">
          <div>
            <p class="font-bold text-gray-800 text-sm">Assign Reviewer</p>
            <p class="text-xs text-gray-400 mt-0.5 max-w-[300px] truncate">{{ quickModal.abstract?.title }}</p>
          </div>
          <button @click="quickModal.open = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="p-5 space-y-4 overflow-y-auto flex-1">
          <!-- Current reviewers -->
          <div v-if="quickModal.abstract?.reviewer_assignments?.length">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Currently Assigned</p>
            <div class="space-y-1.5">
              <div v-for="ra in quickModal.abstract.reviewer_assignments" :key="ra.id"
                class="flex items-center justify-between px-3 py-2 bg-gray-50 rounded-lg text-sm">
                <div>
                  <span class="font-medium">{{ ra.reviewer_name }}</span>
                  <span class="text-gray-400 text-xs ml-2">{{ ra.reviewer_email }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span :class="ra.completed ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'"
                    class="px-2 py-0.5 rounded-full text-xs font-semibold">
                    {{ ra.completed ? '✓ Done' : '⏳ Pending' }}
                  </span>
                  <button @click="quickRemove(ra.reviewer_id)" class="text-red-400 hover:text-red-600 text-xs">✕</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Reviewer picker -->
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1.5">
              Add Reviewer
            </label>
            <!-- Search input -->
            <div class="relative flex items-center border rounded-xl overflow-hidden transition-colors focus-within:ring-2 focus-within:ring-[#0095B6] mb-1"
              :class="quickModal.search ? 'border-[#0095B6]' : 'border-gray-300'">
              <div class="pl-3 flex-shrink-0">
                <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z"/>
                </svg>
              </div>
              <input v-model="quickModal.search" type="text"
                placeholder="Filter reviewers…"
                class="flex-1 bg-transparent text-sm px-3 py-2.5 outline-none placeholder-gray-400"
                ref="quickSearchRef" />
              <button v-if="quickModal.search" @click="quickModal.search = ''; quickModal.selected = null"
                class="pr-3 flex-shrink-0 text-gray-300 hover:text-gray-500">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Reviewer list (always visible) -->
            <div class="border border-gray-200 rounded-xl overflow-hidden">
              <div v-if="loadingReviewers" class="px-4 py-4 text-sm text-gray-400 text-center">
                Loading reviewers…
              </div>
              <div v-else-if="quickFilteredReviewers.length === 0" class="px-4 py-4 text-sm text-gray-400 text-center">
                {{ quickModal.search ? 'No reviewers match' : 'No reviewers available' }}
              </div>
              <div v-else class="max-h-44 overflow-y-auto divide-y divide-gray-50">
                <div v-for="u in quickFilteredReviewers" :key="u.id"
                  @click="quickSelect(u)"
                  class="px-4 py-2.5 text-sm flex items-center gap-3 cursor-pointer transition-colors"
                  :class="quickModal.selected?.id === u.id ? 'bg-[#e6f7fb]' : 'hover:bg-[#e6f7fb]'">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 uppercase"
                    style="background-color:#0095B6;">
                    {{ u.firstname?.[0] }}{{ u.lastname?.[0] }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-800 truncate">{{ u.firstname }} {{ u.lastname }}</p>
                    <p class="text-xs text-gray-400 truncate">{{ u.email }}</p>
                  </div>
                  <span v-if="quickModal.selected?.id === u.id"
                    class="text-xs font-bold flex-shrink-0" style="color:#0095B6;">✓</span>
                </div>
              </div>
            </div>
          </div>

          <p v-if="quickModal.successMsg" class="text-green-600 text-sm text-center">✅ {{ quickModal.successMsg }}</p>
          <p v-if="quickModal.errorMsg" class="text-red-500 text-sm text-center">❌ {{ quickModal.errorMsg }}</p>
        </div>

        <div class="flex justify-end gap-3 px-5 py-4 border-t flex-shrink-0">
          <button @click="quickModal.open = false"
            class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 font-medium">
            Close
          </button>
          <button @click="quickAssign" :disabled="!quickModal.selected || quickModal.assigning"
            class="inline-flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white rounded-xl disabled:opacity-50 transition hover:opacity-90"
            style="background-color:#0095B6;">
            <svg v-if="quickModal.assigning" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
            </svg>
            {{ quickModal.assigning ? 'Assigning…' : 'Assign' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         BULK ASSIGN MODAL  (multiple abstracts × multiple reviewers)
    ════════════════════════════════════════════════════════════════════════ -->
    <div v-if="bulkModal.open"
      class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
      @click.self="bulkModal.open = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-xl flex flex-col max-h-[92vh]">

        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-4 border-b flex-shrink-0">
          <div class="flex items-center gap-3">
            <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0"
              style="background-color:#e6f7fb;">
              <svg class="w-5 h-5" style="color:#0095B6;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <div>
              <p class="font-bold text-gray-800 text-sm">Bulk Assign Reviewers</p>
              <p class="text-xs text-gray-400 mt-0.5">
                {{ selectedIds.size }} abstract{{ selectedIds.size !== 1 ? 's' : '' }} selected
              </p>
            </div>
          </div>
          <button @click="bulkModal.open = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="p-5 space-y-5 overflow-y-auto flex-1">

          <!-- Selected abstracts summary -->
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Abstracts to assign</p>
            <div class="max-h-36 overflow-y-auto space-y-1.5 pr-1">
              <div v-for="abs in selectedAbstracts" :key="abs.id"
                class="flex items-start gap-2 px-3 py-2 bg-gray-50 rounded-lg text-xs">
                <span class="text-gray-400 flex-shrink-0 font-mono">#{{ abs.id }}</span>
                <span class="font-medium text-gray-700 truncate flex-1">{{ abs.title }}</span>
                <span v-if="abs.reviewer_assignments?.length"
                  class="flex-shrink-0 text-xs font-medium" style="color:#0095B6;">
                  {{ abs.reviewer_assignments.length }} reviewer{{ abs.reviewer_assignments.length !== 1 ? 's' : '' }}
                </span>
                <button @click="selectedItems = new Map([...selectedItems].filter(([k]) => k !== abs.id))"
                  class="text-gray-300 hover:text-red-400 flex-shrink-0">✕</button>
              </div>
            </div>
          </div>

          <!-- Reviewer search (multi-select as chips) -->
          <div>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">
              Reviewers to assign
              <span v-if="bulkModal.reviewers.length"
                class="ml-1 px-1.5 py-0.5 rounded-full text-xs font-bold"
                style="background-color:#e6f7fb; color:#0095B6;">
                {{ bulkModal.reviewers.length }}
              </span>
            </p>

            <!-- Chips of selected reviewers -->
            <div v-if="bulkModal.reviewers.length" class="flex flex-wrap gap-2 mb-3">
              <span v-for="r in bulkModal.reviewers" :key="r.id"
                class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border"
                style="background-color:#e6f7fb; color:#006f87; border-color:#b3e4f0;">
                {{ r.firstname }} {{ r.lastname }}
                <button @click="removeBulkReviewer(r.id)"
                  class="leading-none hover:text-red-500 transition-colors" style="color:#0095B6;">✕</button>
              </span>
            </div>

            <!-- Search input -->
            <div class="relative flex items-center border rounded-xl overflow-hidden transition-colors focus-within:ring-2 focus-within:ring-[#0095B6] mb-1"
              :class="bulkModal.search ? 'border-[#0095B6]' : 'border-gray-300'">
              <div class="pl-3 flex-shrink-0">
                <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M21 21l-4.35-4.35M17 11A6 6 0 115 11a6 6 0 0112 0z"/>
                </svg>
              </div>
              <input v-model="bulkModal.search" type="text"
                placeholder="Filter reviewers…"
                class="flex-1 bg-transparent text-sm px-3 py-2.5 outline-none placeholder-gray-400 text-gray-700" />
              <button v-if="bulkModal.search" @click="bulkModal.search = ''"
                class="pr-3 flex-shrink-0 text-gray-300 hover:text-gray-500">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Reviewer list (always visible) -->
            <div class="border border-gray-200 rounded-xl overflow-hidden mb-2">
              <div v-if="loadingReviewers" class="px-4 py-4 text-sm text-gray-400 text-center">
                Loading reviewers…
              </div>
              <div v-else-if="bulkFilteredReviewers.length === 0" class="px-4 py-4 text-sm text-gray-400 text-center">
                {{ bulkModal.search ? 'No reviewers match' : 'No reviewers available' }}
              </div>
              <div v-else class="max-h-48 overflow-y-auto divide-y divide-gray-50">
                <div v-for="u in bulkFilteredReviewers" :key="u.id"
                  @click="addBulkReviewer(u)"
                  class="px-4 py-2.5 text-sm flex items-center gap-3 transition-colors"
                  :class="bulkModal.reviewers.find(r => r.id === u.id)
                    ? 'bg-[#e6f7fb] cursor-default'
                    : 'hover:bg-[#e6f7fb] cursor-pointer'">
                  <div class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold flex-shrink-0 uppercase"
                    style="background-color:#0095B6;">
                    {{ u.firstname?.[0] }}{{ u.lastname?.[0] }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-800 truncate">{{ u.firstname }} {{ u.lastname }}</p>
                    <p class="text-xs text-gray-400 truncate">{{ u.email }}</p>
                  </div>
                  <span v-if="bulkModal.reviewers.find(r => r.id === u.id)"
                    class="text-xs font-bold flex-shrink-0" style="color:#0095B6;">✓ Added</span>
                  <span v-else class="text-xs text-gray-300 flex-shrink-0">+ Add</span>
                </div>
              </div>
            </div>
            <p class="text-xs text-gray-400">Click to add reviewers — all selected will be assigned to every chosen abstract.</p>
          </div>

          <!-- Progress / results -->
          <div v-if="bulkModal.done">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">Results</p>
            <div class="space-y-1 max-h-44 overflow-y-auto">
              <div v-for="r in bulkModal.results_log" :key="r.key"
                class="flex items-center gap-2 text-xs px-3 py-1.5 rounded-lg"
                :class="r.ok ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600'">
                {{ r.ok ? '✅' : '❌' }} {{ r.msg }}
              </div>
            </div>
          </div>

          <!-- Progress bar while assigning -->
          <div v-if="bulkModal.assigning" class="space-y-2">
            <div class="flex items-center justify-between text-xs text-gray-500">
              <span>Assigning… {{ bulkModal.progress }} / {{ bulkModal.total }}</span>
              <span>{{ Math.round(bulkModal.progress / bulkModal.total * 100) }}%</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-2">
              <div class="h-2 rounded-full transition-all duration-300"
                style="background-color:#0095B6;"
                :style="{ width: `${Math.round(bulkModal.progress / bulkModal.total * 100)}%` }">
              </div>
            </div>
          </div>

        </div>

        <!-- Footer -->
        <div class="flex items-center justify-end gap-3 px-5 py-4 border-t flex-shrink-0">
          <button @click="bulkModal.open = false"
            class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 font-medium">
            {{ bulkModal.done ? 'Close' : 'Cancel' }}
          </button>
          <button v-if="!bulkModal.done"
            @click="runBulkAssign"
            :disabled="bulkModal.assigning || bulkModal.reviewers.length === 0 || selectedIds.size === 0"
            class="inline-flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white rounded-xl disabled:opacity-50 transition hover:opacity-90"
            style="background-color:#0095B6;">
            <svg v-if="bulkModal.assigning" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
            </svg>
            <span v-if="bulkModal.assigning">Assigning…</span>
            <span v-else>
              Assign {{ bulkModal.reviewers.length }} reviewer{{ bulkModal.reviewers.length !== 1 ? 's' : '' }}
              to {{ selectedIds.size }} abstract{{ selectedIds.size !== 1 ? 's' : '' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         NOTIFY ACCEPTED AUTHORS MODAL
    ════════════════════════════════════════════════════════════════════════ -->
    <div v-if="notifyModal.open"
      class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
      @click.self="notifyModal.open = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg flex flex-col max-h-[92vh]">

        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-4 border-b flex-shrink-0">
          <div class="flex items-center gap-3">
            <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color:#d1fae5;">
              <svg class="w-5 h-5" style="color:#065f46;" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <div>
              <p class="font-bold text-gray-800 text-sm">Notify Accepted Authors</p>
              <p class="text-xs text-gray-400 mt-0.5">Send acceptance notification emails to accepted abstract authors</p>
            </div>
          </div>
          <button @click="notifyModal.open = false" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="p-5 space-y-4 overflow-y-auto flex-1">

          <!-- Event filter -->
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1.5">Event (optional)</label>
            <select v-model.number="notifyModal.eventId" class="input w-full">
              <option :value="null">All Events</option>
              <option v-for="e in events" :key="e.id" :value="e.id">{{ e.event }}</option>
            </select>
            <p class="text-xs text-gray-400 mt-1">Leave blank to notify accepted authors across all events.</p>
          </div>

          <!-- Portal URL -->
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1.5">Portal URL</label>
            <input v-model="notifyModal.portalUrl" type="url" class="input w-full" placeholder="https://events.ecsahc.org" />
          </div>

          <!-- PPT Template URL -->
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1.5">ECSA PPT Template URL</label>
            <input v-model="notifyModal.pptUrl" type="url" class="input w-full" placeholder="https://www.ecsahc.org/..." />
            <p class="text-xs text-gray-400 mt-1">Link authors will use to download the ECSA PowerPoint template.</p>
          </div>

          <!-- Test email -->
          <div>
            <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1.5">Test Email (optional)</label>
            <input v-model="notifyModal.testEmail" type="email" class="input w-full" placeholder="Leave blank to send to real authors" />
            <p class="text-xs text-gray-400 mt-1">If set, ALL emails are sent to this address instead of the actual authors.</p>
          </div>

          <!-- Results -->
          <div v-if="notifyModal.done" class="bg-green-50 border border-green-200 rounded-xl p-4">
            <p class="font-semibold text-green-700 text-sm mb-1">
              ✅ {{ notifyModal.result.sent }} email{{ notifyModal.result.sent !== 1 ? 's' : '' }} sent
            </p>
            <p v-if="notifyModal.result.failed" class="text-sm text-red-600">
              ⚠️ {{ notifyModal.result.failed }} failed
            </p>
          </div>

          <p v-if="notifyModal.error" class="text-red-500 text-sm">{{ notifyModal.error }}</p>

        </div>

        <!-- Footer -->
        <div class="flex items-center justify-end gap-3 px-5 py-4 border-t flex-shrink-0">
          <button @click="notifyModal.open = false"
            class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 font-medium">
            {{ notifyModal.done ? 'Close' : 'Cancel' }}
          </button>
          <button v-if="!notifyModal.done"
            @click="runNotifyAccepted"
            :disabled="notifyModal.sending"
            class="inline-flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white rounded-xl disabled:opacity-50 transition hover:opacity-90"
            style="background-color:#059669;">
            <svg v-if="notifyModal.sending" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
            </svg>
            {{ notifyModal.sending ? 'Sending…' : (notifyModal.testEmail ? 'Send Test Email' : 'Send Notifications') }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/plugins/axios'

const route        = useRoute()

const abstracts    = ref([])   // current page only
const total        = ref(0)    // total matching records from server
const events       = ref([])
const tracks       = ref([])
const loading      = ref(true)
const exporting    = ref(false)
const exportingPdf = ref(false)
const search       = ref('')
const filterEvent  = ref('')
const filterStatus = ref('')
const filterTrack  = ref('')
const filterType   = ref('')
const page         = ref(1)
const pageSize     = 50

// Cross-page selection: Map<id, abstractObj>
const selectedItems = ref(new Map())
const selectedIds   = computed(() => new Set(selectedItems.value.keys()))

const quickSearchRef = ref(null)

// ── Shared reviewer pool (loaded once for quick + bulk modals) ───────────────
const allReviewers      = ref([])
const loadingReviewers  = ref(false)

async function loadAllReviewers() {
  if (allReviewers.value.length > 0) return // already cached
  loadingReviewers.value = true
  try {
    const res = await api.get('/abstracts/reviewers/candidates')
    allReviewers.value = res.data || []
  } catch (e) {
    console.error('Failed to load reviewers', e)
  } finally {
    loadingReviewers.value = false
  }
}

// ── Quick-assign modal (single abstract) ────────────────────────────────────
const quickModal = ref({
  open: false, abstract: null,
  search: '', selected: null,
  assigning: false, successMsg: '', errorMsg: '',
})

// Reviewers filtered for quick-assign: exclude already-assigned + match search
const quickFilteredReviewers = computed(() => {
  const q = (quickModal.value.search || '').toLowerCase().trim()
  const assignedIds = new Set(
    (quickModal.value.abstract?.reviewer_assignments || []).map(ra => ra.reviewer_id)
  )
  return allReviewers.value
    .filter(u => !assignedIds.has(u.id))
    .filter(u => {
      if (!q) return true
      return `${u.firstname || ''} ${u.lastname || ''} ${u.email || ''}`.toLowerCase().includes(q)
    })
})

function openQuickAssign(abs) {
  quickModal.value = {
    open: true, abstract: abs,
    search: '', selected: null,
    assigning: false, successMsg: '', errorMsg: '',
  }
  loadAllReviewers()
  nextTick(() => quickSearchRef.value?.focus())
}

function quickSelect(u) {
  quickModal.value.selected = u
}

async function quickAssign() {
  if (!quickModal.value.selected) return
  quickModal.value.assigning  = true
  quickModal.value.successMsg = ''
  quickModal.value.errorMsg   = ''
  try {
    await api.post(`/abstracts/${quickModal.value.abstract.id}/assign-reviewer`, {
      reviewer_id: quickModal.value.selected.id,
    })
    quickModal.value.successMsg = `${quickModal.value.selected.firstname} ${quickModal.value.selected.lastname} assigned.`
    quickModal.value.selected   = null
    quickModal.value.search     = ''
    // Refresh abstract in list
    const fresh = await api.get(`/abstracts/${quickModal.value.abstract.id}`)
    const idx = abstracts.value.findIndex(a => a.id === quickModal.value.abstract.id)
    if (idx !== -1) { abstracts.value[idx] = fresh.data; quickModal.value.abstract = fresh.data }
  } catch (e) {
    quickModal.value.errorMsg = e.response?.data?.detail || 'Failed to assign reviewer.'
  } finally {
    quickModal.value.assigning = false
  }
}

async function quickRemove(reviewerId) {
  if (!confirm('Remove this reviewer?')) return
  await api.delete(`/abstracts/${quickModal.value.abstract.id}/reviewers/${reviewerId}`)
  const fresh = await api.get(`/abstracts/${quickModal.value.abstract.id}`)
  const idx = abstracts.value.findIndex(a => a.id === quickModal.value.abstract.id)
  if (idx !== -1) { abstracts.value[idx] = fresh.data; quickModal.value.abstract = fresh.data }
}

// ── Bulk-assign modal (multiple abstracts × multiple reviewers) ──────────────
const bulkModal = ref({
  open: false,
  search: '', reviewers: [],
  assigning: false, done: false,
  progress: 0, total: 0, results_log: [],
})
const bulkDropdownOpen = ref(false)

const selectedAbstracts = computed(() => [...selectedItems.value.values()])

// Reviewers filtered for bulk-assign: match search + not already chip-selected
const bulkFilteredReviewers = computed(() => {
  const q = (bulkModal.value.search || '').toLowerCase().trim()
  return allReviewers.value.filter(u => {
    if (!q) return true
    return `${u.firstname || ''} ${u.lastname || ''} ${u.email || ''}`.toLowerCase().includes(q)
  })
})

function openBulkModal() {
  bulkModal.value = {
    open: true,
    search: '', reviewers: [],
    assigning: false, done: false,
    progress: 0, total: 0, results_log: [],
  }
  bulkDropdownOpen.value = false
  loadAllReviewers()
}

function addBulkReviewer(u) {
  if (bulkModal.value.reviewers.find(r => r.id === u.id)) return
  bulkModal.value.reviewers.push(u)
  bulkModal.value.search = ''
}

function removeBulkReviewer(id) {
  bulkModal.value.reviewers = bulkModal.value.reviewers.filter(r => r.id !== id)
}

async function runBulkAssign() {
  const abstractIds = [...selectedIds.value]  // selectedIds is now a computed Set
  const reviewers   = bulkModal.value.reviewers
  if (!abstractIds.length || !reviewers.length) return

  bulkModal.value.assigning   = true
  bulkModal.value.done        = false
  bulkModal.value.progress    = 0
  bulkModal.value.total       = reviewers.length
  bulkModal.value.results_log = []

  // One request per reviewer — backend sends a single consolidated email per reviewer
  for (const r of reviewers) {
    try {
      const res = await api.post('/abstracts/bulk-assign-reviewer', {
        reviewer_id:  r.id,
        abstract_ids: abstractIds,
      })
      const { assigned, skipped } = res.data
      bulkModal.value.results_log.push({
        key: r.id, ok: true,
        msg: `${r.firstname} ${r.lastname}: ${assigned} assigned${skipped.length ? `, ${skipped.length} skipped` : ''} — 1 email sent`,
      })
    } catch (e) {
      bulkModal.value.results_log.push({
        key: r.id, ok: false,
        msg: `${r.firstname} ${r.lastname}: ${e.response?.data?.detail || 'failed'}`,
      })
    }
    bulkModal.value.progress++
  }

  bulkModal.value.assigning = false
  bulkModal.value.done      = true
  selectedItems.value = new Map()
  fetchAbstracts()
}

// ── Row/page selection helpers ───────────────────────────────────────────────
function toggleRow(abs) {
  const m = new Map(selectedItems.value)
  m.has(abs.id) ? m.delete(abs.id) : m.set(abs.id, abs)
  selectedItems.value = m
}

function toggleSelectAll() {
  const m = new Map(selectedItems.value)
  const allOnPage = abstracts.value.every(a => m.has(a.id))
  if (allOnPage) {
    abstracts.value.forEach(a => m.delete(a.id))
  } else {
    abstracts.value.forEach(a => m.set(a.id, a))
  }
  selectedItems.value = m
}

function goToPage(p) {
  if (p < 1 || p > totalPages.value || p === page.value) return
  page.value = p
}

// ── Data / filters ───────────────────────────────────────────────────────────
async function fetchAbstracts() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('skip',  String((page.value - 1) * pageSize))
    params.set('limit', String(pageSize))
    if (filterEvent.value)  params.set('event_id',          filterEvent.value)
    if (filterStatus.value) params.set('status',            filterStatus.value)
    if (filterTrack.value)  params.set('track_id',          filterTrack.value)
    if (filterType.value)   params.set('presentation_type', filterType.value)
    if (search.value.trim()) params.set('search',           search.value.trim())
    const res = await api.get(`/abstracts/?${params}`)
    abstracts.value = res.data.data  || []
    total.value     = res.data.total ?? 0
  } finally {
    loading.value = false
  }
}

// Reset to page 1 and refetch when any filter changes
watch([search, filterEvent, filterStatus, filterTrack, filterType], () => {
  page.value = 1
  fetchAbstracts()
})

watch(page, fetchAbstracts)

onMounted(async () => {
  if (route.query.track_id) filterTrack.value = Number(route.query.track_id)

  try {
    const [evRes, trackRes] = await Promise.all([
      api.get('/events/?skip=0&limit=200'),
      api.get('/abstracts/tracks/list'),
    ])
    events.value = evRes.data.data || []
    tracks.value = trackRes.data   || []
  } catch (_) {}

  await fetchAbstracts()
})

const exportExcel = async () => {
  exporting.value = true
  try {
    const params = new URLSearchParams()
    if (filterEvent.value)   params.append('event_id', filterEvent.value)
    if (filterStatus.value)  params.append('status',   filterStatus.value)
    if (search.value.trim()) params.append('search',   search.value.trim())
    const res = await api.get(`/abstracts/export?${params.toString()}`, { responseType: 'blob' })
    const parts = ['abstracts']
    if (filterStatus.value) parts.push(filterStatus.value.replace('_', '-'))
    if (search.value.trim()) parts.push(search.value.trim().slice(0, 20).replace(/\s+/g, '-'))
    parts.push(new Date().toISOString().slice(0, 10))
    const url = URL.createObjectURL(new Blob([res.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }))
    const a = document.createElement('a')
    a.href = url; a.download = `${parts.join('_')}.xlsx`; a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('Export failed. Please try again.')
  } finally {
    exporting.value = false
  }
}

const exportPdf = async () => {
  exportingPdf.value = true
  try {
    const params = new URLSearchParams()
    if (filterEvent.value)  params.append('event_id', filterEvent.value)
    if (filterStatus.value) params.append('status',   filterStatus.value)
    const res = await api.get(`/abstracts/export/pdf?${params.toString()}`, { responseType: 'blob' })
    const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }))
    const a = document.createElement('a')
    a.href = url
    a.download = `book_of_abstracts_${new Date().toISOString().slice(0, 10)}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('PDF export failed. Please try again.')
  } finally {
    exportingPdf.value = false
  }
}

const deleteAbstract = async (abs) => {
  if (!confirm(`Delete "${abs.title}"? This cannot be undone.`)) return
  try {
    await api.delete(`/abstracts/${abs.id}`)
    abstracts.value = abstracts.value.filter(a => a.id !== abs.id)
    total.value = Math.max(0, total.value - 1)
    const m = new Map(selectedItems.value); m.delete(abs.id); selectedItems.value = m
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete abstract')
  }
}

// Server already filters — paginated is just the current page from the API
const paginated  = computed(() => abstracts.value)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

// Smart page number list: 1 … 4 5 6 … 12
const pageNumbers = computed(() => {
  const tp = totalPages.value
  const p  = page.value
  if (tp <= 7) return Array.from({ length: tp }, (_, i) => i + 1)
  const pages = new Set([1, tp, p, p - 1, p + 1].filter(n => n >= 1 && n <= tp))
  const sorted = [...pages].sort((a, b) => a - b)
  const result = []
  let prev = 0
  for (const n of sorted) {
    if (n - prev > 1) result.push('...')
    result.push(n)
    prev = n
  }
  return result
})

// Name of the currently active track filter (for display)
const activeTrackName = computed(() => {
  if (!filterTrack.value) return ''
  const t = tracks.value.find(t => t.id === filterTrack.value)
  return t ? `${t.code}: ${t.title}` : ''
})

const statusClass = (s) => ({
  submitted: 'bg-blue-100 text-blue-700',
  under_review: 'bg-yellow-100 text-yellow-700',
  accepted: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
  revision_required: 'bg-orange-100 text-orange-700',
}[s] || 'bg-gray-100 text-gray-600')

// ── Notify Accepted Authors ──────────────────────────────────────────────────
const notifyModal = ref({
  open: false,
  eventId: null,
  portalUrl: 'https://events.ecsahc.org',
  pptUrl: 'https://www.ecsahc.org',
  testEmail: '',
  sending: false,
  done: false,
  result: { sent: 0, failed: 0 },
  error: '',
})

const runNotifyAccepted = async () => {
  const m = notifyModal.value
  m.sending = true
  m.error = ''
  try {
    const payload = {
      portal_url: m.portalUrl,
      ppt_template_url: m.pptUrl,
    }
    if (m.eventId) payload.event_id = m.eventId
    if (m.testEmail) payload.test_email = m.testEmail
    const res = await api.post('/abstracts/notify-acceptance', payload)
    m.result = { sent: res.data.sent, failed: res.data.failed }
    m.done = true
  } catch (e) {
    m.error = e.response?.data?.detail || 'Failed to send notifications. Please try again.'
  } finally {
    m.sending = false
  }
}
</script>
