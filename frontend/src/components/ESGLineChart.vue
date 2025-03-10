<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["data"]);
const chart = ref(null);

onMounted(() => {
  if (!props.data) return;

  new Chart(chart.value, {
    type: "line",
    data: {
      labels: props.data.dates,
      datasets: [
        {
          label: "ESG Score",
          data: props.data.scores,
          borderColor: "#007bff",
          fill: false,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 500px;
  margin: auto;
}
</style>