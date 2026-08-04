<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
    <AdminBar title="Users">
      <a href="#" class="text-sm text-blue-600 hover:underline">Users</a>
    </AdminBar>

    <!-- Page Title -->
    <div class="px-6 pt-4 pb-2">
      <h1 class="text-xl font-bold text-gray-800">Users</h1>
    </div>

    <!-- Success banner (e.g. after adding a user) -->
    <div v-if="successMessage" class="mx-6 mt-2 p-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">
      {{ successMessage }}
    </div>

    <!-- Search & Add -->
    <div class="px-6 pb-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <input
        v-model="search"
        type="text"
        placeholder="Search users..."
        class="w-full md:w-1/3 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0095B6]"
      />
      <router-link
        :to="{ name: 'AddUser' }"
        v-if="canAddUser"
        class="bg-[#0095B6] hover:bg-[#007B97] text-white px-6 py-2 rounded-xl transition"
      >
        + Add User
      </router-link>
    </div>

    <!-- Users List -->
    <main class="px-6 pb-6">
      <div class="w-full overflow-hidden bg-white shadow rounded-lg">
        <table class="w-full table-auto text-sm text-gray-800 rounded-lg overflow-hidden">
          <thead class="bg-gray-100 text-left uppercase text-xs text-gray-800 hidden md:table-header-group">
            <tr>
              <th class="px-6 py-4 w-10">#</th>
              <th class="px-6 py-4">Name</th>
              <th class="px-6 py-4">Email/Username</th>
              <th class="px-6 py-4">Phone</th>
              <th class="px-6 py-4">Role</th>
              <th class="px-6 py-4">Added</th>
              <th class="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="isLoading">
              <td colspan="7" class="py-8">
                <div class="flex justify-center items-center">
                  <DataLoadingSpinner />
                </div>
              </td>
            </tr>

            <tr
              v-for="(user, index) in filteredUsers"
              :key="user.id"
              class="block md:table-row border-t md:border-0 md:hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
              v-else
            >
              <td class="px-6 py-4 block md:table-cell text-gray-400 text-xs font-mono">{{ (currentPage - 1) * perPage + index + 1 }}</td>
              <td class="px-6 py-4 block md:table-cell font-medium">{{ user.firstname }} {{ user.lastname }}</td>
              <td class="px-6 py-4 block md:table-cell">{{ user.email }}</td>
              <td class="px-6 py-4 block md:table-cell">{{ user.phone }}</td>
              <td class="px-6 py-4 block md:table-cell">
                <span class="inline-block px-2 py-0.5 text-xs bg-blue-50 text-blue-700 rounded-full border border-blue-200">{{ user.role }}</span>
              </td>
              <td class="px-6 py-4 block md:table-cell text-gray-500 text-xs">
                <span :title="formatFullDate(user.created_at)">{{ formatRelativeDate(user.created_at) }}</span>
              </td>
              <td class="px-6 py-4 block md:table-cell text-left md:text-right">
                <div class="flex justify-start md:justify-end">
                  <button
                    type="button"
                    @click.stop="toggleRowMenu(user, $event)"
                    class="p-1.5 rounded-lg text-gray-500 hover:text-[#0095B6] hover:bg-gray-100"
                    title="Actions"
                  >
                    <EllipsisVerticalIcon class="w-5 h-5" />
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="!isLoading && filteredUsers.length === 0">
              <td colspan="7" class="text-center px-6 py-4 text-gray-400">No users found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex flex-col md:flex-row md:items-center justify-between mt-4 gap-4 text-sm text-gray-600">
        <div class="flex items-center space-x-2">
          <label for="perPage" class="text-sm">Show</label>
          <select
            id="perPage"
            v-model="perPage"
            class="border border-gray-300 rounded-md px-2 py-1 focus:outline-none focus:ring-1 focus:ring-[#0095B6]"
          >
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
          </select>
        </div>
        <div class="text-center flex-1 md:flex-none">Page {{ currentPage }} of {{ totalPages }}</div>
        <div class="flex justify-end items-center space-x-2">
          <button
            :disabled="currentPage === 1"
            @click="currentPage--"
            class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            :disabled="currentPage === totalPages"
            @click="currentPage++"
            class="px-3 py-1 rounded-md border border-gray-300 hover:bg-gray-100 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>

      <!-- Row actions menu — teleported to <body> so it isn't clipped by the
           table's rounded-corner overflow-hidden, and positioned against the
           trigger button's own coordinates. -->
      <Teleport to="body">
        <div v-if="menuUser"
          :style="{ position: 'fixed', top: menuPosition.top + 'px', left: menuPosition.left + 'px' }"
          class="w-52 bg-white border border-gray-200 rounded-xl shadow-xl z-50 py-1.5 overflow-hidden">
          <router-link v-if="canViewUser"
            :to="{ name: 'AdminUserPerspective', params: { id: menuUser.id } }"
            @click="closeRowMenu"
            class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            View as user
          </router-link>
          <router-link v-if="canViewUser"
            :to="{ name: 'User', params: { id: menuUser.id } }"
            @click="closeRowMenu"
            class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
            <EyeIcon class="w-4 h-4 flex-shrink-0" />
            View admin details
          </router-link>
          <router-link v-if="canEditUser"
            :to="{ name: 'EditUser', params: { id: menuUser.id } }"
            @click="closeRowMenu"
            class="flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
            <PencilSquareIcon class="w-4 h-4 flex-shrink-0" />
            Edit
          </router-link>
          <button v-if="canAddUser" type="button"
            @click="openLinkModal(menuUser); closeRowMenu()"
            class="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 text-left">
            <CalendarIcon class="w-4 h-4 flex-shrink-0" />
            Link to Event
          </button>
          <button v-if="canDeleteUser" type="button"
            @click="confirmDelete(menuUser); closeRowMenu()"
            class="w-full flex items-center gap-2.5 px-4 py-2 text-sm text-red-600 hover:bg-red-50 text-left border-t border-gray-100 mt-1">
            <TrashIcon class="w-4 h-4 flex-shrink-0" />
            Delete
          </button>
        </div>
      </Teleport>

      <!-- Delete Modal -->
      <DeleteConfirmationModal
        :show="showDeleteModal"
        :itemName="selectedUser?.firstname + ' ' + selectedUser?.lastname"
        :loading="deleting"
        @cancel="showDeleteModal = false"
        @confirm="deleteUser"
      />

      <!-- Link to Event Modal -->
      <div v-if="showLinkModal"
        class="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4"
        @click.self="closeLinkModal">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md flex flex-col max-h-[92vh]">
          <div class="flex items-center justify-between px-5 py-4 border-b border-gray-100 flex-shrink-0">
            <div>
              <p class="font-bold text-gray-800 text-sm">Link to Event</p>
              <p class="text-xs text-gray-400">Register {{ linkUser?.firstname }} {{ linkUser?.lastname }} for an event</p>
            </div>
            <button @click="closeLinkModal" class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
          <div class="p-5 space-y-4 overflow-y-auto flex-1">
            <div>
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">Event *</label>
              <select v-model="linkForm.event_id"
                class="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]">
                <option :value="null" disabled>{{ loadingLinkEvents ? 'Loading events…' : 'Select an event…' }}</option>
                <option v-for="ev in linkEvents" :key="ev.id" :value="ev.id">{{ ev.event }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-500 uppercase tracking-widest mb-1">Participation Role *</label>
              <select v-model="linkForm.participation_role"
                class="w-full border border-gray-300 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]">
                <option value="" disabled>Select a role…</option>
                <option v-for="role in PARTICIPATION_ROLES" :key="role.value" :value="role.value">{{ role.label }}</option>
              </select>
            </div>
            <label class="flex items-center gap-3 cursor-pointer p-3 rounded-xl bg-gray-50 border border-gray-200 select-none">
              <input type="checkbox" v-model="linkForm.send_invitation" class="w-4 h-4 accent-[#0095B6] rounded" />
              <div>
                <p class="text-sm font-semibold text-gray-700">Send invitation email</p>
                <p class="text-xs text-gray-400 mt-0.5">Email the participant their login details and event information.</p>
              </div>
            </label>
            <div v-if="linkError" class="flex items-start gap-2 p-3 rounded-xl text-sm text-red-700 bg-red-50 border border-red-200">❌ {{ linkError }}</div>
            <div v-if="linkSuccess" class="flex items-start gap-2 p-3 rounded-xl text-sm text-green-700 bg-green-50 border border-green-200">✅ {{ linkSuccess }}</div>
          </div>
          <div class="flex items-center justify-end gap-3 px-5 py-4 border-t border-gray-100 flex-shrink-0">
            <button @click="closeLinkModal"
              class="px-4 py-2 text-sm border border-gray-200 rounded-xl text-gray-600 hover:bg-gray-50 transition font-medium">Cancel</button>
            <button @click="submitLinkToEvent"
              :disabled="linking || !linkForm.event_id || !linkForm.participation_role"
              class="inline-flex items-center gap-2 px-5 py-2 text-sm font-semibold text-white rounded-xl transition hover:opacity-90 disabled:opacity-50 bg-bondi-blue">
              {{ linking ? 'Adding…' : 'Add to Event' }}
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { EyeIcon, PencilSquareIcon, TrashIcon, CalendarIcon, EllipsisVerticalIcon } from "@heroicons/vue/24/outline";
import AdminBar from "@/components/common/AdminBar.vue";
import api from "@/plugins/axios";
import DeleteConfirmationModal from "@/components/common/DeleteConfirmationModal.vue";
import { debounce } from "lodash";
import DataLoadingSpinner from "@/components/common/DataLoadingSpinner.vue";
import { PARTICIPATION_ROLES } from "@/constants/participationRoles";

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();
const search = ref('');
const debouncedSearch = ref('');
const currentPage = ref(1);
const perPage = ref(10);
const totalPages = ref(1);
const users = ref([]);
const isLoading = ref(false);
const deleting = ref(false);
const showDeleteModal = ref(false);
const selectedUser = ref(null);
const successMessage = ref("");

// Show a one-time success banner after redirecting back from Add User,
// then strip the query param so it doesn't reappear on refresh/back.
if (route.query.added) {
  successMessage.value = String(route.query.added);
  router.replace({ name: "Users" });
  setTimeout(() => (successMessage.value = ""), 6000);
}

function formatRelativeDate(iso) {
  if (!iso) return "—";
  const date = new Date(iso);
  const diffMs = Date.now() - date.getTime();
  const diffMin = Math.round(diffMs / 60000);
  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.round(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.round(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d ago`;
  return date.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function formatFullDate(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleString(undefined, {
    year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
  });
}

const updateDebouncedSearch = debounce((val) => {
  debouncedSearch.value = val.trim();
  currentPage.value = 1;
}, 300);

watch(search, updateDebouncedSearch);
watch(perPage, () => (currentPage.value = 1));

const fetchUsers = async () => {
  isLoading.value = true;
  try {
    const page = currentPage.value;
    const limit = perPage.value;
    const skip = (page - 1) * limit;
    const response = await api.get("/users/", {
      params: { skip, limit, search: debouncedSearch.value },
    });
    users.value = response.data.data;
    totalPages.value = response.data.pages;
  } catch (error) {
    console.error("Error fetching users:", error.response?.data || error.message);
  } finally {
    isLoading.value = false;
  }
};

const confirmDelete = (user) => {
  selectedUser.value = user;
  showDeleteModal.value = true;
};

const deleteUser = async () => {
  deleting.value = true;
  try {
    await api.delete(`/users/${selectedUser.value.id}`);
    showDeleteModal.value = false;
    selectedUser.value = null;
    fetchUsers();
  } catch (error) {
    console.error("Error deleting user:", error.response?.data || error.message);
  } finally {
    deleting.value = false;
  }
};

watch([currentPage, perPage, debouncedSearch], fetchUsers);
onMounted(fetchUsers);

const filteredUsers = computed(() => users.value);

const canAddUser = computed(() => auth.hasPermission("ADD_USER"));
const canViewUser = computed(() => auth.hasPermission("VIEW_USER"));
const canEditUser = computed(() => auth.hasPermission("UPDATE_USER"));
const canDeleteUser = computed(() => auth.hasPermission("DELETE_USER"));

// ── Row actions menu — a single "⋮" button per row instead of a row of
// icons; teleported to <body> and positioned off the trigger button so it
// isn't clipped by the table's rounded-corner overflow-hidden. ─────────────
const menuUser = ref(null);
const menuPosition = ref({ top: 0, left: 0 });
const MENU_WIDTH = 208; // matches w-52

function toggleRowMenu(user, event) {
  if (menuUser.value?.id === user.id) {
    closeRowMenu();
    return;
  }
  const rect = event.currentTarget.getBoundingClientRect();
  menuPosition.value = {
    top: rect.bottom + 4,
    left: Math.max(8, rect.right - MENU_WIDTH),
  };
  menuUser.value = user;
}

function closeRowMenu() {
  menuUser.value = null;
}

function handleWindowInteraction() {
  if (menuUser.value) closeRowMenu();
}

onMounted(() => {
  window.addEventListener("click", handleWindowInteraction);
  window.addEventListener("scroll", handleWindowInteraction, true);
  window.addEventListener("resize", handleWindowInteraction);
});
onUnmounted(() => {
  window.removeEventListener("click", handleWindowInteraction);
  window.removeEventListener("scroll", handleWindowInteraction, true);
  window.removeEventListener("resize", handleWindowInteraction);
});

// ── Link to Event modal ──────────────────────────────────────────────────
const showLinkModal = ref(false);
const linkUser = ref(null);
const linkEvents = ref([]);
const loadingLinkEvents = ref(false);
const linkForm = ref({ event_id: null, participation_role: "", send_invitation: true });
const linking = ref(false);
const linkError = ref("");
const linkSuccess = ref("");

async function openLinkModal(user) {
  linkUser.value = user;
  linkForm.value = { event_id: null, participation_role: "", send_invitation: true };
  linkError.value = "";
  linkSuccess.value = "";
  showLinkModal.value = true;
  loadingLinkEvents.value = true;
  try {
    const res = await api.get("/events/", { params: { limit: 100 } });
    linkEvents.value = res.data?.data || [];
  } catch (error) {
    console.error("Failed to load events for link modal:", error.response?.data || error.message);
  } finally {
    loadingLinkEvents.value = false;
  }
}

function closeLinkModal() {
  showLinkModal.value = false;
  linkUser.value = null;
}

async function submitLinkToEvent() {
  if (!linkForm.value.event_id || !linkForm.value.participation_role || !linkUser.value) return;
  linking.value = true;
  linkError.value = "";
  linkSuccess.value = "";
  try {
    const res = await api.post(`/events/${linkForm.value.event_id}/admin-add-participant`, {
      email: linkUser.value.email,
      firstname: linkUser.value.firstname,
      lastname: linkUser.value.lastname,
      participation_role: linkForm.value.participation_role,
      send_invitation: linkForm.value.send_invitation,
    });
    linkSuccess.value = res.data.message || "Added to event successfully.";
    setTimeout(() => closeLinkModal(), 2000);
  } catch (error) {
    linkError.value = error.response?.data?.detail || "Failed to add participant to event.";
  } finally {
    linking.value = false;
  }
}
</script>
