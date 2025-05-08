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
          v-if="kpiDrilldownData.Environment && kpiDrilldownData.Social && kpiDrilldownData.Governance"
          :data="{
            environmental: kpiDrilldownData.Environment.score,
            social: kpiDrilldownData.Social.score,
            governance: kpiDrilldownData.Governance.score
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

      <!-- Industry Benchmark -->
      <section class="bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center justify-center h-[450px]">
        <h2 class="text-lg font-semibold mb-4">Industry Benchmark vs. Company Scores</h2>
        <BarChart
          v-if="benchmark && kpiDrilldownData.Environment && kpiDrilldownData.Social && kpiDrilldownData.Governance"
          :data="{
            labels: ['Environmental', 'Social', 'Governance', 'Overall ESG'],
            companyScores: [
              kpiDrilldownData.Environment.score || 0,
              kpiDrilldownData.Social.score || 0,
              kpiDrilldownData.Governance.score || 0,
              companyData['Overall ESG Score'] || 0
            ],
            benchmarkScores: [
              benchmark.environmental || 0,
              benchmark.social || 0,
              benchmark.governance || 0,
              benchmark.esg || 0
            ]
          }"
        />
        <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
          Loading benchmark or company scores...
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
          <KPIDrilldown :data="kpiDrilldownData" />
        </div>
        <div v-else-if="activeTab === 'Controversies'">
          <div>
            <div v-if="error" class="text-red-500">{{ error }}</div>
            <Controversies
              :controversyData="controversyData"
              :controversyCategories="controversyCategories"
            />
          </div>
        </div>
        <div v-else-if="activeTab === 'Peer Scores'">
          <div v-if="peers.length">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b">
                  <th class="py-2">Company</th>
                  <th class="py-2">Ticker</th>
                  <th class="py-2">Environmental</th>
                  <th class="py-2">Social</th>
                  <th class="py-2">Governance</th>
                  <th class="py-2">Overall ESG</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="peer in peers" :key="peer.ticker" class="border-b">
                  <td class="py-2">{{ peer.company_name || "N/A" }}</td>
                  <td class="py-2">{{ peer.ticker }}</td>
                  <td class="py-2">{{ peer.environmental }}</td>
                  <td class="py-2">{{ peer.social }}</td>
                  <td class="py-2">{{ peer.governance }}</td>
                  <td class="py-2">{{ peer.esg }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="h-40 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
            Peer Scores not available.
          </div>
        </div>
        <div v-else-if="activeTab === 'Latest News'">
          <NewsFeed :newsList="latestNews" :loading="aiLoading || latestNews.length === 0" />
        </div>
      </div>
    </div>

    <!-- AI Summary -->
    <div class="bg-white shadow-lg rounded-2xl p-6 my-8 max-w-7xl mx-auto">
      <AI :insight="aiInsight" :loading="aiLoading" :error="aiError" />
    </div>

    <!-- ChatGPT Q&A -->
    <div class="bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-lg font-semibold mb-4">Ask ChatGPT</h2>
      <textarea
        v-model="chatInput"
        placeholder="Ask a question about this company..."
        class="w-full p-4 border rounded-lg mb-4"
      ></textarea>
      <button
        @click="askChatGPT"
        class="px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700"
      >
        Ask
      </button>
      <div v-if="chatResponse" class="mt-4 p-4 bg-gray-100 rounded-lg text-gray-700">
        {{ chatResponse }}
      </div>
      <div v-else class="mt-4 p-4 bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
        ChatGPT is currently unavailable.
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
import Controversies from "@/components/Controversies.vue";
import AI from "@/components/AI.vue";
import NewsFeed from "@/components/NewsFeed.vue";
import BarChart from "@/components/BarChart.vue"; // Import the BarChart component
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const route = useRoute();
const symbol = route.params.symbol; // Dynamically fetch the symbol from the route

const companyData = ref({
  "ESG Scores": {
    environmental: 70.5,
    social: 65.3,
    governance: 78.9,
    esg: 71.2,
  },
}); // Mock company data for testing
const activeSection = ref("CompanyProfile"); // Toggle between sections
const peers = ref([]); // Default empty array for Peer Scores
const benchmark = ref({
  environmental: 75.32,
  social: 68.45,
  governance: 80.12,
  esg: 74.63,
}); // Mock data for testing
const tabs = ["KPI Breakdown", "Controversies", "Peer Scores", "Latest News"]; // Tabs for the second row
const activeTab = ref(tabs[0]);
const kpiDrilldownData = ref({});
const latestNews = ref([]); // Default empty array for Latest News
const chatInput = ref("");
const chatResponse = ref(""); // Default empty string for ChatGPT response
const controversyData = ref({}); // Default empty object for Controversy Data
const controversyCategories = ref([]); // Default empty array
const error = ref(null);
const aiInsight = ref(null); // AI-generated summary
const aiLoading = ref(true); // Loading state for AI summary
const aiError = ref(null); // Error state for AI summary
const news = ref(null);

const fetchCompanyData = async () => {
  try {
    const response = await axiosInstance.get(`/get-esg-data/${symbol}/`);
    console.log("Backend Response:", response.data);
    console.log("API Response:", response.data);

    companyData.value = response.data;
    kpiDrilldownData.value = response.data["KPI Drilldown"] || {}; // Fallback to empty object
    controversyData.value = response.data["Controversy Data"] || {}; // Fallback to empty object
    controversyCategories.value = response.data["Controversy Categories"] || []; // Fallback to empty array

    console.log("Controversy Data:", controversyData.value);
    console.log("Controversy Categories:", controversyCategories.value);
  } catch (err) {
    error.value = "Failed to load company data.";
    console.error("Error fetching company data:", err);
  }
};

const fetchPeerScores = async () => {
  try {
    const response = await axiosInstance.get(`/fetch-esg-peer-scores/${symbol}/`);
    peers.value = response.data || []; // Fallback to empty array
    console.log("Peer scores fetched:", peers.value);
  } catch (error) {
    console.warn("Peer Scores backend not implemented or unavailable.");
  }
};

const fetchLatestNews = async () => {
  try {
    const response = await axiosInstance.get(`/fetch-esg-news/?company_name=${companyData.value["Company Name"]}`);
    if (response.data.status === "processing" && response.data.task_id) {
      const taskId = response.data.task_id;
      pollNewsStatus(taskId);
      return;
    }
    // If completed immediately (cached), handle as before:
    const articles = response.data.result?.articles || [];
    latestNews.value = articles.map((article) => ({
      title: article.title || "No title available",
      description: article.description || "No description available",
      url: article.url || "#",
      source: article.source || "Unknown source",
      publishedAt: article.date
        ? new Date(article.date).toLocaleDateString()
        : "Unknown date",
    }));
  } catch (error) {
    console.warn("Failed to fetch latest news:", error);
    latestNews.value = [];
  }
};

const pollNewsStatus = async (taskId) => {
  try {
    const response = await axiosInstance.get(`/check-esg-news-status/${taskId}/`);
    if (response.data.status === "processing") {
      setTimeout(() => pollNewsStatus(taskId), 3000);
    } else if (response.data.status === "completed") {
      const articles = response.data.result?.articles || [];
      latestNews.value = articles.map((article) => ({
        title: article.title || "No title available",
        description: article.description || "No description available",
        url: article.url || "#",
        source: article.source || "Unknown source",
        publishedAt: article.date
          ? new Date(article.date).toLocaleDateString()
          : "Unknown date",
      }));
    } else if (response.data.status === "error") {
      console.error("Error fetching news:", response.data.message);
      latestNews.value = [];
    }
  } catch (error) {
    console.warn("Failed to poll news status:", error);
    latestNews.value = [];
  }
};

const fetchAISummary = async () => {
  try {
    aiLoading.value = true;
    const response = await axiosInstance.post("/generate-esg-insight/", {
      companyData: companyData.value,
    });
    if (response.data.status === "processing" && response.data.task_id) {
      pollAIInsightStatus(response.data.task_id);
      return;
    }
    aiInsight.value = response.data.result;
    aiLoading.value = false;
  } catch (error) {
    console.error("Error fetching AI summary:", error);
    aiError.value = "Unable to generate ESG insight.";
    aiLoading.value = false;
  }
};

const pollAIInsightStatus = async (taskId) => {
  try {
    const response = await axiosInstance.get(`/check-ai-insight-status/${taskId}/`);
    if (response.data.status === "processing") {
      setTimeout(() => pollAIInsightStatus(taskId), 3000);
    } else if (response.data.status === "completed") {
      aiInsight.value = response.data.result;
      aiLoading.value = false;
    } else if (response.data.status === "error") {
      aiError.value = response.data.message || "Unable to generate ESG insight.";
      aiLoading.value = false;
    }
  } catch (error) {
    aiError.value = "Unable to generate ESG insight.";
    aiLoading.value = false;
  }
};

const askChatGPT = async () => {
  try {
    const response = await axiosInstance.post(`/chatgpt-advisor/`, {
      question: chatInput.value,
      symbol,
    });
    chatResponse.value = response.data.answer || "No response available."; // Fallback message
    console.log("ChatGPT response:", chatResponse.value);
  } catch (error) {
    console.warn("ChatGPT backend not implemented or unavailable.");
    chatResponse.value = "ChatGPT is currently unavailable.";
  }
};

onMounted(async () => {
  try {
    await fetchCompanyData();
    await fetchAISummary(); // Fetch AI summary after company data
    fetchPeerScores(); // Non-blocking
    fetchLatestNews(); // Non-blocking
    // Commenting out the fetchIndustryBenchmark call to use mock data
    // fetchIndustryBenchmark(); 
  } catch (error) {
    console.error("Error initializing page:", error);
  }
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