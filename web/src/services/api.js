// src/plugins/axios.js
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

axios.defaults.baseURL = "http://localhost:8000";

// Axios interceptor for handling expired tokens
axios.interceptors.response.use(
  (res) => res,
  async (error) => {
    const auth = useAuthStore();
    if (error.response && error.response.status === 401) {
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
