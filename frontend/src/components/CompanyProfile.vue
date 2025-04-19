<template>
  <div class="bg-white shadow-lg rounded-2xl p-6 space-y-6">
    <h2 class="text-2xl font-bold text-gray-800">Company Profile</h2>
    <div v-if="profileData" class="space-y-4">
      <!-- Company Overview -->
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-700">{{ profileData.symbol }}</h3>
          <p class="text-gray-600">{{ profileData.summaryProfile.industry }}</p>
        </div>
        <a
          :href="profileData.summaryProfile.website"
          target="_blank"
          class="text-blue-600 hover:underline mt-2 md:mt-0"
        >
          Visit Website
        </a>
      </div>

      <!-- Address -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 class="text-sm font-medium text-gray-500">Address</h4>
          <p class="text-gray-700">
            {{ profileData.summaryProfile.address1 }}, {{ profileData.summaryProfile.city }},
            {{ profileData.summaryProfile.state }} {{ profileData.summaryProfile.zip }},
            {{ profileData.summaryProfile.country }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Contact</h4>
          <p class="text-gray-700">Phone: {{ profileData.summaryProfile.phone }}</p>
        </div>
      </div>

      <!-- Business Summary -->
      <div>
        <h4 class="text-sm font-medium text-gray-500">Business Summary</h4>
        <p class="text-gray-700 leading-relaxed">
          {{ profileData.summaryProfile.longBusinessSummary }}
        </p>
      </div>

      <!-- Additional Information -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 class="text-sm font-medium text-gray-500">Sector</h4>
          <p class="text-gray-700">{{ profileData.summaryProfile.sector }}</p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Full-Time Employees</h4>
          <p class="text-gray-700">
            {{ profileData.summaryProfile.fullTimeEmployees?.toLocaleString() }}
          </p>
        </div>
      </div>
    </div>
    <div v-else class="h-40 flex items-center justify-center text-gray-400">
      Loading company profile...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const profileData = ref(null);

const fetchCompanyProfile = async (symbol) => {
  try {
    const response = await axios.get(
      `https://yahoo-finance-real-time1.p.rapidapi.com/stock/get-profile?region=US&lang=en-US&symbol=${symbol}`,
      {
        headers: {
          "x-rapidapi-key": "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
          "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com",
        },
      }
    );
    profileData.value = response.data;
  } catch (error) {
    console.error("Error fetching company profile:", error);
  }
};

const props = defineProps({
  symbol: {
    type: String,
    required: true,
  },
});

onMounted(() => {
  fetchCompanyProfile(props.symbol);
});
</script>

<style scoped>
h2 {
  color: #1f2937; /* Tailwind gray-800 */
}

h3 {
  color: #374151; /* Tailwind gray-700 */
}

p {
  color: #4b5563; /* Tailwind gray-600 */
}
</style>