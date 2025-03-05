<template>
    <div v-if="esgData">
      <h3>Environmental: {{ esgData.environmental }}</h3>
      <h3>Social: {{ esgData.social }}</h3>
      <h3>Governance: {{ esgData.governance }}</h3>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  import axios from "axios";
  
  const props = defineProps(["company"]);
  const esgData = ref(null);
  
  watch(() => props.company, async () => {
    if (!props.company) return;
    const response = await axios.get(`/api/esg/${props.company}`);
    esgData.value = response.data;
  });
  </script>
  