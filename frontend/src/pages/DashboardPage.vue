<template>
  <div class="dashboard-container" v-if="authStore.user">
    <!-- Header Section -->
    <header class="dashboard-header">
      <h1>Welcome, {{ authStore.user.first_name }} 👋</h1>
      <p>Monitor your ESG investments, sentiment trends, and portfolio performance.</p>
    </header>

    <!-- Portfolio Summary -->
    <div class="portfolio-summary">
      <div class="summary-card">
        <h3>Total Portfolio Value</h3>
        <p v-if="!loading">${{ portfolioValue ? portfolioValue.toLocaleString() : '0' }}</p>
        <p v-else>Loading...</p>
      </div>
      <div class="summary-card">
        <h3>Overall ESG Score</h3>
        <p v-if="!loading">
          {{ !isNaN(esgScore) ? esgScore : 'No Data Available' }}{{ !isNaN(esgScore) ? '/100' : '' }}
        </p>
        <p v-else>Loading...</p>
      </div>
      <div class="summary-card">
        <h3>Portfolio Performance</h3>
        <p v-if="!loading" :class="{ positive: performanceChange >= 0, negative: performanceChange < 0 }">
          {{ performanceChange }}%
        </p>
        <p v-else>Loading...</p>
      </div>
    </div>

    <!-- ESG Charts & Market Sentiment -->
    <div class="dashboard-grid">
      <div class="chart-card">
        <h2>ESG Category Breakdown</h2>
        <ESGPieChart :data="esgBreakdown" />
      </div>
      <div class="chart-card">
        <h2>ESG Score Trends</h2>
        <ESGLineChart :data="esgTrends" />
      </div>
    </div>

    <!-- Top Holdings Section -->
    <div class="top-holdings">
      <h2>Top Portfolio Holdings</h2>
      <TopPortfolioHoldings />
    </div>

    <!-- ESG Market News -->
    <ESGNewsFeed />

    <!-- Investment Suggestions -->
    <div class="insights-section">
      <h2>Investment Insights</h2>
      <InvestmentSuggestions :portfolio="portfolio" />
    </div>
  </div>
  <div v-else>
    <p>Loading user data...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/useAuthStore";
import ESGPieChart from "@/components/ESGPieChart.vue";
import ESGLineChart from "@/components/ESGLineChart.vue";
import ESGNewsFeed from "@/components/ESGNewsFeed.vue";
import InvestmentSuggestions from "@/components/InvestmentSuggestions.vue";
import TopPortfolioHoldings from "@/components/TopPortfolioHoldings.vue";
import axios from "axios";

const authStore = useAuthStore();
const portfolioValue = ref(0);
const esgScore = ref(null); // Set to null initially
const performanceChange = ref(0);
const esgBreakdown = ref({});
const esgTrends = ref({
  ESGScore: [],
  EnvironmentalScore: [],
  SocialScore: [],
  GovernanceScore: [],
});
const topHoldings = ref([]);
const loading = ref(true);
const portfolio = ref([]); // Define the portfolio property

const loadDashboardData = async () => {
  try {
    const response = await axios.get("/api/dashboard/");
    console.log("API Response:", response.data); // Log the API response for debugging
    portfolioValue.value = response.data.portfolio_value;
    esgScore.value = response.data.overall_esg_score; // Ensure this value is being set
    performanceChange.value = response.data.portfolio_performance_change;
    esgBreakdown.value = response.data.esg_breakdown;
    esgTrends.value = response.data.esg_trends;
    topHoldings.value = response.data.top_holdings;
    portfolio.value = response.data.top_holdings; // Populate the portfolio property
  } catch (error) {
    console.error("Error loading dashboard data:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(loadDashboardData);
</script>

<style scoped>
/* Apple-Style Dashboard */
.dashboard-container {
  max-width: 1200px;
  margin: auto;
  padding: 40px 20px;
  background: #f9f9f9;
}

/* Header Styling */
.dashboard-header {
  text-align: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

.dashboard-header p {
  font-size: 1.1rem;
  color: #666;
}

/* Portfolio Summary */
.portfolio-summary {
  display: flex;
  justify-content: space-around;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: transform 0.3s ease;
}

.summary-card:hover {
  transform: translateY(-5px);
}

/* ESG Charts */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-5px);
}

/* Top Holdings */
.top-holdings {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
  margin-bottom: 30px;
}

.top-holdings ul {
  list-style: none;
  padding: 0;
}

.top-holdings li {
  padding: 10px;
  font-size: 1.1rem;
  border-bottom: 1px solid #eaeaea;
}

/* Investment Insights */
.insights-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
  margin-bottom: 30px;
}

.insights-section:hover {
  transform: translateY(-5px);
}

/* Positive/Negative Colors */
.positive {
  color: green;
}

.negative {
  color: red;
}

/* Responsive */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>