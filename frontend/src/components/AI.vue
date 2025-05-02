<template>
  <div class="w-full p-6 bg-white shadow-xl rounded-2xl space-y-6">
    <h1 class="text-2xl font-semibold text-gray-800">AI ESG Report</h1>

    <!-- Loading -->
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
      Generating ESG analysis... Please wait.
    </div>

    <!-- Error -->
    <div v-if="error" class="bg-red-100 text-red-700 px-4 py-2 rounded-lg">
      {{ error }}
    </div>

    <!-- Insight Display -->
    <div v-if="insight" class="space-y-6 text-gray-800">
      <!-- Summary -->
      <section>
        <h2 class="text-lg font-semibold">Summary</h2>
        <p>{{ insight.summary || "No summary available." }}</p>
      </section>

      <!-- ESG Scores -->
      <section>
        <h2 class="text-lg font-semibold">ESG Scores</h2>
        <ul class="space-y-2">
          <li>
            <strong>Environmental:</strong> {{ insight.esgScores.Environmental.score }} - 
            {{ insight.esgScores.Environmental.interpretation }}
          </li>
          <li>
            <strong>Social:</strong> {{ insight.esgScores.Social.score }} - 
            {{ insight.esgScores.Social.interpretation }}
          </li>
          <li>
            <strong>Governance:</strong> {{ insight.esgScores.Governance.score }} - 
            {{ insight.esgScores.Governance.interpretation }}
          </li>
          <li>
            <strong>Overall:</strong> {{ insight.esgScores.Overall.score }} - 
            {{ insight.esgScores.Overall.interpretation }}
          </li>
        </ul>
      </section>

      <!-- Controversies -->
      <section>
        <h2 class="text-lg font-semibold">Controversies</h2>
        <p>{{ insight.controversies.details || "No controversies reported." }}</p>
        <p class="text-gray-600">{{ insight.controversies.interpretation }}</p>
      </section>

      <!-- Alignment with Preferences -->
      <section>
        <h2 class="text-lg font-semibold">Alignment with Preferences</h2>
        <p><strong>Strategy:</strong> {{ insight.alignment.strategy }}</p>
        <div>
          <strong>Strengths:</strong>
          <ul class="list-disc ml-6">
            <li v-for="strength in insight.alignment.strengths" :key="strength">
              {{ strength }}
            </li>
          </ul>
        </div>
        <div>
          <strong>Risks:</strong>
          <ul class="list-disc ml-6">
            <li v-for="risk in insight.alignment.risks" :key="risk">
              {{ risk }}
            </li>
          </ul>
        </div>
        <p><strong>Conclusion:</strong> {{ insight.alignment.conclusion }}</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "AIInsight",
  props: {
    insight: {
      type: Object,
      default: null,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: null,
    },
  },
};
</script>