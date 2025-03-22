<template>
  <div class="portfolio-container">
    <table v-if="portfolio.length > 0" class="holdings-table" table>
      <thead>
        <tr>
          <th>Company Name</th>
          <th>Ticker</th>
          <th>Live Price</th>
          <th>Market Value</th>
          <th>% Return</th>
          <th>$ Return</th>
          <th>ESG Score</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in portfolio" :key="stock.id">
          <td>{{ stock.company_name }}</td>
          <td>{{ stock.symbol }}</td>
          <td v-if="stock.livePrice">${{ stock.livePrice.toFixed(2) }}</td>
          <td v-else>Loading...</td>
          <td v-if="stock.livePrice">${{ (stock.shares * stock.livePrice).toFixed(2) }}</td>
          <td v-else>Loading...</td>
          <td v-if="stock.livePrice">
            {{ calculatePercentageReturn(stock).toFixed(2) }}%
          </td>
          <td v-if="stock.livePrice">
            ${{ calculateDollarReturn(stock).toFixed(2) }}
          </td>
          <td>{{ stock.esg_score }}</td>
          <td>
            <button class="edit-btn" @click="editStock(stock)">✏️ Edit</button>
            <button class="remove-btn" @click="removeStock(stock.id)">❌ Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>You don't have any holdings yet. Start adding companies to your portfolio!</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "../axiosConfig";

const portfolio = ref([]);

const loadPortfolio = async () => {
  try {
    const response = await axiosInstance.get("/get-portfolio/");
    portfolio.value = Array.isArray(response.data) ? response.data : [];

    if (portfolio.value.length > 0) {
      // Fetch live prices for all stocks
      for (let stock of portfolio.value) {
        await updateStockPrice(stock);
      }
    }
  } catch (error) {
    console.error("Failed to fetch portfolio:", error);
  }
};

const updateStockPrice = async (stock) => {
  try {
    const response = await axiosInstance.get(`/get-stock-price/?symbol=${stock.symbol}`);
    stock.livePrice = response.data.price;
  } catch (error) {
    console.error(`Failed to fetch price for ${stock.symbol}:`, error);
  }
};

const calculatePercentageReturn = (stock) => {
  const marketValue = stock.shares * stock.livePrice;
  return ((marketValue - stock.amount_invested) / stock.amount_invested) * 100;
};

const calculateDollarReturn = (stock) => {
  const marketValue = stock.shares * stock.livePrice;
  return marketValue - stock.amount_invested;
};

const removeStock = async (id) => {
  try {
    await axiosInstance.delete(`/remove-stock/${id}/`);
    portfolio.value = portfolio.value.filter((stock) => stock.id !== id);
  } catch (error) {
    console.error("Failed to remove stock:", error);
  }
};

const editStock = (stock) => {
  alert(`Edit functionality for ${stock.company_name} is not implemented yet.`);
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
