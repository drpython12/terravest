<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <!-- Hero Section -->
    <section class="hero w-full">
      <div class="hero-container mx-auto text-center">
        <h1>Empower Your Sustainable Investments</h1>
        <p>AI-driven ESG analysis for transparent and personalized investment decisions.</p>
        <button class="cta">Get Started</button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features w-full">
      <div class="container features-container mx-auto">
        <div class="feature">
          <h2 class="feature-heading">Real-Time Insights</h2>
          <p>Live sentiment analysis and dynamic ESG scores to keep you ahead.</p>
        </div>
        <div class="feature">
          <h2 class="feature-heading">Transparent Reporting</h2>
          <p>Clear, narrative explanations that empower informed decisions.</p>
        </div>
        <div class="feature">
          <h2 class="feature-heading">Custom Recommendations</h2>
          <p>Tailored strategies to match your unique investment goals.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
    };
  },
  async created() {
    try {
      const response = await axios.get('/title');
      this.title = response.data;
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style scoped>
/* Retain existing styles */
.feature-heading {
  font-size: 1.75rem;
  color: white;
}
.features {
  background: black;
  padding: 50px 0;
  text-align: center;
}
</style>