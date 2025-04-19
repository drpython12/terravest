<template>
  <div class="flex items-center justify-center w-full h-full">
    <canvas ref="radarChart" class="w-full h-full"></canvas>
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

const radarChart = ref(null);

const renderChart = () => {
  if (radarChart.value) {
    new Chart(radarChart.value, {
      type: "radar",
      data: {
        labels: ["Environmental", "Social", "Governance"],
        datasets: [
          {
            label: "ESG Pillar Scores",
            data: [props.data.environmental, props.data.social, props.data.governance],
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true, // Dynamically adjust aspect ratio
        scales: {
          r: {
            ticks: {
              display: true,
              backdropColor: "transparent",
            },
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

<style scoped>
/* Ensure the container dynamically adjusts */
canvas {
  max-width: 100%;
  max-height: 100%;
}
</style>