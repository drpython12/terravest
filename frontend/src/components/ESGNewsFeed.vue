<template>
  <div class="news-container">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Latest ESG News</h3>
    <ul>
      <li v-for="news in newsList" :key="news.uuid" class="mb-4">
        <a :href="news.link" target="_blank" class="text-blue-600 hover:underline">
          {{ news.title }}
        </a>
        <p class="text-sm text-gray-500">{{ news.publisher }}</p>
        <img
          v-if="news.thumbnail"
          :src="news.thumbnail"
          alt="News Thumbnail"
          class="mt-2 rounded-lg"
        />
      </li>
    </ul>
    <p v-if="loading" class="text-gray-500">Loading news...</p>
    <p v-if="!loading && newsList.length === 0" class="text-gray-500">No ESG news available.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const newsList = ref([]);
const loading = ref(true);

const fetchESGNews = async () => {
  try {
    const response = await axios.get("/fetch-esg-news/");
    const newsData = response.data.news || [];
    newsList.value = newsData.map((item) => ({
      uuid: item.uuid,
      title: item.title,
      link: item.link,
      publisher: item.publisher,
      thumbnail: item.thumbnail?.resolutions?.[0]?.url || null,
    }));
    console.log("Fetched ESG news:", newsList.value);
  } catch (error) {
    console.error("Failed to fetch ESG news:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchESGNews);
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
  padding: 10px 0;
  border-bottom: 1px solid #eaeaea;
}

.news-container li:last-child {
  border-bottom: none;
}

.news-container a {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

.news-container a:hover {
  text-decoration: underline;
}

.news-container img {
  max-width: 100%;
  height: auto;
}
</style>