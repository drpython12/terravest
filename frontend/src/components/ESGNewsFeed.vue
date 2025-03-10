<template>
    <div class="news-container">
      <h3>Latest ESG News</h3>
      <ul>
        <li v-for="news in newsList" :key="news.id">
          <a :href="news.url" target="_blank">{{ news.title }}</a>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  
  const newsList = ref([]);
  
  const fetchNews = async () => {
    try {
      const response = await axios.get("/api/esg-news");
      newsList.value = response.data;
    } catch (error) {
      console.error("Failed to fetch ESG news:", error);
    }
  };
  
  onMounted(fetchNews);
  </script>
  
  <style scoped>
  .news-container {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  }
  
  .news-container ul {
    list-style: none;
    padding: 0;
  }
  
  .news-container li {
    padding: 10px;
    border-bottom: 1px solid #eaeaea;
  }
  
  .news-container a {
    text-decoration: none;
    color: #007bff;
    font-weight: bold;
  }
  
  .news-container a:hover {
    text-decoration: underline;
  }
  </style>