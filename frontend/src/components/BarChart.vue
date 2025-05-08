<template>
  <div class="chart-container relative">
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const barChart = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy(); // Destroy the previous instance to avoid duplication
  }

  chartInstance = new Chart(barChart.value, {
    type: "bar",
    data: {
      labels: props.data.labels,
      datasets: [
        {
          label: "Company Scores",
          data: props.data.companyScores,
          backgroundColor: "rgba(54, 162, 235, 0.6)",
        },
        {
          label: "Industry Benchmark",
          data: props.data.benchmarkScores,
          backgroundColor: "rgba(255, 99, 132, 0.6)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // Allow the chart to fill the container
      plugins: {
        legend: {
          position: "top",
        },
      },
      scales: {
        x: {
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
          },
        },
      },
    },
  });
};

onMounted(() => {
  renderChart();
});

watch(
  () => props.data,
  () => {
    renderChart(); // Re-render the chart when data changes
  }
);
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  max-width: 600px; /* Optional: Set a max width */
  margin: auto;
  position: relative;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>