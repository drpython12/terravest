<template>
  <div class="portfolio-container">
    <div v-if="esgData.length > 0" class="esg-cards">
      <div v-for="company in esgData" :key="company.id" class="esg-card">
        <h2 class="company-name">{{ company.company_name }} ({{ company.symbol }})</h2>
        <div class="esg-section">
          <h3 class="section-title">
            <span class="environment-icon">🟣</span> Environment
            <span class="score">{{ company.environmental }}</span>
          </h3>
          <ul class="score-list">
            <li>Emissions: {{ company.emissions }}</li>
            <li>Resource Use: {{ company.resource_use }}</li>
            <li>Innovation: {{ company.innovation }}</li>
          </ul>
        </div>
        <div class="esg-section">
          <h3 class="section-title">
            <span class="social-icon">🟠</span> Social
            <span class="score">{{ company.social }}</span>
          </h3>
          <ul class="score-list">
            <li>Human Rights: {{ company.human_rights }}</li>
            <li>Product Responsibility: {{ company.product_responsibility }}</li>
            <li>Workforce: {{ company.workforce }}</li>
            <li>Community: {{ company.community }}</li>
          </ul>
        </div>
        <div class="esg-section">
          <h3 class="section-title">
            <span class="governance-icon">🟢</span> Governance
            <span class="score">{{ company.governance }}</span>
          </h3>
          <ul class="score-list">
            <li>Management: {{ company.management }}</li>
            <li>Shareholders: {{ company.shareholders }}</li>
            <li>CSR Strategy: {{ company.csr_strategy }}</li>
          </ul>
        </div>
      </div>
    </div>
    <p v-else>No ESG data available for your portfolio companies.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "../axiosConfig";

const esgData = ref([]);

const loadESGData = async () => {
  try {
    const response = await axiosInstance.get("/get-esg-data/");
    esgData.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Failed to fetch ESG data:", error);
  }
};

onMounted(loadESGData);
</script>

<style scoped>
/* Container styling */
.portfolio-container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 90%;
  max-width: 1200px;
  margin: auto;
  margin-top: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* ESG Cards Layout */
.esg-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.esg-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.company-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #333;
}

/* ESG Section Styling */
.esg-section {
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.environment-icon {
  color: #6a1b9a; /* Purple */
}

.social-icon {
  color: #ff9800; /* Orange */
}

.governance-icon {
  color: #4caf50; /* Green */
}

.score {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

/* Score List Styling */
.score-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.score-list li {
  font-size: 14px;
  color: #555;
  margin-bottom: 5px;
}
</style>