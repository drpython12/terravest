<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-8 text-gray-900">
    <!-- Page Title -->
    <h1 class="text-4xl font-bold tracking-tight text-center">
      {{ companyData["Company Name"] || "Loading..." }}
    </h1>

    <!-- Top Row -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Radar Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">ESG Pillar Score Breakdown</h2>
        <RadarChart
          v-if="companyData.Environmental && companyData.Social && companyData.Governance"
          :data="{
            environmental: companyData.Environmental,
            social: companyData.Social,
            governance: companyData.Governance
          }"
        />
        <div v-else class="h-80 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- Line Chart -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">ESG Score Over Time</h2>
        <LineChart
          v-if="companyData['Historical Scores']"
          :data="{
            labels: companyData['Historical Scores'].map((entry) => entry.year),
            scores: companyData['Historical Scores'].map((entry) => entry.score)
          }"
        />
        <div v-else class="h-80 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading...
        </div>
      </section>

      <!-- AI Summary -->
      <section class="bg-white shadow-lg rounded-2xl p-6">
        <h2 class="text-lg font-semibold mb-4">AI-Generated Summary</h2>
        <p v-if="companyData.ai_summary" class="text-gray-700 leading-relaxed">
          {{ companyData.ai_summary }}
        </p>
        <div v-else class="h-80 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
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
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const route = useRoute();
const symbol = route.params.symbol;

const companyData = ref({});

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

const props = defineProps({
  data: {
    type: Array, // Updated to accept an array of historical scores
    required: true,
  },
});

const lineChart = ref(null);

const renderChart = () => {
  if (lineChart.value) {
    new Chart(lineChart.value, {
      type: "line",
      data: {
        labels: props.data.map((entry) => entry.year), // Extract years
        datasets: [
          {
            label: "ESG Score",
            data: props.data.map((entry) => entry.score), // Extract scores
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 2,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
};

onMounted(() => {
  renderChart();
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