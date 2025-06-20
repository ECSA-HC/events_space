import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

// Layouts
import DefaultLayout from "@/layouts/DefaultLayout.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";

// Public Pages
import HomeView from "@/pages/public/HomeView.vue";
import EventsView from "@/pages/public/EventsView.vue";
import EventView from "@/pages/public/EventView.vue";
import LoginView from "@/pages/public/LoginView.vue";
import RegisterView from "@/pages/public/RegisterView.vue";

// Admin Pages
import DashboardView from "@/pages/admin/DashboardView.vue";
import ClustersView from "@/pages/admin/clusters/ClustersView.vue";
import AddClusterView from "@/pages/admin/clusters/AddClusterView.vue";
import ClusterView from "@/pages/admin/clusters/ClusterView.vue";
import EditClusterView from "@/pages/admin/clusters/EditClusterView.vue";
import AdminEventsView from "@/pages/admin/events/EventsView.vue";
import AddEventView from "@/pages/admin/events/AddEventView.vue";
import EditEventView from "@/pages/admin/events/EditEventView.vue";
import MyEventsView from "@/pages/admin/events/MyEventsView.vue";
import AdminEventView from "@/pages/admin/events/AdminEventView.vue";
import UsersView from "@/pages/admin/users/UsersView.vue";
import AddUserView from "@/pages/admin/users/AddUserView.vue";
import UserView from "@/pages/admin/users/UserView.vue";
import EditUserView from "@/pages/admin/users/EditUserView.vue";
import RolesView from "@/pages/admin/roles/RolesView.vue";
import AddRoleView from "@/pages/admin/roles/AddRoleView.vue";
import RoleView from "@/pages/admin/roles/RoleView.vue";
import EditRoleView from "@/pages/admin/roles/EditRoleView.vue";
import SettingsView from "@/pages/admin/settings/SettingsView.vue";

// Error Pages
import ForbiddenView from "@/pages/errors/ForbiddenView.vue";

const routes = [
  {
    path: "/",
    component: DefaultLayout,
    children: [
      { path: "", name: "Home", component: HomeView },
      { path: "events", name: "Events", component: EventsView },
      { path: "event/:id", name: "Event", component: EventView },
      { path: "login", name: "Login", component: LoginView },
      { path: "register/:id", name: "Register", component: RegisterView },
    ],
  },
  {
    path: "/admin",
    component: AdminLayout,
    children: [
      {
        path: "dashboard",
        name: "AdminDashboard",
        component: DashboardView,
        meta: { requiresAuth: true },
      },
      {
        path: "clusters",
        name: "Clusters",
        component: ClustersView,
        meta: { requiresAuth: true, permissions: ["VIEW_ORG_UNIT"] },
      },
      {
        path: "add-cluster",
        name: "AddCluster",
        component: AddClusterView,
        meta: { requiresAuth: true, permissions: ["ADD_ORG_UNIT"] },
      },
      {
        path: "cluster/:id",
        name: "Cluster",
        component: ClusterView,
        meta: { requiresAuth: true, permissions: ["VIEW_ORG_UNIT"] },
      },
      {
        path: "/clusters/:id/edit",
        name: "EditCluster",
        component: EditClusterView,
        meta: { requiresAuth: true, permissions: ["UPDATE_ORG_UNIT"] },
      },
      {
        path: "admin-events",
        name: "AdminEvents",
        component: AdminEventsView,
        meta: { requiresAuth: true },
      },
      {
        path: "my-events",
        name: "MyEvents",
        component: MyEventsView,
        meta: { requiresAuth: true },
      },
      {
        path: "add-event",
        name: "AddEvent",
        component: AddEventView,
        meta: { requiresAuth: true, permissions: ["ADD_EVENT"] },
      },
      {
        path: "admin-events/:id",
        name: "AdminEvent",
        component: AdminEventView,
        meta: { requiresAuth: true, permissions: ["VIEW_EVENT"] },
      },
      {
        path: "/admin-events/:id/edit",
        name: "EditEvent",
        component: EditEventView,
        meta: { requiresAuth: true, permissions: ["UPDATE_EVENT"] },
      },
      {
        path: "users",
        name: "Users",
        component: UsersView,
        meta: { requiresAuth: true, permissions: ["VIEW_USER"] },
      },
      {
        path: "add-user",
        name: "AddUser",
        component: AddUserView,
        meta: { requiresAuth: true, permissions: ["ADD_USER"] },
      },
      {
        path: "users/:id",
        name: "User",
        component: UserView,
        meta: { requiresAuth: true, permissions: ["VIEW_USER"] },
      },
      {
        path: "users/:id/edit",
        name: "EditUser",
        component: EditUserView,
        meta: { requiresAuth: true, permissions: ["UPDATE_USER"] },
      },
      {
        path: "roles",
        name: "Roles",
        component: RolesView,
        meta: { requiresAuth: true },
      },
      {
        path: "add-role",
        name: "AddRole",
        component: AddRoleView,
        meta: { requiresAuth: true, permissions: ["ADD_ROLE"] },
      },
      {
        path: "role/:id",
        name: "Role",
        component: RoleView,
        meta: { requiresAuth: true, permissions: ["VIEW_ROLE"] },
      },
      {
        path: "/roles/:id/edit",
        name: "EditRole",
        component: EditRoleView,
        meta: { requiresAuth: true, permissions: ["UPDATE_ROLE"] },
      },
      {
        path: "settings",
        name: "Settings",
        component: SettingsView,
        meta: { requiresAuth: true },
      },
    ],
  },
  {
    path: "/403",
    name: "Forbidden",
    component: ForbiddenView,
  },
  {
    path: "/:catchAll(.*)",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (!auth.token) auth.loadFromStorage();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next({ name: "Login" });
  }

  if (to.meta.permissions) {
    const hasPermission = to.meta.permissions.every((p) =>
      auth.hasPermission(p)
    );
    if (!hasPermission) return next({ name: "Forbidden" });
  }

  next();
});

export default router;
