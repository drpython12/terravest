<template>
  <div class="bg-white shadow-lg rounded-2xl p-6 space-y-6">
    <h2 class="text-lg font-semibold mb-4">AI-Generated ESG Insights</h2>

    <div v-if="loading" class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
      Generating AI Summary...
    </div>

    <div v-else-if="insight" class="space-y-6">
      <!-- ESG Scores -->
      <section>
        <h3 class="text-xl font-bold text-gray-800">ESG Scores</h3>
        <div class="space-y-4">
          <div v-for="(score, key) in insight.esgScores" :key="key" class="space-y-2">
            <div class="flex justify-between">
              <span class="font-medium text-gray-700">{{ key }}</span>
              <span class="font-semibold text-gray-900">{{ score.score.toFixed(2) }} / 100</span>
            </div>
            <p class="text-sm text-gray-600">{{ score.interpretation }}</p>
          </div>
        </div>
      </section>

      <!-- Controversies -->
      <section>
        <h3 class="text-xl font-bold text-gray-800">Controversies</h3>
        <p class="text-gray-700">{{ insight.controversies.details }}</p>
        <p class="text-sm text-gray-600">{{ insight.controversies.interpretation }}</p>
      </section>

      <!-- Alignment with Strategy -->
      <section>
        <h3 class="text-xl font-bold text-gray-800">Alignment with {{ insight.alignment.strategy }}</h3>
        <div class="space-y-4">
          <h4 class="font-semibold text-gray-700">Key Strengths:</h4>
          <ul class="list-disc pl-6 text-gray-700 space-y-2">
            <li v-for="point in insight.alignment.strengths" :key="point">{{ point }}</li>
          </ul>
          <h4 class="font-semibold text-gray-700">Potential Risks:</h4>
          <ul class="list-disc pl-6 text-gray-700 space-y-2">
            <li v-for="point in insight.alignment.risks" :key="point">{{ point }}</li>
          </ul>
          <h4 class="font-semibold text-gray-700">Conclusion:</h4>
          <p class="text-gray-700">{{ insight.alignment.conclusion }}</p>
        </div>
      </section>

      <!-- Summary -->
      <section>
        <h3 class="text-xl font-bold text-gray-800">Summary</h3>
        <p class="text-gray-700">{{ insight.summary }}</p>
      </section>
    </div>

    <div v-else class="h-full w-full bg-gray-100 rounded-lg flex items-center justify-center text-gray-400">
      AI Summary not available.
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

defineProps({
  insight: {
    type: Object,
    default: () => ({
      esgScores: {},
      controversies: { details: "", interpretation: "" },
      alignment: { strategy: "", strengths: [], risks: [], conclusion: "" },
      summary: "",
    }),
  },
  loading: {
    type: Boolean,
    default: true,
  },
});
</script>

<style scoped>
h2 {
  color: #374151; /* Tailwind gray-800 */
}

h3 {
  color: #1f2937; /* Tailwind gray-900 */
}

h4 {
  color: #374151; /* Tailwind gray-800 */
}

p {
  color: #4b5563; /* Tailwind gray-700 */
}
</style>