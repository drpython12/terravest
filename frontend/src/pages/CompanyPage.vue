<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-8 text-gray-900">
    <!-- Page Title -->
    <h1 class="text-4xl font-bold tracking-tight text-center">
      {{ companyData.company_name || "Loading..." }}
    </h1>

    <!-- Top Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Radar Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">ESG Pillar Score Breakdown</h2>
        <RadarChart v-if="companyData.radarChart" :data="companyData.radarChart" />
        <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- Line Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">ESG Score Over Time</h2>
        <LineChart v-if="companyData.lineChart" :data="companyData.lineChart" />
        <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- AI Summary -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">AI-Generated Summary</h2>
        <p v-if="companyData.aiSummary" class="text-gray-700 leading-relaxed">
          {{ companyData.aiSummary }}
        </p>
        <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>
    </div>

    <!-- Second Row: Tab Group -->
    <div class="bg-white shadow-lg rounded-2xl p-6">
      <div class="flex space-x-4 border-b pb-2">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          :class="[
            'px-4 py-2 font-medium',
            activeTab === tab ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'
          ]"
        >
          {{ tab }}
        </button>
      </div>
      <div class="mt-4">
        <div v-if="activeTab === 'KPI Breakdown'">
          <KPIDrilldown v-if="companyData.kpiBreakdown" :data="companyData.kpiBreakdown" />
          <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            Loading...
          </div>
        </div>
        <div v-else-if="activeTab === 'Controversies'">
          <div class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            [Controversy Data Placeholder]
          </div>
        </div>
        <div v-else-if="activeTab === 'Benchmark'">
          <div class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            [Benchmark Data Placeholder]
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-lg font-semibold mb-4">ESG Contribution to Investment Strategy</h2>
      <div class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
        [ESG Contribution Chart Placeholder]
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axiosInstance from "@/axiosConfig";

import RadarChart from "@/components/RadarChart.vue";
import LineChart from "@/components/LineChart.vue";
import KPIDrilldown from "@/components/KPIDrilldown.vue";

const route = useRoute();
const symbol = route.params.symbol;

const companyData = ref({});

const fetchCompanyData = async () => {
  try {
    const response = await axiosInstance.get(`/get-esg-data/${symbol}/`);
    companyData.value = response.data;
  } catch (error) {
    console.error("Error fetching company data:", error);
  }
};

const tabs = ["KPI Breakdown", "Controversies", "Benchmark"];
const activeTab = ref(tabs[0]);

onMounted(() => {
  fetchCompanyData();
});
</script>

<style scoped>
h1 {
  color: #1f2937; /* Tailwind gray-900 */
}

h2 {
  color: #374151; /* Tailwind gray-800 */
}

p {
  color: #4b5563; /* Tailwind gray-700 */
}
</style>