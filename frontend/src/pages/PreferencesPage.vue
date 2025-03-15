<template>
  <div class="container">
    <h2 class="title">Investor Preferences</h2>
    <form @submit.prevent="submitPreferences">
      <!-- Investment Type -->
      <div class="input-container">
        <label for="investmentType">Preferred Investment Type</label>
        <select v-model="investmentType" id="investmentType" class="input-box">
          <option value="stocks">Stocks</option>
          <option value="bonds">Bonds</option>
          <option value="real_estate">Real Estate</option>
          <option value="crypto">Cryptocurrency</option>
        </select>
      </div>

      <!-- Risk Level -->
      <div class="input-container">
        <label for="riskLevel">Risk Level</label>
        <select v-model="riskLevel" id="riskLevel" class="input-box">
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <!-- Investment Strategy Preference -->
      <div class="input-container">
        <label for="investmentStrategy">Investment Strategy Preference</label>
        <select v-model="investmentStrategy" id="investmentStrategy" class="input-box">
          <option value="impact_investing">🌱 Impact Investing</option>
          <option value="esg_integration">🔍 ESG Integration</option>
          <option value="ethical_screening">🚫 Ethical Screening</option>
          <option value="traditional_esg">📈 Traditional Investing with ESG Consideration</option>
        </select>
      </div>

      <!-- ESG Factor Priority -->
      <div class="input-container">
        <label for="esgFactors">ESG Factor Priority (Select up to 2)</label>
        <div>
          <label><input type="checkbox" v-model="esgFactors" value="environment" /> 🌍 Environment</label>
          <label><input type="checkbox" v-model="esgFactors" value="social" /> 👥 Social</label>
          <label><input type="checkbox" v-model="esgFactors" value="governance" /> 🏛️ Governance</label>
        </div>
      </div>

      <!-- Industry Preferences -->
      <div class="input-container">
        <label for="industryPreferences">Industry Preferences (Optional)</label>
        <div>
          <label><input type="checkbox" v-model="industryPreferences" value="tech_innovation" /> ✅ Tech & Innovation</label>
          <label><input type="checkbox" v-model="industryPreferences" value="renewable_energy" /> ✅ Renewable Energy</label>
          <label><input type="checkbox" v-model="industryPreferences" value="healthcare" /> ✅ Healthcare</label>
          <label><input type="checkbox" v-model="industryPreferences" value="consumer_goods" /> ✅ Consumer Goods</label>
          <label><input type="checkbox" v-model="industryPreferences" value="finance_banking" /> ✅ Finance & Banking</label>
          <label><input type="checkbox" v-model="industryPreferences" value="no_preference" /> ✅ No preference</label>
        </div>
      </div>

      <!-- Exclusions -->
      <div class="input-container">
        <label for="exclusions">Exclusions (Optional)</label>
        <div>
          <label><input type="checkbox" v-model="exclusions" value="fossil_fuels" /> ❌ Fossil Fuels</label>
          <label><input type="checkbox" v-model="exclusions" value="weapons_defense" /> ❌ Weapons & Defense</label>
          <label><input type="checkbox" v-model="exclusions" value="tobacco_alcohol" /> ❌ Tobacco & Alcohol</label>
          <label><input type="checkbox" v-model="exclusions" value="gambling" /> ❌ Gambling</label>
        </div>
      </div>

      <!-- Sentiment Analysis Preference -->
      <div class="input-container">
        <label for="sentimentAnalysis">Sentiment Analysis Preference</label>
        <select v-model="sentimentAnalysis" id="sentimentAnalysis" class="input-box">
          <option value="yes">📊 Yes, consider real-time market & news sentiment</option>
          <option value="no">⚖️ No, rely only on ESG reports & data</option>
        </select>
      </div>

      <!-- Transparency Level -->
      <div class="input-container">
        <label for="transparencyLevel">Transparency Level in Reports</label>
        <select v-model="transparencyLevel" id="transparencyLevel" class="input-box">
          <option value="simple_summary">📑 Simple Summary</option>
          <option value="detailed_breakdown">📋 Detailed Breakdown</option>
        </select>
      </div>

      <!-- Submit Button -->
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
      investmentStrategy: '',
      esgFactors: [],
      industryPreferences: [],
      exclusions: [],
      sentimentAnalysis: '',
      transparencyLevel: '',
    };
  },
  methods: {
    async fetchPreferences() {
      try {
        const response = await axiosInstance.get('/account/preferences/');
        if (response.data.success) {
          const preferences = response.data.preferences;
          this.investmentType = preferences.investment_type || '';
          this.riskLevel = preferences.risk_level || '';
          this.investmentStrategy = preferences.investment_strategy || '';
          this.esgFactors = preferences.esg_factors || [];
          this.industryPreferences = preferences.industry_preferences || [];
          this.exclusions = preferences.exclusions || [];
          this.sentimentAnalysis = preferences.sentiment_analysis || '';
          this.transparencyLevel = preferences.transparency_level || '';
        }
      } catch (error) {
        console.error('Error fetching preferences:', error);
      }
    },
    async submitPreferences() {
      try {
        const response = await axiosInstance.post('/account/preferences/', {
          investmentType: this.investmentType,
          riskLevel: this.riskLevel,
          investmentStrategy: this.investmentStrategy,
          esgFactors: this.esgFactors,
          industryPreferences: this.industryPreferences,
          exclusions: this.exclusions,
          sentimentAnalysis: this.sentimentAnalysis,
          transparencyLevel: this.transparencyLevel,
        });
        if (response.data.success) {
          window.location.href = '/dashboard';
        }
      } catch (error) {
        console.error('Preferences submission error:', error);
      }
    },
  },
  mounted() {
    this.fetchPreferences();
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

/* Checkbox container styling */
.input-container label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  text-align: left;
}
</style>