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
    try {
      const response = await axios.get("/investment-recommendations/"); // Update the URL if necessary
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching investment recommendations:", error);
    }
  };
  
  onMounted(loadSuggestions);
  </script>
