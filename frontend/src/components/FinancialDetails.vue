<template>
  <div class="bg-white shadow-lg rounded-2xl p-6 space-y-6">
    <h2 class="text-2xl font-bold text-gray-800">Financial Details</h2>

    <!-- User Holdings -->
    <div v-if="userHoldings" class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-700">Your Holdings</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 class="text-sm font-medium text-gray-500">Shares Held</h4>
          <p class="text-gray-700">{{ userHoldings.shares || 0 }}</p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Average Price</h4>
          <p class="text-gray-700">
            ${{ parseFloat(userHoldings.price_bought_at || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Total Investment</h4>
          <p class="text-gray-700">
            ${{ parseFloat(userHoldings.amount_invested || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Current Value</h4>
          <p class="text-gray-700">
            ${{ parseFloat(currentValue || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Return ($)</h4>
          <p :class="returnDollar >= 0 ? 'text-green-600' : 'text-red-600'">
            ${{ parseFloat(returnDollar || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Return (%)</h4>
          <p :class="returnPercent >= 0 ? 'text-green-600' : 'text-red-600'">
            {{ parseFloat(returnPercent || 0).toFixed(2) }}%
          </p>
        </div>
      </div>
    </div>

    <!-- Financial Metrics -->
    <div v-if="financialData" class="space-y-4">
      <h3 class="text-lg font-semibold text-gray-700">Market Metrics</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 class="text-sm font-medium text-gray-500">Current Price</h4>
          <p class="text-gray-700">
            ${{ parseFloat(financialData.currentPrice || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Market Cap</h4>
          <p class="text-gray-700">
            ${{ (parseFloat(financialData.marketCap || 0) / 1e9).toFixed(2) }}B
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">52-Week High</h4>
          <p class="text-gray-700">
            ${{ parseFloat(financialData.high52Week || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">52-Week Low</h4>
          <p class="text-gray-700">
            ${{ parseFloat(financialData.low52Week || 0).toFixed(2) }}
          </p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">P/E Ratio</h4>
          <p class="text-gray-700">{{ financialData.peRatio || "N/A" }}</p>
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-500">Dividend Yield</h4>
          <p class="text-gray-700">{{ financialData.dividendYield || "N/A" }}%</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else class="h-40 flex items-center justify-center text-gray-400">
      Loading financial details...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "@/axiosConfig";

const userHoldings = ref(null);
const financialData = ref(null);
const currentValue = ref(0);
const returnDollar = ref(0);
const returnPercent = ref(0);

const props = defineProps({
  symbol: {
    type: String,
    required: true,
  },
});

const fetchUserHoldings = async () => {
  try {
    const response = await axiosInstance.get(`/get-portfolio/`);
    const holdings = response.data.find((stock) => stock.symbol === props.symbol);
    if (holdings) {
      userHoldings.value = holdings;
    }
  } catch (error) {
    console.error("Error fetching user holdings:", error);
  }
};

const fetchFinancialData = async () => {
  try {
    const response = await axiosInstance.get(`/get-stock-price?symbol=${props.symbol}`);
    const stockData = response.data;

    financialData.value = {
      currentPrice: stockData.price,
      marketCap: 1500000000000, // Example: 1.5T
      high52Week: 3000,
      low52Week: 2000,
      peRatio: 25.3,
      dividendYield: 1.5,
    };

    if (userHoldings.value) {
      currentValue.value = userHoldings.value.shares * financialData.value.currentPrice;
      returnDollar.value = currentValue.value - parseFloat(userHoldings.value.amount_invested || 0);
      returnPercent.value =
        (returnDollar.value / parseFloat(userHoldings.value.amount_invested || 1)) * 100;
    }
  } catch (error) {
    console.error("Error fetching financial data:", error);
  }
};

onMounted(() => {
  fetchUserHoldings();
  fetchFinancialData();
});
</script>

<style scoped>
h2 {
  color: #1f2937; /* Tailwind gray-800 */
}

h3 {
  color: #374151; /* Tailwind gray-700 */
}

h4 {
  color: #6b7280; /* Tailwind gray-500 */
}

p {
  color: #4b5563; /* Tailwind gray-600 */
}
</style>