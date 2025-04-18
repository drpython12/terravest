<template>
  <div class="h-80 w-full bg-gray-100 rounded-lg flex items-center justify-center">
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
        maintainAspectRatio: false,
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