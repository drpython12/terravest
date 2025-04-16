<template>
  <div class="h-40 w-full bg-gray-100 rounded-lg flex items-center justify-center">
    <canvas ref="lineChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const lineChart = ref(null);

const renderChart = () => {
  if (lineChart.value) {
    new Chart(lineChart.value, {
      type: "line",
      data: {
        labels: props.data.labels,
        datasets: [
          {
            label: "ESG Score",
            data: props.data.scores,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 2,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
};

onMounted(() => {
  renderChart();
});
</script>