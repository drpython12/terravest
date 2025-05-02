<template>
  <div class="w-full p-6 bg-white shadow-xl rounded-2xl space-y-6">
    <h2 class="text-2xl font-semibold text-gray-800 text-center">Controversies Heatmap</h2>

    <!-- Loading Spinner (matches AI.vue) -->
    <div v-if="loading" class="text-center py-4 text-gray-500">
      <svg
        class="animate-spin h-5 w-5 text-gray-500 mx-auto mb-2"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8v8H4z"
        ></path>
      </svg>
      Loading controversies data...
    </div>

    <!-- No Data Message -->
    <div v-else-if="!hasData" class="text-center py-4 text-gray-500 text-lg">
      No controversy data available.
    </div>

    <!-- Heatmap Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm text-left border-collapse">
        <thead>
          <tr class="border-b">
            <th class="py-2 px-4">Category</th>
            <th
              v-for="year in sortedYears"
              :key="year"
              class="py-2 px-4 text-center"
            >
              {{ year }}
            </th>
            <th class="py-2 px-4 text-center font-bold">Total</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="category in sortedCategories"
            :key="category"
            class="border-b"
          >
            <td class="py-2 px-4 font-medium">
              {{ formatFieldName(category) }}
            </td>
            <td
              v-for="year in sortedYears"
              :key="year"
              class="py-2 px-4 text-center"
              :class="getHeatmapColor(getValueScore(year, category))"
            >
              {{ getDisplayValue(year, category) }}
            </td>
            <!-- Row total -->
            <td class="py-2 px-4 text-center font-bold">
              {{ getCategoryTotal(category) }}
            </td>
          </tr>
          <!-- Column totals row -->
          <tr class="border-t font-bold">
            <td class="py-2 px-4">Total</td>
            <td
              v-for="year in sortedYears"
              :key="year"
              class="py-2 px-4 text-center"
            >
              {{ getYearTotal(year) }}
            </td>
            <td class="py-2 px-4 text-center">
              {{ grandTotal }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";

const props = defineProps({
  controversyData: { type: Object, required: true },
  controversyCategories: { type: Array, required: true },
  loading: { type: Boolean, default: false }
});

// Get all years sorted ascending
const sortedYears = computed(() => {
  return Object.keys(props.controversyData)
    .map(Number)
    .sort((a, b) => a - b)
    .map(String);
});

// Sort categories alphabetically
const sortedCategories = computed(() => {
  return [...props.controversyCategories].sort((a, b) => a.localeCompare(b));
});

// Check if there is any data
const hasData = computed(() => {
  return (
    Object.keys(props.controversyData).length > 0 &&
    props.controversyCategories.length > 0 &&
    sortedYears.value.length > 0 &&
    sortedCategories.value.length > 0
  );
});

// Get value or 0 if missing
const getValueScore = (year, category) => {
  const yearData = props.controversyData[year] || {};
  const entry = yearData[category];
  if (!entry || entry.value === undefined || entry.value === null) return 0;
  return entry.value;
};

// Get display value (show 0 if missing)
const getDisplayValue = (year, category) => {
  const yearData = props.controversyData[year] || {};
  const entry = yearData[category];
  if (!entry || entry.value === undefined || entry.value === null) return 0;
  if (typeof entry.value === "boolean") return entry.value ? "Yes" : "No";
  return entry.value;
};

// Row total
const getCategoryTotal = (category) => {
  return sortedYears.value.reduce((sum, year) => sum + Number(getValueScore(year, category)), 0);
};

// Column total
const getYearTotal = (year) => {
  return sortedCategories.value.reduce((sum, category) => sum + Number(getValueScore(year, category)), 0);
};

// Grand total
const grandTotal = computed(() => {
  return sortedCategories.value.reduce(
    (catSum, category) => catSum + getCategoryTotal(category),
    0
  );
});

// Heatmap color logic (higher = worse = red)
const allScores = computed(() => {
  const scores = [];
  for (const year of sortedYears.value) {
    for (const category of sortedCategories.value) {
      scores.push(Number(getValueScore(year, category)));
    }
  }
  return scores.filter((v) => typeof v === "number");
});
const minScore = computed(() => Math.min(...allScores.value));
const maxScore = computed(() => Math.max(...allScores.value));

const getHeatmapColor = (score) => {
  if (score === null || score === undefined || score === 0) return "bg-gray-200 text-gray-700";
  if (maxScore.value === minScore.value) return "bg-gray-200 text-gray-700";
  // Normalize so higher = worse (red)
  const norm = (score - minScore.value) / (maxScore.value - minScore.value);
  if (norm > 0.8) return "bg-red-700 text-white";
  if (norm > 0.6) return "bg-orange-500 text-white";
  if (norm > 0.4) return "bg-yellow-300 text-gray-900";
  return "bg-green-400 text-gray-900";
};

// Format field name for display
const formatFieldName = (fieldName) => {
  return fieldName.replace(/Count$/, "").replace(/([a-z])([A-Z])/g, "$1 $2");
};
</script>

<style scoped>
h2 {
  color: #374151;
}
</style>