<template>
    <div class="dashboard-container">
      <header class="dashboard-header">
        <h1>Welcome, {{ authStore.user }}!</h1>
        <p>Track your ESG investments and sentiment trends.</p>
      </header>
  
      <div class="dashboard-content">
        <!-- Left Section: Portfolio Overview -->
        <div class="portfolio-section">
          <h2>Your Portfolio</h2>
          <PortfolioTable :portfolio="portfolio" @select-company="loadCompanyDetails" />
        </div>
  
        <!-- Right Section: Sentiment & ESG Details -->
        <div class="analysis-section">
          <h2>Market Sentiment Analysis</h2>
          <SentimentGraph :company="selectedCompany" />
  
          <h2 v-if="selectedCompany">ESG Score Breakdown - {{ selectedCompany }}</h2>
          <ESGDetails v-if="selectedCompany" :company="selectedCompany" />
        </div>
      </div>
  
      <!-- AI-Generated Investment Recommendations -->
      <InvestmentSuggestions :portfolio="portfolio" />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useAuthStore } from '../store/useAuthStore';
  import PortfolioTable from "@/components/PortfolioTable.vue";
  import SentimentGraph from "@/components/SentimentGraph.vue";
  import ESGDetails from "@/components/ESGDetails.vue";
  import InvestmentSuggestions from "@/components/InvestmentSuggestions.vue";
  import axios from "axios";
  
  const authStore = useAuthStore();
  const portfolio = ref([]);
  const selectedCompany = ref(null);
  
  const loadPortfolio = async () => {
    try {
      const response = await axios.get("/api/portfolio/", { withCredentials: true });
      portfolio.value = response.data;
    } catch (error) {
      console.error("Failed to fetch portfolio:", error);
    }
  };
  
  const loadCompanyDetails = (company) => {
    selectedCompany.value = company;
  };
  
  onMounted(() => {
    loadPortfolio();
  });
  </script>
  
  <style scoped>
  .dashboard-container {
    padding: 20px;
    background-color: #f9f9f9;
  }
  
  .dashboard-header {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .dashboard-content {
    display: flex;
    gap: 20px;
  }
  
  .portfolio-section {
    width: 50%;
  }
  
  .analysis-section {
    width: 50%;
  }
  </style>  