<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="container header-container">
        <router-link to="/" class="flex items-center logo-container">
          <span class="logo-text">TerraVest</span>
        </router-link>
        <nav class="nav">
          <a href="#" aria-label="Features">Features</a>
          <a href="#" aria-label="About">About</a>
          <a href="#" aria-label="Contact">Contact</a>
          <router-link to="/account" aria-label="Account">Account</router-link>
        </nav>
      </div>
    </header>

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
import axios from 'axios';
import logo from '@/assets/terravest-logo.png';

export default {
  name: 'App',
  data() {
    return {
      logo,
      appData: null,
    };
  },
  async created() {
    try {
      const response = await axios.get('/api/app-data');
      this.appData = response.data;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style>
</style>