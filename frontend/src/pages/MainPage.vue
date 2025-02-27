<template>
  <div>
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

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MainPage',
});
</script>

<style scoped>
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