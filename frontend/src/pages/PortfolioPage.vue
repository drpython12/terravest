<template>
  <div class="portfolio-container">
    <header class="portfolio-header">
      <h1>Your Portfolio</h1>
      <p>Manage your investments and track ESG performance.</p>
    </header>

    <!-- Add Company Button -->
    <div class="add-company-button" @mouseenter="dropdownOpen = true" @mouseleave="dropdownOpen = false">
      <button class="green-button">+ Add Company</button>
      <div v-if="dropdownOpen" class="dropdown-menu">
        <button @click="selectOption('companyFinder')">Company Finder</button>
        <button @click="selectOption('bulkImport')">Bulk Import</button>
      </div>
    </div>

    <!-- Company Finder Form -->
    <div v-if="showCompanyFinder" class="company-finder">
      <h2>Company Finder</h2>
      <div class="input-container">
        <input
          v-model="searchQuery"
          placeholder="Search for a company..."
          class="search-input"
          @input="fetchCompanies"
        />
      </div>
      <ul v-if="searchResults.length">
        <li>v-for="(company, index) in searchResults"
          :key="index"
          @click="selectCompany(company)"
          {{ company.name }} ({{ company.symbol }}) - {{ company.region }} [{{ company.currency }}]
      </li>
      </ul>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="selectedStock">
        <p>Selected: {{ selectedStock.name }} ({{ selectedStock.symbol }})</p>
        <input type="number" v-model="shares" placeholder="Number of shares" class="shares-input" />
        <button @click="addStock" class="add-button">Add to Portfolio</button>
      </div>
    </div>

    <!-- Holdings Table -->
    <HoldingsTable />
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import HoldingsTable from "../components/HoldingsTable.vue";

const searchQuery = ref("");
const searchResults = ref([]);
const selectedStock = ref(null);
const shares = ref(0);
const dropdownOpen = ref(false);
const showCompanyFinder = ref(false);
const errorMessage = ref("");

const searchCompany = async (query) => {
  if (!searchQuery.value.trim()) {
        searchResults.value = [];
        return;
    }
    try {
        let response = await axios.get(`/search-company/`, {
            params: { query: searchQuery.value.trim() }
        });

        if (response.data.results) {
            searchResults.value = response.data.results;
        } else {
            searchResults.value = [];
        }
    } catch (error) {
        console.error("Error fetching company data:", error);
        searchResults.value = [];
    }
};

const fetchCompanies = async () => {
  if (searchQuery.value.length < 2) return; // Only fetch after 2+ characters

  console.log(`Fetching companies for query: ${searchQuery.value}`); // Debugging log

  errorMessage.value = "";
  try {
    const response = await axios.get(`/api/search-companies/`, {
      params: {
        query: searchQuery.value
      }
    });
    console.log("Full response:", response); // Debugging log
    console.log("Search results:", response.data.results); // Debugging log
    searchResults.value = response.data.results || [];
  } catch (error) {
    console.error("Failed to search companies:", error);
    errorMessage.value = "Failed to search companies. Please try again.";
  }
};

const selectCompany = (company) => {
  selectedStock.value = company;
  searchQuery.value = company.name; // Set input to selected company name
  searchResults.value = []; // Hide dropdown after selection
};

const addStock = async () => {
  if (!selectedStock.value || shares.value <= 0) {
    alert("Please select a stock and enter a valid number of shares.");
    return;
  }

  try {
    await axios.post("/api/add-stock", {
      symbol: selectedStock.value.symbol,
      shares: shares.value,
    });
    selectedStock.value = null;
    shares.value = 0;
  } catch (error) {
    console.error("Failed to add stock:", error);
  }
};

const selectOption = (option) => {
  dropdownOpen.value = false;
  if (option === 'companyFinder') {
    showCompanyFinder.value = true;
  } else if (option === 'bulkImport') {
    showCompanyFinder.value = false;
    // Implement bulk import functionality here
  }
};

watch(searchQuery, fetchCompanies);
</script>

<style scoped>
/* Apple-Style UI */
.portfolio-container {
  max-width: 1200px;
  margin: auto;
  padding: 40px 20px;
  background: #f9f9f9;
}

.portfolio-header {
  text-align: center;
  margin-bottom: 30px;
}

.portfolio-header h1 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

.add-company-button {
  text-align: center;
  margin-bottom: 20px;
  position: relative;
}

.green-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 6px;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.green-button:hover {
  background-color: #218838;
}

.dropdown-menu {
  display: none;
  flex-direction: column;
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 5px;
  width: 100%;
}

.add-company-button:hover .dropdown-menu,
.dropdown-menu:hover {
  display: flex;
}

.dropdown-menu button {
  background: none;
  border: none;
  padding: 10px;
  cursor: pointer;
  text-align: left;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: black;
}

.dropdown-menu button:hover {
  background: #f0f0f0;
}

.company-finder {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
}

.company-finder h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.input-container {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.shares-input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.add-button {
  padding: 10px 15px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 6px;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.add-button:hover {
  background: #0056b3;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>