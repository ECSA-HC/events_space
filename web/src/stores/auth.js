import { defineStore } from "pinia";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
    permissions: [],
    refreshTimeout: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    hasPermission: (state) => (code) =>
      state.permissions.some((p) => p.permission_code === code),
  },
  actions: {
    setAuth({ user, token, permissions }) {
      this.user = user;
      this.token = token;
      this.permissions = permissions;
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("permissions", JSON.stringify(permissions));
    },

    loadFromStorage() {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");
      const permissions = localStorage.getItem("permissions");
      if (token && user && permissions) {
        this.setAuth({
          user: JSON.parse(user),
          token,
          permissions: JSON.parse(permissions),
        });
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.permissions = [];
      localStorage.clear();
      delete axios.defaults.headers.common["Authorization"];
    },

    async refreshToken() {
      try {
        const res = await axios.post(`${API_BASE_URL}/auth/refresh`);
        this.token = res.data.access_token;
        axios.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;
        localStorage.setItem("token", this.token);
      } catch (e) {
        this.logout();
      }
    },
  },
});
