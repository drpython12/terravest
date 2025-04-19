<template>
  <div class="chart-container relative">
    <canvas ref="lineChart"></canvas>
    <div v-if="hoveredDataset" class="legend-container absolute top-0 left-0 p-2 bg-white shadow-lg rounded-lg">
      <p class="text-sm font-medium" :style="{ color: hoveredDataset.color }">
        {{ hoveredDataset.label }}
      </p>
    </div>
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

const lineChart = ref(null);
let chartInstance = null;
const hoveredDataset = ref(null); // Track the hovered dataset

const roundToNearestFive = (value) => Math.round(value / 5) * 5;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  const allScores = [
    ...(props.data.scores || []),
    ...(props.data.environmentalScores || []),
    ...(props.data.socialScores || []),
    ...(props.data.governanceScores || []),
  ];

  const rawMinScore = Math.min(...allScores) - 5;
  const rawMaxScore = Math.max(...allScores) + 5;

  const minScore = roundToNearestFive(rawMinScore > 0 ? rawMinScore : 0);
  const maxScore = roundToNearestFive(rawMaxScore);

  chartInstance = new Chart(lineChart.value, {
    type: "line",
    data: {
      labels: props.data.labels,
      datasets: [
        {
          label: "ESG Score",
          data: props.data.scores,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: "rgba(75, 192, 192, 1)",
          tension: 0.4,
        },
        {
          label: "Environmental Score",
          data: props.data.environmentalScores,
          borderColor: "rgba(54, 162, 235, 1)",
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: "rgba(54, 162, 235, 1)",
          tension: 0.4,
        },
        {
          label: "Social Score",
          data: props.data.socialScores,
          borderColor: "rgba(255, 206, 86, 1)",
          backgroundColor: "rgba(255, 206, 86, 0.2)",
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 206, 86, 1)",
          tension: 0.4,
        },
        {
          label: "Governance Score",
          data: props.data.governanceScores,
          borderColor: "rgba(255, 99, 132, 1)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderWidth: 3,
          pointRadius: 5,
          pointBackgroundColor: "rgba(255, 99, 132, 1)",
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false, // Hide the default legend
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Year",
          },
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
          },
        },
        y: {
          beginAtZero: minScore === 0,
          min: minScore,
          max: maxScore,
          title: {
            display: true,
            text: "Score",
          },
          grid: {
            color: "rgba(200, 200, 200, 0.2)",
          },
        },
      },
      onHover: (event, elements) => {
        if (elements.length > 0) {
          const datasetIndex = elements[0].datasetIndex;
          const dataset = chartInstance.data.datasets[datasetIndex];
          hoveredDataset.value = {
            label: dataset.label,
            color: dataset.borderColor,
          };
        } else {
          hoveredDataset.value = null; // Clear the legend when not hovering
        }
      },
    },
  });
};

onMounted(() => {
  renderChart();
});

watch(() => props.data, renderChart);
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 400px;
  max-width: 600px;
  margin: auto;
  position: relative;
}

.legend-container {
  z-index: 10;
  pointer-events: none; /* Prevent interference with hover events */
}
</style>