<template>
  <div class="flex min-h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md p-5">
      <h1 class="text-2xl font-bold text-blue-800 mb-8">BioLab IPS</h1>
      <nav class="space-y-4">
        <router-link to="/" class="block text-gray-700 hover:text-blue-600 font-medium">
          Inicio
        </router-link>
        <router-link to="/pacientes" class="block text-gray-700 hover:text-blue-600 font-medium">
          Pacientes
        </router-link>
        <router-link to="/resultados" class="block text-gray-700 hover:text-blue-600 font-medium">
          Ingreso Resultados
        </router-link>
        <router-link to="/especialistas" class="block text-gray-700 hover:text-blue-600 font-medium">
          Especialistas
        </router-link>
      </nav>
    </aside>

    <!-- Contenido principal -->
    <main class="flex-1 p-10">
      <router-view />
    </main>
  </div>
</template>
