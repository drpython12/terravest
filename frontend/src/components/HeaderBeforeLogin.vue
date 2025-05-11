<template>
  <header class="header w-full">
    <div class="container header-container mx-auto flex items-center justify-between">
      <router-link to="/" class="flex items-center logo-container">
        <span class="logo-text">TerraVest</span>
      </router-link>
      <nav class="nav flex items-center gap-6">
        <a href="#" aria-label="Features">Features</a>
        <a href="#" aria-label="About">About</a>
        <a href="#" aria-label="Contact">Contact</a>
        <router-link to="/login" aria-label="Account">Account</router-link>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderBeforeLogin',
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