<template>
    <div>
      <h2>Investment Recommendations</h2>
      <p>{{ suggestion }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  
  const suggestion = ref("");
  
  const loadSuggestions = async () => {
    const response = await axios.get("/api/investment-recommendations/");
    suggestion.value = response.data.recommendation;
  };
  
  onMounted(loadSuggestions);
  </script>
  