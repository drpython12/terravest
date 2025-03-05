<template>
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>ESG Score</th>
          <th>Industry</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="company in portfolio" :key="company.id">
          <td>{{ company.name }}</td>
          <td>{{ company.esg_score }}</td>
          <td>{{ company.industry }}</td>
          <td><button @click="$emit('select-company', company.name)">View ESG</button></td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script setup>
  defineProps(["portfolio"]);
  </script>
  
  <style scoped>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
  }
  
  button {
    cursor: pointer;
    background-color: #007bff;
    color: white;
    padding: 5px;
    border: none;
  }
  </style>
  