<template>
  <div class="dashboard-container">
    <Sidebar />
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
  display: flex;
  height: 100vh;
  width: 100vw; /* ✅ Usa todo el ancho de la ventana */
  overflow: hidden;
}

.main-content {
  flex-grow: 1;
  padding: 40px;
  background-color: #f4f7f6;
  overflow-y: auto;
}
</style>
