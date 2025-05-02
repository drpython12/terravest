<template>
  <div class="news-container">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">Latest ESG News</h3>
    <ul v-if="newsList.length">
      <li v-for="(news, index) in newsList" :key="index" class="mb-4">
        <a :href="news.url" target="_blank" class="text-blue-600 hover:underline">
          {{ news.title }}
        </a>
        <p class="text-sm text-gray-500">
          Source: {{ news.source }} | Published: {{ news.publishedAt }}
        </p>
      </li>
    </ul>
    <p v-else class="text-gray-500">No ESG news available.</p>
  </div>
</template>

<script setup>
defineProps({
  newsList: {
    type: Array,
    required: true,
  },
});
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