<template>
    <div class="max-w-7xl mx-auto px-6 py-10 space-y-8 text-gray-900">
  
      <h1 class="text-3xl font-semibold tracking-tight">Company ESG Breakdown</h1>
      <h1 class="text-3xl font-bold text-red-600 underline">Tailwind is working?</h1>

      <!-- ESG Pillar Score Breakdown -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">ESG Pillar Score Breakdown</h2>
        <div class="h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          [Radar Chart: E / S / G Pillars]
        </div>
      </section>
  
      <!-- ESG Score Over Time -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">ESG Score Over Time</h2>
        <div class="h-64 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          [Line Chart: ESG score history]
        </div>
      </section>
  
      <!-- KPI-Level Drilldown -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">KPI-Level Drilldown</h2>
        <ul class="space-y-2">
          <li class="flex justify-between text-gray-700">
            <span>Carbon Emissions</span><span class="font-medium">65</span>
          </li>
          <li class="flex justify-between text-gray-700">
            <span>Board Diversity</span><span class="font-medium">80</span>
          </li>
          <li class="flex justify-between text-gray-700">
            <span>Employee Turnover</span><span class="font-medium">73</span>
          </li>
        </ul>
      </section>
  
      <!-- Controversy Tracker -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">Controversy Tracker</h2>
        <div class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          [Timeline or dot chart showing controversy intensity]
        </div>
      </section>
  
      <!-- ESG vs Industry Benchmark -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">ESG vs Industry Benchmark</h2>
        <div class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          [Bar comparison: Company vs Industry]
        </div>
      </section>
  
      <!-- ESG Contribution to Strategy -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">ESG Contribution to Investment Strategy</h2>
        <div class="h-32 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          [Stacked bar chart showing strategy contribution]
        </div>
      </section>
  
      <!-- GPT Narrative Summary -->
      <section class="bg-white shadow rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">AI-Generated Summary</h2>
        <p class="text-gray-700 leading-relaxed">
          The company has a good overall ESG score, with particularly strong performance in the
          <strong class="font-medium">Social</strong> and <strong class="font-medium">Governance</strong> categories. The ESG score has increased over the past year.
          There have been recent controversies related to labor practices. The company is
          well-aligned with an <strong class="font-medium">Impact investing strategy</strong>.
        </p>
      </section>
  
    </div>
  </template>
  

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/store/useAuthStore"; // Import the auth store
import RadarChart from "@/components/RadarChart.vue";
import LineChart from "@/components/LineChart.vue";
import KPIDrilldown from "@/components/KPIDrilldown.vue";
import DotPlot from "@/components/DotPlot.vue";
import HorizontalBarChart from "@/components/HorizontalBarChart.vue";
import StackedBarChart from "@/components/StackedBarChart.vue";
import axiosInstance from "@/axiosConfig";

const route = useRoute(); // Access the route object
const symbol = route.params.symbol; // Get the "symbol" parameter from the route

const authStore = useAuthStore(); // Initialize the auth store

const companyData = ref({});
const esgBreakdown = ref({});
const esgTrends = ref({});
const userPreferences = ref({});
const controversyData = ref({});
const industryBenchmarkData = ref({});
const investmentStrategyData = ref({});
const kpiData = ref({});

const fetchCompanyData = async () => {
  try {
// Call the backend API with the ticker parameter
    const response = await axiosInstance.get(`/get-esg-data/${symbol}/`);
    companyData.value = response.data;
    console.log("Company Data:", companyData.value); // Debugging
  } catch (error) {
    console.error("Error fetching company data:", error);
    companyData.value = null; // Set to null if data is not found
  }
};

const fetchUserPreferences = async () => {
  try {
    const response = await axiosInstance.get("/account/preferences/");
    if (response.data.success) {
      userPreferences.value = response.data.preferences;
    }
  } catch (error) {
    console.error("Error fetching user preferences:", error);
  }
};

onMounted(async () => {
  console.log('Symbol:', symbol); // Debugging the symbol parameter
  await fetchCompanyData();
  await fetchUserPreferences();
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: auto;
  padding: 40px;
  background: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.company-header {
  text-align: center;
  margin-bottom: 40px;
}

.company-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
}

.company-symbol {
  font-size: 1.2rem;
  color: #555;
  margin-top: 5px;
}

.company-description {
  font-size: 1.1rem;
  color: #666;
  margin-top: 10px;
}

.esg-breakdown,
.esg-trends,
.chat-wrapper {
  margin-bottom: 40px;
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.trend-charts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

h2 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.chat-description {
  text-align: center;
  font-size: 1rem;
  color: #666;
  margin-bottom: 20px;
}
</style>