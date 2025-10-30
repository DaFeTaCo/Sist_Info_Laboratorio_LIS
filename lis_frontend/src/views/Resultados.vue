<template>
  <div class="dashboard-container">
    <main class="main-content">
      <header class="header">
        <h1><span>BioLab</span> Resultados de Laboratorio</h1>
      </header>

      <!-- Barra de búsqueda -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="Buscar por código de ingreso"
          v-model="busqueda"
        />
      </div>

      <!-- Tabla -->
      <div class="form-container">
        <h2>Listado de Resultados ({{ resultadosFiltrados.length }} registros)</h2>

        <div v-if="cargando">Cargando resultados...</div>

        <table v-else>
          <thead>
            <tr>
              <th>ID</th>
              <th>Código Ingreso</th>
              <th>Colesterol Total</th>
              <th>Colesterol HDL</th>
              <th>Colesterol LDL</th>
              <th>Triglicéridos</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in resultadosFiltrados" :key="r.id">
              <td>{{ r.id }}</td>
              <td>{{ r.codigo_ingreso }}</td>
              <td>{{ r.colesterol_total }}</td>
              <td>{{ r.colesterol_hdl }}</td>
              <td>{{ r.colesterol_ldl }}</td>
              <td>{{ r.trigliceridos }}</td>
              <td>
                <button class="btn btn-edit" @click="editarResultado(r)">Editar</button>
                <button class="btn btn-delete" @click="eliminarResultado(r.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="resultadosFiltrados.length === 0" class="no-data">
          No se encontraron resultados.
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const resultados = ref([])
const busqueda = ref('')
const cargando = ref(true)

// 🔹 Cargar lista de resultados
const cargarResultados = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/resultados/')
    resultados.value = response.data.resultados || response.data
  } catch (error) {
    console.error('Error al cargar resultados:', error)
  } finally {
    cargando.value = false
  }
}

// 🔹 Computed: filtro de búsqueda
const resultadosFiltrados = computed(() => {
  if (!busqueda.value) return resultados.value
  const b = busqueda.value.toLowerCase()
  return resultados.value.filter(r =>
    r.codigo_ingreso.toLowerCase().includes(b)
  )
})

// 🔹 Editar resultado
const editarResultado = (resultado) => {
  alert(`Editar resultado ID: ${resultado.id}`)
}

// 🔹 Eliminar resultado
const eliminarResultado = async (id) => {
  if (confirm('¿Seguro que deseas eliminar este resultado?')) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/resultados/${id}/`)
      alert('Resultado eliminado correctamente')
      await cargarResultados()
    } catch (error) {
      console.error('Error al eliminar resultado:', error)
    }
  }
}

onMounted(cargarResultados)
</script>

<style scoped>
/* Reutiliza el mismo estilo de Pacientes.vue */
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #f4f7f6;
}
.main-content {
  flex-grow: 1;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
}
.header h1 {
  font-size: 2em;
  color: #2c3e50;
}
.header h1 span {
  color: #1abc9c;
}
.search-bar input {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  width: 100%;
  font-size: 1em;
  outline: none;
}
.form-container {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-width: 1300px;
  margin: 2 auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
thead {
  background-color: #1abc9c;
  color: white;
}
th, td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  color: #000;
}
tr:hover {
  background-color: #f9f9f9;
}
.btn {
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  margin-right: 5px;
}
.btn-edit {
  background-color: #3498db;
  color: white;
}
.btn-edit:hover {
  background-color: #2980b9;
}
.btn-delete {
  background-color: #e74c3c;
  color: white;
}
.btn-delete:hover {
  background-color: #c0392b;
}
.no-data {
  text-align: center;
  padding: 20px;
  color: #777;
}
</style>
