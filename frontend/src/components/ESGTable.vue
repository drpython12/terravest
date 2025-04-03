<template>
  <div class="portfolio-container">
    <table v-if="esgData.length > 0" class="holdings-table">
      <thead>
        <tr>
          <th>Company Name</th>
          <th>Ticker</th>
          <th>ESG Score</th>
          <th>Environmental</th>
          <th>Social</th>
          <th>Governance</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in esgData" :key="company.id">
          <td>{{ company.company_name }}</td>
          <td>{{ company.symbol }}</td>
          <td>{{ company.esg_score }}</td>
          <td>{{ company.environmental }}</td>
          <td>{{ company.social }}</td>
          <td>{{ company.governance }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>No ESG data available. Add companies to view ESG performance.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axiosInstance from "../axiosConfig";

const esgData = ref([]);

const loadESGData = async () => {
  try {
    const response = await axiosInstance.get("/get-esg-data/");
    esgData.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("Failed to fetch ESG data:", error);
  }
};

onMounted(loadESGData);
</script>

<style scoped>
/* Reuse the same styles as HoldingsTable.vue */
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
}

.holdings-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}
</style>