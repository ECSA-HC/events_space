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
    impersonating: false,
    adminSession: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    hasPermission: (state) => (code) =>
      state.permissions.some((p) => p.permission_code === code),
    isImpersonating: (state) => state.impersonating,
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
        this.needsRefresh = true;
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.permissions = [];
      this.needsRefresh = false;
      this.impersonating = false;
      this.adminSession = null;
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
        if (!this.impersonating) {
          localStorage.setItem("user", JSON.stringify(res.data.user));
          localStorage.setItem("permissions", JSON.stringify(res.data.permissions));
        }
      } catch (e) {
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

    startImpersonation({ user, token, permissions }) {
      // Save real admin session
      this.adminSession = {
        user: this.user,
        token: this.token,
        permissions: this.permissions,
        mustChangePassword: this.mustChangePassword,
      };
      // Swap in the target user's credentials
      this.user = user;
      this.token = token;
      this.permissions = permissions;
      this.mustChangePassword = false;
      this.impersonating = true;
      this.needsRefresh = false;
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    },

    stopImpersonation() {
      if (!this.adminSession) return;
      const s = this.adminSession;
      this.user = s.user;
      this.token = s.token;
      this.permissions = s.permissions;
      this.mustChangePassword = s.mustChangePassword;
      this.adminSession = null;
      this.impersonating = false;
      this.needsRefresh = false;
      axios.defaults.headers.common["Authorization"] = `Bearer ${s.token}`;
    },
  },
});
