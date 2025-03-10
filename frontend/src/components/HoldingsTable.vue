<template>
  <div class="portfolio-holdings">
    <h2>Current Holdings</h2>
    <table v-if="portfolio.length > 0">
      <thead>
        <tr>
          <th>Company</th>
          <th>Shares</th>
          <th>Live Price</th>
          <th>Market Value</th>
          <th>ESG Score</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in portfolio" :key="stock.id">
          <td>{{ stock.symbol }}</td>
          <td>{{ stock.shares }}</td>
          <td v-if="stock.livePrice">${{ stock.livePrice.toFixed(2) }}</td>
          <td v-else>Loading...</td>
          <td v-if="stock.livePrice">${{ (stock.shares * stock.livePrice).toFixed(2) }}</td>
          <td v-else>Loading...</td>
          <td>{{ stock.esg_score }}</td>
          <td>
            <button class="remove-btn" @click="removeStock(stock.id)">Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>You don't have any holdings.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const portfolio = ref([]);

const loadPortfolio = async () => {
  try {
    const response = await axios.get("/api/portfolio");
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
    const response = await axios.get(`/api/stock-data?symbol=${stock.symbol}`);
    stock.livePrice = response.data.price;
  } catch (error) {
    console.error(`Failed to fetch price for ${stock.symbol}:`, error);
  }
};

const removeStock = async (id) => {
  try {
    await axios.delete(`/api/remove-stock/${id}`);
    portfolio.value = portfolio.value.filter((stock) => stock.id !== id);
  } catch (error) {
    console.error("Failed to remove stock:", error);
  }
};

onMounted(loadPortfolio);
</script>

<style scoped>
.portfolio-holdings {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

.remove-btn {
  background: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
}
</style>
