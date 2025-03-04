<template>
  <div id="app">
    <!-- Header -->
    <Header />

    <!-- Routed Content -->
    <router-view />

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer-container">
        <p>&copy; 2025 TerraVest. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { useAuthStore } from './store/useAuthStore';
import Header from './components/Header.vue';

export default {
  name: 'App',
  components: {
    Header,
  },
  async created() {
    const authStore = useAuthStore();
    await authStore.fetchUser();
  },
};
</script>