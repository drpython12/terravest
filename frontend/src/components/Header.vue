<template>
  <header class="header">
    <div class="container header-container">
      <router-link to="/" class="flex items-center logo-container">
        <span class="logo-text">TerraVest</span>
      </router-link>
      <nav class="nav">
        <a href="#" aria-label="Features">Features</a>
        <a href="#" aria-label="About">About</a>
        <a href="#" aria-label="Contact">Contact</a>
        <router-link to="/dashboard" v-if="isLoggedIn">Dashboard</router-link>
        <a href="#" @click="logout" v-if="isLoggedIn">Logout</a>
        <router-link :to="accountLink" aria-label="Account">Account</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLoggedIn: false,
    };
  },
  computed: {
    accountLink() {
      return this.isLoggedIn ? '/account' : '/login';
    }
  },
  async created() {
    try {
      const response = await axios.get('/api/app-data');
      this.isLoggedIn = response.data.isLoggedIn; // Assuming the API returns the login status
    } catch (error) {
      console.error(error);
    }
  },
  methods: {
    logout() {
      axios.post('/account/logout/')
        .then(() => {
          this.isLoggedIn = false;
          window.location.href = '/';
        })
        .catch(error => {
          console.error("Logout error:", error);
        });
    }
  }
};
</script>

<style scoped>
/* Header Styles */
.header {
  background: #fff;
  border-bottom: 1px solid #eaeaea;
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}

/* Logo Container: Image and Text Side by Side */
.logo-container {
  display: flex;
  align-items: center;
}
.logo-text {
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
  margin-left: 8px; /* Space between image and text */
}

/* Navigation */
.nav {
  display: flex;
  gap: 30px;
}
.nav a {
  text-decoration: none;
  color: #555;
  font-weight: 500;
  transition: color 0.3s ease;
}
.nav a:hover {
  color: #000;
}
</style>
