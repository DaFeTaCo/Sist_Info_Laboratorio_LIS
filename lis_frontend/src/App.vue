<template>
  <div class="dashboard-container">
    <Sidebar class="sidebar" />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.dashboard-container {
  display: block;
}

.main-content {
  margin-left: 90px;
  width: calc(100vw - 220px);
  height: 100vh;
  padding: 40px;
  background-color: #f4f7f6;
  overflow-y: auto;
}
</style>

<style>
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, sans-serif;
  background-color: #f4f7f6;
}
</style>
