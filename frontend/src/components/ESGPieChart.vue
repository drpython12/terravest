<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["data", "weighting"]);
const chart = ref(null);
let chartInstance = null;

onMounted(() => {
  renderChart();
});

watch(() => props.data, () => {
  if (chartInstance) {
    chartInstance.destroy();
  }
  renderChart();
});

function renderChart() {
  if (!props.data || !props.weighting) return;

  const { environmental, social, governance } = props.data;
  const totalWeight = props.weighting.reduce((acc, w) => acc + w, 0);

  const weightedData = {
    environmental: (environmental.score * props.weighting[0]) / totalWeight,
    social: (social.score * props.weighting[1]) / totalWeight,
    governance: (governance.score * props.weighting[2]) / totalWeight,
  };

  const subcategories = [
    ...environmental.subcategories,
    ...social.subcategories,
    ...governance.subcategories,
  ];

  const subcategoryScores = subcategories.map((sub) => sub.score);
  const subcategoryColors = subcategories.map((sub) => sub.color);

  chartInstance = new Chart(chart.value, {
    type: "doughnut",
    data: {
      labels: ["Environmental", "Social", "Governance", ...subcategories.map((sub) => sub.name)],
      datasets: [
        {
          label: "Main ESG Categories",
          data: [weightedData.environmental, weightedData.social, weightedData.governance],
          backgroundColor: ["#4CAF50", "#FFC107", "#2196F3"],
          borderWidth: 1,
          hoverOffset: 4,
        },
        {
          label: "Subcategories",
          data: subcategoryScores,
          backgroundColor: subcategoryColors,
          borderWidth: 1,
          hoverOffset: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: (tooltipItem) => {
              const datasetIndex = tooltipItem.datasetIndex;
              const dataIndex = tooltipItem.dataIndex;
              if (datasetIndex === 0) {
                return `${tooltipItem.label}: ${tooltipItem.raw.toFixed(2)}%`;
              } else {
                return `${subcategories[dataIndex].name}: ${tooltipItem.raw.toFixed(2)}%`;
              }
            },
          },
        },
      },
    },
  });
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 600px;
  margin: auto;
}
</style>