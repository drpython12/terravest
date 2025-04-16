<template>
  <div class="h-40 w-full bg-gray-100 rounded-lg flex items-center justify-center">
    <canvas ref="radarChart"></canvas>
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
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          r: {
            suggestedMin: 0,
            suggestedMax: 100,
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