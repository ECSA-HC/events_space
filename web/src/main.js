import "./assets/main.css"; // Tailwind
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import api from "./plugins/axios";
import { useAuthStore } from "@/stores/auth";

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);
app.use(router);

// Now that Pinia is installed, we can safely use stores
const auth = useAuthStore();
auth.loadFromStorage(); // If async, consider awaiting or handling promise

// Attach Axios instance globally (optional, better to import/use api directly)
app.config.globalProperties.$axios = api;

app.mount("#app");
