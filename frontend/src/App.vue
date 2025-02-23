<template>
    <div id="app">
      <!-- Header -->
      <header class="header">
        <div class="container header-container">
          <router-link to="/" class="flex items-center logo-container">
            <span class="logo-text">TerraVest</span>
          </router-link>
          <nav class="nav">
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
          </nav>
        </div>
      </header>
  
      <!-- Hero Section -->
      <section class="hero">
        <div class="container hero-container">
          <h1>Empower Your Sustainable Investments</h1>
          <p>AI-driven ESG analysis for transparent and personalized investment decisions.</p>
          <button class="cta">Get Started</button>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features">
        <div class="container features-container">
          <div class="feature">
            <h2>Real-Time Insights</h2>
            <p>Live sentiment analysis and dynamic ESG scores to keep you ahead.</p>
          </div>
          <div class="feature">
            <h2>Transparent Reporting</h2>
            <p>Clear, narrative explanations that empower informed decisions.</p>
          </div>
          <div class="feature">
            <h2>Custom Recommendations</h2>
            <p>Tailored strategies to match your unique investment goals.</p>
          </div>
        </div>
      </section>
  
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