<template>
  <div>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { Chart } from "chart.js";

export default {
  props: ["company"],
  setup(props) {
    const chart = ref(null);
    const chartInstance = ref(null);

    const loadSentimentData = async () => {
      if (!props.company) return;

      const response = await axios.get(`/api/sentiment/${props.company}`);
      const data = response.data;

      if (chartInstance.value) {
        chartInstance.value.destroy();
      }

      chartInstance.value = new Chart(chart.value, {
        type: "line",
        data: {
          labels: data.dates,
          datasets: [{ label: "Sentiment Score", data: data.scores, borderColor: "blue" }],
        },
      });
    };

    watch(() => props.company, loadSentimentData);
    onMounted(loadSentimentData);

    return {
      chart,
    };
  },
};
</script>

<style scoped>
/* Add any necessary styles here */
</style>