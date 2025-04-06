<template>
  <div class="chart-container">
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["data"]);
const chart = ref(null);
let chartInstance = null;

// Utility function to round to the nearest 5
const roundToNearestFive = (value) => Math.round(value / 5) * 5;

const createChart = () => {
  if (chartInstance) {
    chartInstance.destroy(); // Destroy the previous chart instance
  }

  // Flatten all score values to calculate min and max dynamically
  const allScores = [
    ...(props.data?.ESGScore?.map((item) => item.score) || []),
    ...(props.data?.EnvironmentPillarScore?.map((item) => item.score) || []),
    ...(props.data?.SocialPillarScore?.map((item) => item.score) || []),
    ...(props.data?.GovernancePillarScore?.map((item) => item.score) || []),
  ];

  // Calculate dynamic min and max values for the Y-axis
  const rawMinScore = Math.min(...allScores) - 5; // Add padding below the minimum score
  const rawMaxScore = Math.max(...allScores) + 5; // Add padding above the maximum score

  const minScore = roundToNearestFive(rawMinScore > 0 ? rawMinScore : 0); // Ensure the minimum value is at least 0
  const maxScore = roundToNearestFive(rawMaxScore);

  const labels = props.data?.ESGScore?.map((item) => item.year) || [];
  chartInstance = new Chart(chart.value, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "ESG Score",
          data: props.data?.ESGScore?.map((item) => item.score) || [],
          borderColor: "#007bff",
          fill: false,
          tension: 0.3,
        },
        {
          label: "Environmental Score",
          data: props.data?.EnvironmentPillarScore?.map((item) => item.score) || [],
          borderColor: "#28a745",
          fill: false,
          tension: 0.3,
        },
        {
          label: "Social Score",
          data: props.data?.SocialPillarScore?.map((item) => item.score) || [],
          borderColor: "#ffc107",
          fill: false,
          tension: 0.3,
        },
        {
          label: "Governance Score",
          data: props.data?.GovernancePillarScore?.map((item) => item.score) || [],
          borderColor: "#dc3545",
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
          beginAtZero: minScore === 0, // Start at 0 if the minimum score is 0
          min: minScore, // Set the rounded minimum value
          max: maxScore, // Set the rounded maximum value
        },
      },
    },
  });
};

onMounted(() => {
  if (props.data) {
    createChart();
  }
});

watch(() => props.data, createChart);
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 500px;
  height: 400px; /* Adjust the height of the chart */
  margin: auto;
}
</style>