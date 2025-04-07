<template>
  <table v-if="isDataReady" class="holdings-table">
    <thead>
      <tr>
        <th>Company Name</th>
        <th>Weight</th>
        <th>Market Value</th>
        <th>% Return</th>
        <th>$ Return</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="stock in limitedPortfolio" :key="stock.id">
        <!-- Make the company name clickable -->
        <td>
          <router-link :to="`/company/${stock.symbol}`" class="company-link">
            {{ stock.company_name }}
          </router-link>
        </td>
        <td>{{ calculateWeight(stock).toFixed(2) }}%</td>
        <td>${{ (stock.shares * stock.livePrice).toFixed(2) }}</td>
        <td>{{ calculatePercentageReturn(stock).toFixed(2) }}%</td>
        <td>${{ calculateDollarReturn(stock).toFixed(2) }}</td>
      </tr>
    </tbody>
  </table>
  <p v-else>Loading your portfolio...</p>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axiosInstance from "../axiosConfig";

const portfolio = ref([]);
const isDataReady = ref(false);
const totalPortfolioValue = ref(0);

// Limit the portfolio to the top 5 companies
const limitedPortfolio = computed(() => portfolio.value.slice(0, 5));

const updateStockPrice = async (stock) => {
  try {
    const response = await axiosInstance.get(`/get-stock-price/?symbol=${stock.symbol}`);
    stock.livePrice = response.data.price;
  } catch (error) {
    console.error(`Failed to fetch price for ${stock.symbol}:`, error);
  }
};

const loadPortfolio = async () => {
  try {
    const response = await axiosInstance.get("/get-portfolio/");
    portfolio.value = Array.isArray(response.data) ? response.data : [];

    if (portfolio.value.length > 0) {
      // Fetch live prices for all stocks
      await Promise.all(
        portfolio.value.map(async (stock) => {
          await updateStockPrice(stock);
        })
      );

      // Calculate the total portfolio value
      totalPortfolioValue.value = portfolio.value.reduce((total, stock) => {
        return total + stock.shares * stock.livePrice;
      }, 0);
    }

    isDataReady.value = true; // Mark data as ready after all calculations
  } catch (error) {
    console.error("Failed to fetch portfolio:", error);
  }
};

const calculateWeight = (stock) => {
  const marketValue = stock.shares * stock.livePrice;
  return (marketValue / totalPortfolioValue.value) * 100;
};

const calculatePercentageReturn = (stock) => {
  const marketValue = stock.shares * stock.livePrice;
  return ((marketValue - stock.amount_invested) / stock.amount_invested) * 100;
};

const calculateDollarReturn = (stock) => {
  const marketValue = stock.shares * stock.livePrice;
  return marketValue - stock.amount_invested;
};

onMounted(loadPortfolio);
</script>

<style scoped>
.portfolio-container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 90%;
  max-width: 1200px;
  margin: auto;
  margin-top: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.holdings-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.holdings-table th,
.holdings-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
  white-space: nowrap; /* Ensure text stays on one line */
}

.holdings-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.company-link {
  color: #007aff;
  text-decoration: none;
  font-weight: bold;
}

.company-link:hover {
  text-decoration: underline;
}

.edit-btn,
.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin: 0 5px;
}

.edit-btn:hover {
  color: #007aff;
}

.remove-btn:hover {
  color: red;
}
</style>