// src/plugins/axios.js
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

axios.defaults.baseURL = "http://localhost:8000";

// Automatically attach Authorization header
axios.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;
  }
  return config;
});

// Handle token refresh on 401, but only if token exists
axios.interceptors.response.use(
  (res) => res,
  async (error) => {
    const auth = useAuthStore();

    // ✅ Only refresh if user is logged in and request is not login itself
    if (
      error.response &&
      error.response.status === 401 &&
      auth.token &&
      !error.config._retry &&
      !error.config.url.includes("/auth/login")
    ) {
      error.config._retry = true;
      try {
        await auth.refreshToken();
        error.config.headers["Authorization"] = `Bearer ${auth.token}`;
        return axios(error.config);
      } catch {
        auth.logout();
      }
    }

    return Promise.reject(error);
  }
);

export default axios;
// // src/plugins/axios.js
// import axios from "axios";
// import { useAuthStore } from "@/stores/auth";

// axios.defaults.baseURL = "http://localhost:8000";

// // Automatically attach Authorization header
// axios.interceptors.request.use((config) => {
//   const auth = useAuthStore();
//   if (auth.token) {
//     config.headers.Authorization = `Bearer ${auth.token}`;
//   }
//   return config;
// });

// // Handle token refresh on 401
// axios.interceptors.response.use(
//   (res) => res,
//   async (error) => {
//     const auth = useAuthStore();
//     if (error.response && error.response.status === 401) {
//       try {
//         await auth.refreshToken();
//         error.config.headers["Authorization"] = `Bearer ${auth.token}`;
//         return axios(error.config);
//       } catch {
//         auth.logout();
//       }
//     }
//     return Promise.reject(error);
//   }
// );

// export default axios;
