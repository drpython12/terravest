<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-8 text-gray-900">
    <!-- Page Title -->
    <h1 class="text-4xl font-bold tracking-tight text-center">
      Explore Companies
    </h1>

    <!-- Search Bar -->
    <div class="flex justify-center">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search for a company..."
        class="w-full max-w-3xl px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
    </div>

    <!-- Trending Tickers -->
    <div class="space-y-8">
      <section>
        <h2 class="text-2xl font-semibold mb-4">Trending Tickers</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="ticker in filteredTrendingTickers"
            :key="ticker.symbol"
            class="bg-white shadow-lg rounded-2xl p-6 flex flex-col justify-between"
          >
            <div>
              <h3 class="text-lg font-medium text-gray-800">
                {{ ticker.symbol }}
              </h3>
              <p class="text-sm text-gray-500">
                {{ ticker.fullExchangeName }} ({{ ticker.region }})
              </p>
              <p class="text-sm text-gray-500">
                Price: ${{ ticker.regularMarketPrice }}
              </p>
              <p
                :class="[
                  'text-sm font-medium',
                  ticker.regularMarketChangePercent > 0
                    ? 'text-green-600'
                    : 'text-red-600'
                ]"
              >
                {{ ticker.regularMarketChangePercent.toFixed(2) }}%
              </p>
            </div>
            <div class="mt-4 flex justify-between items-center">
              <button
                @click="addToPortfolio(ticker.symbol)"
                class="text-sm text-blue-600 hover:underline"
              >
                Add to Portfolio
              </button>
              <button
                @click="goToCompanyPage(ticker.symbol)"
                class="text-sm text-blue-600 hover:underline"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const searchQuery = ref("");
const screeners = ref([]);
const trendingTickers = ref([]);
const searchResults = ref([]);
const searching = ref(false);
const searchError = ref("");

// Fetch predefined screeners from Yahoo Finance API
const fetchScreeners = async () => {
  try {
    const response = await axios.get(
      "https://yahoo-finance-real-time1.p.rapidapi.com/screeners/get-list",
      {
        headers: {
          "x-rapidapi-key": "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
          "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com",
        },
      }
    );
    const screenerData = response.data.finance.result;

    // Mock company data for each screener (replace with actual API calls if available)
    screeners.value = screenerData.map((screener) => ({
      id: screener.id,
      title: screener.title,
      description: screener.description,
      companies: Array.from({ length: 6 }, (_, i) => ({
        name: `${screener.title} Company ${i + 1}`,
        symbol: `${screener.canonicalName}_${i + 1}`,
      })),
    }));
  } catch (error) {
    console.error("Error fetching screeners:", error);
  }
};

// Fetch trending tickers from Yahoo Finance API
const fetchTrendingTickers = async () => {
  try {
    const response = await axios.get(
      "https://yahoo-finance-real-time1.p.rapidapi.com/market/get-trending-tickers?region=US",
      {
        headers: {
          "x-rapidapi-key": "c4cf9f510cmsh80ee50ea6a7d2b3p171c27jsnab5350889c90",
          "x-rapidapi-host": "yahoo-finance-real-time1.p.rapidapi.com",
        },
      }
    );
    // Filter only equities
    trendingTickers.value = response.data.finance.result[0].quotes.filter(
      (ticker) => ticker.quoteType === "EQUITY"
    );
  } catch (error) {
    console.error("Error fetching trending tickers:", error);
  }
};

// Filter screeners based on search query
const filteredScreeners = computed(() =>
  screeners.value.filter((screener) =>
    screener.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

// Filter trending tickers based on search query
const filteredTrendingTickers = computed(() =>
  trendingTickers.value.filter((ticker) =>
    ticker.symbol.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

// Navigate to company details page
const goToCompanyPage = (symbol) => {
  router.push(`/company/${symbol}`);
};

// Mock function to add a company to the portfolio
const addToPortfolio = (symbol) => {
  console.log(`Added ${symbol} to portfolio`);
};

// Watch searchQuery and fetch company results from backend
watch(
  searchQuery,
  async (newQuery) => {
    if (!newQuery || newQuery.length < 2) {
      searchResults.value = [];
      searchError.value = "";
      return;
    }
    searching.value = true;
    searchError.value = "";
    try {
      // Adjust the URL if your backend is on a different path
      const response = await axios.get(`/search-company/?query=${encodeURIComponent(newQuery)}`);
      searchResults.value = response.data.results || [];
    } catch (err) {
      searchResults.value = [];
      searchError.value = "Error searching companies.";
    } finally {
      searching.value = false;
    }
  }
);

onMounted(() => {
  fetchScreeners();
  fetchTrendingTickers();
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