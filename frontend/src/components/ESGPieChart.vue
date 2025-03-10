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
    type: "pie",
    data: {
      labels: ["Environmental", "Social", "Governance"],
      datasets: [
        {
          data: [props.data.environmental, props.data.social, props.data.governance],
          backgroundColor: ["#4CAF50", "#FFC107", "#2196F3"],
          borderWidth: 1,
        },
      ],
    },
  });
});
</script>

<style scoped>
.chart-container {
  width: 100%;
  max-width: 400px;
  margin: auto;
}
</style>