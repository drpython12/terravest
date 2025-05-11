<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-12 text-gray-900">
    <!-- Header Section -->
    <header class="text-center space-y-4">
      <h1 class="text-4xl font-bold text-gray-800">
        Welcome, {{ authStore.user?.first_name || 'Guest' }} 👋
      </h1>
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

    <!-- ESG Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Radar Chart -->
      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">ESG Pillar Score Breakdown</h2>
        <RadarChart
          v-if="!loading"
          :data="{
            environmental: esgBreakdown.environmental,
            social: esgBreakdown.social,
            governance: esgBreakdown.governance
          }"
        />
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </div>

      <!-- Line Chart -->
      <div class="bg-white shadow-lg rounded-2xl p-6 hover:shadow-xl transition">
        <h2 class="text-lg font-semibold text-gray-700 mb-4">ESG Score Trends</h2>
        <LineChart
          v-if="!loading"
          :data="{
            labels: esgTrends.ESGScore.map((entry) => entry.year),
            scores: esgTrends.ESGScore.map((entry) => entry.score),
            environmentalScores: esgTrends.EnvironmentPillarScore.map((entry) => entry.score),
            socialScores: esgTrends.SocialPillarScore.map((entry) => entry.score),
            governanceScores: esgTrends.GovernancePillarScore.map((entry) => entry.score)
          }"
        />
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
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
import RadarChart from "@/components/RadarChart.vue";
import LineChart from "@/components/LineChart.vue";
import InvestmentSuggestions from "@/components/InvestmentSuggestions.vue";
import TopPortfolioHoldings from "@/components/TopPortfolioHoldings.vue";
import axios from "axios";

const authStore = useAuthStore();
const portfolioValue = ref(0);
const esgScore = ref(null);
const performanceChange = ref(0);
const esgBreakdown = ref({});
const esgTrends = ref({
  ESGScore: [],
  EnvironmentPillarScore: [],
  SocialPillarScore: [],
  GovernancePillarScore: [],
});
const loading = ref(true);

const loadDashboardData = async () => {
  try {
    const response = await axios.get("/api/dashboard/");
    portfolioValue.value = response.data.portfolio_value;
    esgScore.value = response.data.overall_esg_score;
    performanceChange.value = response.data.portfolio_performance_change;
    esgBreakdown.value = response.data.esg_breakdown;
    esgTrends.value = response.data.esg_trends;
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