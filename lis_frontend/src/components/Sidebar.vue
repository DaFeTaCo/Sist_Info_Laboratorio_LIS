<template>
  <div class="sidebar">
    <h2>Menú</h2>
    <nav>
      <router-link to="/inicio" class="sidebar-link" exact>Inicio</router-link>
      <router-link to="/pacientes" class="sidebar-link">Pacientes</router-link>
      <router-link to="/laboratoristas" class="sidebar-link">Laboratoristas</router-link>
      <router-link to="/resultados" class="sidebar-link">Resultados</router-link>
      <!-- puedes seguir agregando más -->
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 240px;
  background-color: #2c3e50;
  color: white;
  padding: 20px;
  min-height: 100vh;
}

.sidebar h2 {
  font-size: 1.4em;
  margin-bottom: 1em;
}

.sidebar-link {
  display: block;
  color: white;
  text-decoration: none;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  transition: background 0.3s;
}

.sidebar-link:hover {
  background: #34495e;
}

.router-link-active {
  background: #1abc9c;
}
</style>
