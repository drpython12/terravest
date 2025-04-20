<template>
  <div class="flex flex-col">
    <h2 class="text-lg font-semibold mb-4">KPI-Level Drilldown</h2>
    <ul class="space-y-4">
      <li
        v-for="(metric, key) in data || {}"
        :key="key"
        class="border-b pb-2"
      >
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <span
              class="w-4 h-4 rounded-full mr-2"
              :style="{ backgroundColor: metric?.color || '#ccc' }"
            ></span>
            <span class="font-semibold">{{ key }}</span>
          </div>
          <div class="flex items-center">
            <span class="font-medium">{{ metric?.score || 0 }}</span>
          </div>
        </div>
        <ul
          v-if="metric?.details"
          class="mt-2 space-y-1 pl-6 text-gray-700"
        >
          <li
            v-for="(subValue, subKey) in metric.details"
            :key="subKey"
            class="flex justify-between"
          >
            <span>{{ subKey }}</span>
            <span class="font-medium">{{ subValue || 0 }}</span>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    default: () => ({}),
  },
});
</script>