import { defineStore } from "pinia";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: null,
    permissions: [],
    mustChangePassword: false,
    refreshTimeout: null,
    needsRefresh: false,
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
      this.mustChangePassword = user?.must_change_password ?? false;
      this.needsRefresh = false;
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("permissions", JSON.stringify(permissions));
    },

    loadFromStorage() {
      const token = localStorage.getItem("token");
      const user = localStorage.getItem("user");
      const permissions = localStorage.getItem("permissions");
      if (token && user) {
        this.user = JSON.parse(user);
        this.token = token;
        this.permissions = permissions ? JSON.parse(permissions) : [];
        this.mustChangePassword = this.user?.must_change_password ?? false;
        this.needsRefresh = true; // stale — refresh on next navigation
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.permissions = [];
      this.needsRefresh = false;
      localStorage.clear();
      delete axios.defaults.headers.common["Authorization"];
    },

    async refreshPermissions() {
      if (!this.token) return;
      try {
        const res = await axios.get("/auth/me");
        this.user = res.data.user;
        this.permissions = res.data.permissions;
        this.mustChangePassword = res.data.user?.must_change_password ?? false;
        this.needsRefresh = false;
        localStorage.setItem("user", JSON.stringify(res.data.user));
        localStorage.setItem("permissions", JSON.stringify(res.data.permissions));
      } catch (e) {
        // Token expired or invalid — log out
        this.logout();
      }
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
