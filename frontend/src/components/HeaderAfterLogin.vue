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
        <router-link to="/dashboard">Dashboard</router-link>
        <div class="dropdown">
          <button class="dropbtn">Account</button>
          <div class="dropdown-content">
            <router-link to="/account/settings">Settings</router-link>
            <a href="#" @click="logout">Logout</a>
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import { useAuthStore } from '../store/useAuthStore';
import { useRouter } from 'vue-router';

export default {
  name: 'HeaderAfterLogin',
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const logout = async () => {
      await authStore.logout();
      router.push('/login');
    };

    return {
      logout,
    };
  },
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

/* Dropdown Styles */
.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
  background-color: #fff;
  color: #555;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  color: #000;
}
</style>