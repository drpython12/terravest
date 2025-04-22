<template>
  <div class="space-y-8">
    <!-- Heatmap Section -->
    <section class="bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-lg font-semibold mb-4 text-center">Controversies Heatmap</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left border-collapse">
          <thead>
            <tr class="border-b">
              <th class="py-2 px-4">Field</th>
              <th v-for="year in Object.keys(controversyData)" :key="year" class="py-2 px-4 text-center">
                {{ year }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in sortedCategories" :key="category" class="border-b">
              <td class="py-2 px-4 font-medium">
                {{ formatFieldName(category) }}
              </td>
              <td
                v-for="year in Object.keys(controversyData)"
                :key="year"
                class="py-2 px-4 text-center"
                :class="getHeatmapColor(controversyData[year]?.[category]?.valuescore)"
              >
                <template v-if="category === 'ESGCControversiesScore'">
                  {{ controversyData[year]?.[category]?.value || 'N/A' }}
                </template>
                <template v-else-if="category === 'ControversiesScore'">
                  {{ controversyData[year]?.[category]?.valuescore || 'N/A' }}
                </template>
                <template v-else>
                  <template v-if="controversyData[year]?.[category]?.value === true">
                    Yes
                  </template>
                  <template v-else-if="controversyData[year]?.[category]?.value === false">
                    No
                  </template>
                  <template v-else>
                    {{ controversyData[year]?.[category]?.value || 'N/A' }}
                  </template>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Analysis Section -->
    <section class="bg-white shadow-lg rounded-2xl p-6">
      <h2 class="text-lg font-semibold mb-4 text-center">Controversies Analysis</h2>
      <ul class="space-y-4">
        <li v-for="(yearData, year) in controversyData" :key="year" class="border-b pb-4">
          <h3 class="font-semibold text-gray-800">Year: {{ year }}</h3>
          <ul class="space-y-2">
            <li
              v-for="(data, category) in yearData"
              :key="category"
              class="flex justify-between text-gray-700"
            >
              <span>{{ formatFieldName(category) }}</span>
              <span class="font-medium">
                {{ data.value === true ? "Yes" : data.value === false ? "No" : data.value || "N/A" }}
                <span v-if="data.valuescore">({{ data.valuescore }}%)</span>
              </span>
            </li>
          </ul>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { computed } from "vue";

// Props
defineProps({
  controversyData: {
    type: Object,
    required: true,
  },
  controversyCategories: {
    type: Array,
    required: true,
  },
});

// Heatmap color logic
const getHeatmapColor = (score) => {
  if (score === null || score === undefined) return "bg-gray-200";
  if (score >= 75) return "bg-green-500 text-white";
  if (score >= 50) return "bg-yellow-400 text-gray-800";
  if (score >= 25) return "bg-orange-400 text-white";
  return "bg-red-500 text-white";
};

// Format field name
const formatFieldName = (fieldName) => {
  // Remove "Count" from field names and add spaces between camel case words
  return fieldName.replace(/Count$/, "").replace(/([a-z])([A-Z])/g, "$1 $2");
};

// Filter and sort categories
const sortedCategories = computed(() => {
  if (!Array.isArray(controversyCategories)) {
    console.error("controversyCategories is not an array or is undefined.");
    return [];
  }

  // Sort categories alphabetically
  return controversyCategories.sort((a, b) => a.localeCompare(b));
});
</script>

<style scoped>
h2 {
  color: #374151; /* Tailwind gray-800 */
}
</style>