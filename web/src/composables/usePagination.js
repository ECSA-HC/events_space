// src/composables/usePagination.js
import { ref, watch } from "vue";

export function usePagination(fetchDataFn, initialPerPage = 10) {
  const currentPage = ref(1);
  const perPage = ref(initialPerPage);
  const totalPages = ref(1);
  const isLoading = ref(false);
  const error = ref(null);

  const fetchData = async () => {
    isLoading.value = true;
    error.value = null;
    try {
      // skip = (page - 1) * perPage (assuming backend supports skip=0)
      const skip = (currentPage.value - 1) * perPage.value;
      const limit = perPage.value;
      const result = await fetchDataFn(skip, limit);
      totalPages.value = result.totalPages;
    } catch (err) {
      error.value = err;
    } finally {
      isLoading.value = false;
    }
  };

  // Watch changes to currentPage and perPage to refetch
  watch([currentPage, perPage], fetchData, { immediate: true });

  return {
    currentPage,
    perPage,
    totalPages,
    isLoading,
    error,
    fetchData,
  };
}
