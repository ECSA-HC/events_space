<template>
  <div class="flex-1 flex flex-col max-w-7xl w-full mx-auto overflow-hidden">
    <!-- Admin Bar -->
<!-- Admin Bar -->
<AdminBar title="Users">
  <a href="#" class="text-sm text-blue-600 hover:underline">Users</a>
</AdminBar>

<!-- Page Title -->
<div class="px-6 pt-4 pb-2">
  <h1 class="text-xl font-bold text-gray-800">Users</h1>
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
          <th class="px-6 py-4">Name</th>
          <th class="px-6 py-4">Email/Username</th>
          <th class="px-6 py-4">Phone</th>
          <th class="px-6 py-4 text-right">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="isLoading">
          <td colspan="3" class="py-8">
            <div class="flex justify-center items-center">
              <DataLoadingSpinner />
            </div>
          </td>
        </tr>

        <tr
          v-for="user in filteredUsers"
          :key="user.id"
          class="block md:table-row border-t md:border-0 md:hover:bg-gray-50 even:bg-gray-50 odd:bg-white"
          v-else
        >
          <td class="px-6 py-4 block md:table-cell">{{ user.firstname }} {{ user.lastname }}</td>
          <td class="px-6 py-4 block md:table-cell">{{ user.email }}</td>
          <td class="px-6 py-4 block md:table-cell">{{ user.phone }}</td>
          <td class="px-6 py-4 block md:table-cell text-left md:text-right">
            <div class="flex items-center space-x-3 justify-start md:justify-end">
              <router-link
                v-if="canViewUser"
                :to="{ name: 'User', params: { id: user.id } }"
                class="text-gray-500 hover:text-blue-600"
                title="View"
              >
                <EyeIcon class="w-6 h-6" />
              </router-link>
              <router-link
                v-if="canEditUser"
                :to="{ name: 'EditUser', params: { id: user.id } }"
                class="text-gray-500 hover:text-blue-600"
                title="Edit"
              >
                <PencilSquareIcon class="w-6 h-6" />
              </router-link>
              <ActionIcon
                :can="canDeleteUser"
                :icon="TrashIcon"
                label="Delete"
                colorClass="text-gray-500 hover:text-blue-600"
                @click="confirmDelete(user)"
              />
            </div>
          </td>
        </tr>

        <tr v-if="!isLoading && filteredUsers.length === 0">
          <td colspan="3" class="text-center px-6 py-4 text-gray-400">No users found.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Delete Modal -->
  <DeleteConfirmationModal
    :show="showDeleteModal"
    :itemName="selectedUser?.name"
    :loading="deleting"
    @cancel="showDeleteModal = false"
    @confirm="deleteUser"
  />
</main>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { EyeIcon, PencilSquareIcon, TrashIcon } from "@heroicons/vue/24/outline";
import AdminBar from "@/components/common/AdminBar.vue";
import api from "@/plugins/axios";
import ActionIcon from '@/components/common/ActionIcon.vue';
import DeleteConfirmationModal from '@/components/common/DeleteConfirmationModal.vue';
import { debounce } from 'lodash';
import DataLoadingSpinner from '@/components/common/DataLoadingSpinner.vue'

const auth = useAuthStore();
const search = ref('');
const debouncedSearch = ref('');
const currentPage = ref(1);
const perPage = ref(5);
const totalPages = ref(1);
const users = ref([]);
const isLoading = ref(false);
const deleting = ref(false);
const showDeleteModal = ref(false);
const selectedUser = ref(null);

const updateDebouncedSearch = debounce((val) => {
  debouncedSearch.value = val;
  currentPage.value = 1;
}, 300);
watch(search, updateDebouncedSearch);
watch(perPage, () => (currentPage.value = 1));

const fetchUsers = async () => {
  isLoading.value = true;
  try {
    const page = Number(currentPage.value);
    const limit = Number(perPage.value);
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
</script>
