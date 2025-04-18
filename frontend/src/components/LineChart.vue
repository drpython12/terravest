<template>
  <div class="h-80 w-full bg-gray-100 rounded-lg flex items-center justify-center">
    <canvas ref="lineChart" class="w-full h-full"></canvas>
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
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderWidth: 2,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: "Year",
            },
          },
          y: {
            title: {
              display: true,
              text: "Score",
            },
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