<template>
  <div class="container">
    <header class="portfolio-header">
      <h1>Your Portfolio</h1>
      <p>Manage your investments and track ESG performance.</p>
    </header>

    <!-- Add Company Button -->
    <div class="add-company-button">
      <button class="green-button" @click="showModal = true">+ Add Company</button>
    </div>

    <!-- Financial | ESG Toggle -->
    <div class="toggle-options">
      <span
        :class="{ active: selectedTab === 'financial' }"
        @click="selectedTab = 'financial'"
      >
        Financial
      </span>
      |
      <span
        :class="{ active: selectedTab === 'esg' }"
        @click="selectedTab = 'esg'"
      >
        ESG
      </span>
    </div>

    <!-- Modal for Add Company -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Add Company</h2>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <!-- Options for Company Finder and Bulk Import -->
          <div v-if="!selectedOption" class="options">
            <span class="option-text" @click="selectOption('companyFinder')">Company Finder</span>
            <span class="option-text" @click="selectOption('bulkImport')">Bulk Import</span>
          </div>

          <!-- Company Finder Form -->
          <div v-if="selectedOption === 'companyFinder' && !companySelected" class="company-finder">
            <button class="back-button" @click="goBack">&larr; Back</button>
            <h3 class="sub-heading">Company Finder</h3>
            <div class="input-container">
              <input
                v-model="searchQuery"
                placeholder="Search for a company..."
                class="search-input"
              />
              <button @click="fetchCompanies" class="search-button">
                <span class="search-icon">🔍</span>
              </button>
            </div>
            <ul v-if="searchResults.length" class="dropdown">
              <li v-for="(company, index) in searchResults"
                  :key="index"
                  @click="selectCompany(company)">
                <div class="result-item">
                  <div class="result-symbol">{{ company.symbol }}</div>
                  <div class="result-name">{{ company.name }}</div>
                </div>
              </li>
            </ul>
            <div v-else-if="!searchResults.length && searchQuery" class="no-results-message">
              No results found. Currently, we only support companies listed on the USA, Japan, and UK stock exchanges.
            </div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          </div>

          <!-- Add Company Details Form -->
          <div v-if="selectedOption === 'companyFinder' && companySelected" class="company-details">
            <button class="back-button" @click="companySelected = false">&larr; Back</button>
            <h3 class="sub-heading">Add Company Details</h3>
            <p class="selected-stock">Selected: {{ selectedStock.name }} ({{ selectedStock.symbol }})</p>
            <div class="input-container">
              <input
                v-if="inputType === 'shares'"
                type="number"
                v-model="shares"
                placeholder="Number of shares"
                class="shares-input"
              />
              <input
                v-if="inputType === 'amount'"
                type="number"
                v-model="amountInvested"
                placeholder="Amount invested ($)"
                class="shares-input"
              />
              <div class="switch-input">
                <span
                  :class="{ active: inputType === 'shares' }"
                  @click="inputType = 'shares'"
                >
                  Number of shares
                </span>
                |
                <span
                  :class="{ active: inputType === 'amount' }"
                  @click="inputType = 'amount'"
                >
                  Amount invested
                </span>
              </div>
              <div class="input-container">
                <input
                  type="number"
                  v-model="priceBoughtAt"
                  placeholder="Price Bought At (per share)"
                  class="shares-input"
                />
              </div>
            </div>
            <button @click="addStock" class="add-button">Add to Portfolio</button>
          </div>

          <!-- Bulk Import Form -->
          <div v-if="selectedOption === 'bulkImport'" class="bulk-import">
            <button class="back-button" @click="goBack">&larr; Back</button>
            <h3 class="sub-heading">Bulk Import</h3>
            <p>Upload a CSV file to add multiple companies to your portfolio.</p>
            <input type="file" @change="handleFileUpload" class="file-input" />
            <button @click="uploadFile" class="upload-button">Upload</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Display Tables Based on Selected Tab -->
    <HoldingsTable v-if="selectedTab === 'financial'" />
    <ESGTable v-else />
  </div>
</template>

<script setup>
import { ref } from "vue";
import axiosInstance from "../axiosConfig";
import HoldingsTable from "../components/HoldingsTable.vue";
import ESGTable from "../components/ESGTable.vue";

const searchQuery = ref("");
const searchResults = ref([]);
const selectedStock = ref(null);
const shares = ref(null);
const amountInvested = ref(null);
const priceBoughtAt = ref(null);
const inputType = ref("shares");
const showModal = ref(false);
const selectedOption = ref(null);
const companySelected = ref(false);
const errorMessage = ref("");
const file = ref(null);
const selectedTab = ref("financial"); // Default to Financial

const fetchCompanies = async () => {
  try {
    const response = await axiosInstance.get("/search-company/", {
      params: {
        query: searchQuery.value,
      },
    });
    console.log("API Response:", response.data); // Debugging log
    searchResults.value = response.data.results || [];
  } catch (error) {
    console.error("Error fetching companies:", error);
    errorMessage.value = error.response?.data?.error || "Failed to search companies. Please try again.";
  }
};

const selectCompany = (company) => {
  selectedStock.value = company;
  companySelected.value = true;
};

const addStock = async () => {
  if (inputType.value === "shares" && (!selectedStock.value || shares.value <= 0 || priceBoughtAt.value <= 0)) {
    alert("Please select a stock, enter a valid number of shares, and enter a valid price bought at.");
    return;
  }

  if (inputType.value === "amount" && (!selectedStock.value || amountInvested.value <= 0 || priceBoughtAt.value <= 0)) {
    alert("Please select a stock, enter a valid amount invested, and enter a valid price bought at.");
    return;
  }

  try {
    await axiosInstance.post("/add-stock/", {
      symbol: selectedStock.value.symbol,
      name: selectedStock.value.name,  // Include company name
      shares: inputType.value === "shares" ? shares.value : null,
      amountInvested: inputType.value === "amount" ? amountInvested.value : null,
      priceBoughtAt: priceBoughtAt.value,
    });
    selectedStock.value = null;
    shares.value = null;
    amountInvested.value = null;
    priceBoughtAt.value = null;
    closeModal();
  } catch (error) {
    console.error("Failed to add stock:", error);
  }
};

const closeModal = () => {
  showModal.value = false;
  searchQuery.value = "";
  searchResults.value = [];
  selectedStock.value = null;
  shares.value = null;
  amountInvested.value = null;
  priceBoughtAt.value = null;
  selectedOption.value = null;
  companySelected.value = false;
  inputType.value = "shares";
};

const selectOption = (option) => {
  selectedOption.value = option;
};

const goBack = () => {
  selectedOption.value = null;
  companySelected.value = false;
};

const handleFileUpload = (event) => {
  file.value = event.target.files[0];
};

const uploadFile = async () => {
  if (!file.value) {
    alert("Please select a file to upload.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file.value);

  try {
    await axiosInstance.post("/bulk-import/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    alert("File uploaded successfully.");
    closeModal();
  } catch (error) {
    console.error("Failed to upload file:", error);
    alert("Failed to upload file. Please try again.");
  }
};
</script>

<style scoped>
/* Container styling */
.container {
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

/* Title styling */
.portfolio-header h1 {
  font-size: 28px;
  font-weight: bold;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  margin-bottom: 10px;
  color: #333;
}

.portfolio-header p {
  font-size: 16px;
  color: #666;
  margin-bottom: 30px;
}

/* Input box styling */
.search-input, .shares-input, .file-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  margin-bottom: 10px;
  padding-right: 40px; /* Add padding to the right to make space for the icon */
}

.search-input {
  position: relative;
}

.search-button {
  position: absolute;
  right: 10px;
  top: 42%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
}

.search-icon {
  font-size: 16px;
  color: #ccc;
}

/* Submit button styling */
.add-button, .green-button, .upload-button {
  background-color: #007aff;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 10px;
}

.add-button:hover, .green-button:hover, .upload-button:hover {
  background-color: #005bb5;
}

/* Option text styling */
.option-text {
  font-size: 16px;
  color: #007aff;
  cursor: pointer;
  margin: 0 10px;
}

.option-text:hover {
  text-decoration: underline;
}

/* Dropdown styling */
.dropdown {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
  max-width: 400px; /* Set a maximum width */
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 5px;
  left: 50%;
  transform: translateX(-50%);
}

.dropdown li {
  padding: 0;
  cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

.dropdown li:hover {
  background: #f0f0f0;
}

.result-item {
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.result-symbol {
  font-weight: bold;
  font-size: 1rem;
  color: #333;
}

.result-name {
  font-size: 0.875rem;
  color: #666;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.no-results-message {
  color: #666;
  margin-top: 10px;
}

/* Add spacing between elements */
.input-container, .add-company-button, .company-finder, .bulk-import, .error-message, .add-button {
  margin-bottom: 20px;
  position: relative;
}

/* Modal styling */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 500px;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

/* Sub-heading styling */
.sub-heading {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Back button styling */
.back-button {
  background: none;
  border: none;
  font-size: 16px;
  color: #007aff;
  cursor: pointer;
  margin-bottom: 20px;
}

.back-button:hover {
  text-decoration: underline;
}

/* Switch input styling */
.switch-input {
  display: flex;
  justify-content: center;
  margin: 20px 0; /* Adjusted margin to create even spacing */
}

.switch-input span {
  cursor: pointer;
  font-size: 14px;
  color: #007aff;
  margin: 0 5px;
}

.switch-input span.active {
  font-weight: bold;
  text-decoration: underline;
}

/* Selected stock styling */
.selected-stock {
  margin-bottom: 20px; /* Add margin to create space between the selected stock text and the input box */
}

/* Add styles for the toggle options */
.toggle-options {
  margin: 20px 0;
  font-size: 16px;
  color: #007aff;
  cursor: pointer;
}

.toggle-options span {
  margin: 0 10px;
  cursor: pointer;
}

.toggle-options span.active {
  font-weight: bold;
}

/* Add hover underline for toggle options */
.toggle-options span:hover {
  text-decoration: underline;
}
</style>