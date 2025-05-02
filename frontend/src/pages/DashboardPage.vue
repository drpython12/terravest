<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-12 text-gray-900">
    <!-- Header Section -->
    <header class="text-center space-y-4">
      <h1 class="text-4xl font-bold text-gray-800">
        Welcome, {{ authStore.user?.first_name || 'Guest' }} 👋
      </h1>
      <p class="text-lg text-gray-600"></p>
    </header>

    <!-- Portfolio Summary -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white shadow-lg rounded-2xl p-6 text-center hover:shadow-xl transition">
        <h3 class="text-lg font-semibold text-gray-700">Total Portfolio Value</h3>
        <p v-if="!loading" class="text-2xl font-bold text-gray-800">
          ${{ portfolioValue ? portfolioValue.toLocaleString() : '0' }}
        </p>
        <p v-else class="text-gray-400">Loading...</p>
      </div>
      <div class="bg-white shadow-lg rounded-2xl p-6 text-center hover:shadow-xl transition">
        <h3 class="text-lg font-semibold text-gray-700">Overall ESG Score</h3>
        <p v-if="!loading" class="text-2xl font-bold text-gray-800">
          {{ !isNaN(esgScore) ? esgScore : 'No Data Available' }}{{ !isNaN(esgScore) ? '/100' : '' }}
        </p>
        <p v-else class="text-gray-400">Loading...</p>
      </div>
      <div class="bg-white shadow-lg rounded-2xl p-6 text-center hover:shadow-xl transition">
        <h3 class="text-lg font-semibold text-gray-700">Portfolio Performance</h3>
        <p
          v-if="!loading"
          :class="[
            'text-2xl font-bold',
            performanceChange >= 0 ? 'text-green-600' : 'text-red-600'
          ]"
        >
          {{ performanceChange }}%
        </p>
        <p v-else class="text-gray-400">Loading...</p>
      </div>
    </div>

    <!-- ESG Charts & Market Sentiment -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">ESG Category Breakdown</h2>
        <ESGPieChart :data="esgBreakdown" />
      </div>
      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">ESG Score Trends</h2>
        <ESGLineChart :data="esgTrends" />
      </div>
    </div>

    <!-- Top Holdings Section -->
    <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Top Portfolio Holdings</h2>
      <TopPortfolioHoldings />
    </div>

    <!-- ESG Market News -->
    <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">ESG Market News</h2>
      <NewsFeed />
    </div>

    <!-- Investment Suggestions -->
    <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
      <h2 class="text-lg font-semibold text-gray-700 mb-4">Investment Insights</h2>
      <InvestmentSuggestions :portfolio="portfolio" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/store/useAuthStore";
import ESGPieChart from "@/components/ESGPieChart.vue";
import ESGLineChart from "@/components/ESGLineChart.vue";
import NewsFeed from "@/components/NewsFeed.vue";
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
/* Tailwind classes are used for styling; no additional CSS is required */
</style>