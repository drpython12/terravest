<template>
  <div class="flex flex-col">
    <h2 class="text-lg font-semibold mb-4">KPI-Level Drilldown</h2>
    <ul class="space-y-2">
      <li
        v-for="(value, key) in data"
        :key="key"
        class="flex justify-between text-gray-700"
      >
        <span>{{ key }}</span><span class="font-medium">{{ value }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>