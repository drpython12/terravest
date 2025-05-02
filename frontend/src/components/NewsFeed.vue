<template>
  <div class="news-container">
    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center py-4 text-gray-500">
      <svg
        class="animate-spin h-5 w-5 text-gray-500 mx-auto mb-2"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8H4z"
        ></path>
      </svg>
      Loading latest news...
    </div>
    <!-- News List -->
    <ul v-else-if="newsList.length">
      <li v-for="(news, index) in newsList" :key="index" class="mb-4">
        <a :href="news.url" target="_blank" class="text-blue-600 hover:underline">
          {{ news.title }}
        </a>
        <p class="text-sm text-gray-500">
          Source: {{ news.source }} | Published: {{ news.publishedAt }}
        </p>
      </li>
    </ul>
    <p v-else class="text-gray-500">No news available.</p>
  </div>
</template>

<script setup>
defineProps({
  newsList: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
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