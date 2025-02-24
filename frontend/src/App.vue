<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="container header-container">
        <router-link to="/" class="flex items-center logo-container">
          <span class="logo-text">TerraVest</span>
        </router-link>
        <nav class="nav">
          <a href="#">Features</a>
          <a href="#">About</a>
          <a href="#">Contact</a>
          <router-link to="/account">Account</router-link>
        </nav>
      </div>
    </header>

    <!-- Routed Content -->
    <router-view />

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer-container">
        <p>&copy; 2024 TerraVest. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import logo from '@/assets/terravest-logo.png';

export default {
  name: 'App',
  data() {
    return {
      logo,
    };
  },
};
</script>

<style scoped>
/* You can add header/footer styling here if needed */
</style>