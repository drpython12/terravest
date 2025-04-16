<template>
  <div id="app">
    <!-- Conditionally Render Headers -->
    <HeaderBeforeLogin v-if="!isLoggedIn" />
    <HeaderAfterLogin v-else />

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
import HeaderBeforeLogin from './components/HeaderBeforeLogin.vue';
import HeaderAfterLogin from './components/HeaderAfterLogin.vue';
import { computed } from 'vue';

export default {
  name: 'App',
  components: {
    HeaderBeforeLogin,
    HeaderAfterLogin,
  },
  setup() {
    const authStore = useAuthStore();
    const isLoggedIn = computed(() => authStore.isLoggedIn);

    return {
      isLoggedIn,
    };
  },
  async created() {
    const authStore = useAuthStore();
    await authStore.fetchUser();
  },
};
</script>