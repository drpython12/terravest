<template>
  <div class="container">
    <h2 class="title">Investor Preferences</h2>
    <form @submit.prevent="submitPreferences">
      <div class="input-container">
        <label for="investmentType">Preferred Investment Type</label>
        <select v-model="investmentType" id="investmentType" class="input-box">
          <option value="stocks">Stocks</option>
          <option value="bonds">Bonds</option>
          <option value="real_estate">Real Estate</option>
          <option value="crypto">Cryptocurrency</option>
        </select>
      </div>
      <div class="input-container">
        <label for="riskLevel">Risk Level</label>
        <select v-model="riskLevel" id="riskLevel" class="input-box">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      <button type="submit" class="submit-button">Submit</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig';

export default {
  data() {
    return {
      investmentType: '',
      riskLevel: '',
    };
  },
  methods: {
    async submitPreferences() {
      try {
        const response = await axiosInstance.post('/account/preferences/', {
          investmentType: this.investmentType,
          riskLevel: this.riskLevel,
        });
        if (response.data.success) {
          window.location.href = '/dashboard';
        }
      } catch (error) {
        console.error('Preferences submission error:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Container styling */
.container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 500px;
  margin: auto;
  margin-top: 50px;
}

/* Title styling */
.title {
  font-size: 22px;
  font-weight: bold;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  margin-bottom: 20px;
}

/* Input box styling */
.input-box {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  margin-bottom: 10px;
}

/* Submit button styling */
.submit-button {
  background-color: #007aff;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #005bb5;
}
</style>