<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-8 text-gray-900">
    <!-- Page Title -->
    <h1 class="text-4xl font-bold tracking-tight text-center">
      {{ companyData["Company Name"] || "Loading..." }}
    </h1>

    <!-- Toggle Buttons -->
    <div class="flex justify-center space-x-4">
      <button
        @click="activeSection = 'CompanyProfile'"
        :class="[
          'px-4 py-2 font-medium rounded-lg',
          activeSection === 'CompanyProfile' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
        ]"
      >
        Company Profile
      </button>
      <button
        @click="activeSection = 'FinancialDetails'"
        :class="[
          'px-4 py-2 font-medium rounded-lg',
          activeSection === 'FinancialDetails' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
        ]"
      >
        Financial Details
      </button>
    </div>

    <!-- Toggle Content -->
    <div v-if="activeSection === 'CompanyProfile'" class="space-y-8">
      <CompanyProfile :symbol="symbol" />
    </div>
    <div v-else-if="activeSection === 'FinancialDetails'" class="space-y-8">
      <FinancialDetails :symbol="symbol" />
    </div>

    <!-- Top Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Radar Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-center h-[450px]">
        <h2 class="text-lg font-semibold mb-4">ESG Pillar Score Breakdown</h2>
        <RadarChart
          v-if="companyData.Environmental && companyData.Social && companyData.Governance"
          :data="{
            environmental: companyData.Environmental,
            social: companyData.Social,
            governance: companyData.Governance
          }"
        />
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- Line Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-center h-[450px]">
        <h2 class="text-lg font-semibold mb-4">ESG Score Over Time</h2>
        <LineChart
          v-if="companyData['Historical Scores']"
          :data="{
            labels: companyData['Historical Scores'].map((entry) => entry.year),
            scores: companyData['Historical Scores'].map((entry) => entry.score),
            environmentalScores: companyData['Historical Scores'].map((entry) => entry.environmental),
            socialScores: companyData['Historical Scores'].map((entry) => entry.social),
            governanceScores: companyData['Historical Scores'].map((entry) => entry.governance)
          }"
        />
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- AI Summary -->
      <section class="bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-center h-[450px]">
        <h2 class="text-lg font-semibold mb-4">AI-Generated Summary</h2>
        <p v-if="companyData.ai_summary" class="text-gray-700 leading-relaxed text-center">
          {{ companyData.ai_summary }}
        </p>
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
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
          <KPIDrilldown
            v-if="companyData"
            :data="{
              'Resource Use': companyData['Resource Use'],
              Emissions: companyData.Emissions,
              Innovation: companyData.Innovation,
              'CSR Strategy': companyData['CSR Strategy']
            }"
          />
          <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            Loading...
          </div>
        </div>
        <div v-else-if="activeTab === 'Controversies'">
          <div v-if="companyData.controversy_data && companyData.controversy_data.length">
            <ul class="space-y-2">
              <li
                v-for="entry in companyData.controversy_data"
                :key="entry.year"
                class="flex justify-between text-gray-700"
              >
                <span>{{ entry.year }}</span><span class="font-medium">{{ entry.score }}</span>
              </li>
            </ul>
          </div>
          <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            No controversies found.
          </div>
        </div>
        <div v-else-if="activeTab === 'Benchmark'">
          <div v-if="companyData.industry_benchmark">
            <p class="text-gray-700">
              Industry Benchmark ESG Score: <span class="font-medium">{{ companyData.industry_benchmark }}</span>
            </p>
          </div>
          <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            Loading...
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Row -->
    <div class="bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-lg font-semibold mb-4">ESG Contribution to Investment Strategy</h2>
      <div v-if="companyData">
        <ul class="space-y-2">
          <li
            v-for="(value, key) in {
              Community: companyData.Community,
              Workforce: companyData.Workforce,
              Shareholders: companyData.Shareholders,
              Management: companyData.Management,
              'Product Responsibility': companyData['Product Responsibility'],
              'Human Rights': companyData['Human Rights']
            }"
            :key="key"
            class="flex justify-between text-gray-700"
          >
            <span>{{ key }}</span><span class="font-medium">{{ value }}</span>
          </li>
        </ul>
      </div>
      <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
        Loading...
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
import CompanyProfile from "@/components/CompanyProfile.vue";
import FinancialDetails from "@/components/FinancialDetails.vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const route = useRoute();
const symbol = route.params.symbol;

const companyData = ref({});
const activeSection = ref("CompanyProfile"); // Toggle between sections

const fetchCompanyData = async () => {
  try {
    const response = await axiosInstance.get(`/get-esg-data/${symbol}/`);
    companyData.value = response.data;
    console.log("Company data fetched:", companyData.value);
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