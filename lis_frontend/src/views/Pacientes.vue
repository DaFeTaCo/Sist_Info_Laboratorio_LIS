<template>
  <div class="dashboard-container">

    <!-- Contenido principal -->
    <main class="main-content">
      <header class="header">
        <h1><span>BioLab</span> Pacientes Registrados</h1>
      </header>

      <!-- Barra de búsqueda -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="Buscar por nombre o documento"
          v-model="busqueda"
        />
      </div>

      <!-- Tabla -->
      <div class="form-container">
        <h2>Listado de Pacientes ({{ pacientesFiltrados.length }} registros)</h2>

        <div v-if="cargando">Cargando pacientes...</div>

        <table v-else>
          <thead>
            <tr>
              <th>ID</th>
              <th>Código Ingreso</th>
              <th>Documento</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Dirección</th>
              <th>Teléfono</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in pacientesFiltrados" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.codigo_ingreso }}</td>
              <td>{{ p.documento }}</td>
              <td>{{ p.nombre }}</td>
              <td>{{ p.apellido }}</td>
              <td>{{ p.direccion }}</td>
              <td>{{ p.telefono }}</td>
              <td>
                <button class="btn btn-edit" @click="editarPaciente(p)">Editar</button>
                <button class="btn btn-delete" @click="eliminarPaciente(p.id)">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-if="pacientesFiltrados.length === 0" class="no-data">
          No se encontraron pacientes.
        </div>
      </div>

      <!-- Crear nuevo paciente -->
      <div class="action-section">
        <h3>Agregar nuevo paciente</h3>
        <form @submit.prevent="crearPaciente" class="form-inline">
          <input v-model="nuevoPaciente.codigo_ingreso" placeholder="Código ingreso" required />
          <input v-model="nuevoPaciente.documento" placeholder="Documento" required />
          <input v-model="nuevoPaciente.nombre" placeholder="Nombre" required />
          <input v-model="nuevoPaciente.apellido" placeholder="Apellido" required />
          <input v-model="nuevoPaciente.direccion" placeholder="Dirección" />
          <input v-model="nuevoPaciente.telefono" placeholder="Teléfono" />
          <button class="btn btn-green" type="submit">Agregar</button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const pacientes = ref([])
const busqueda = ref('')
const cargando = ref(true)
const nuevoPaciente = ref({
  codigo_ingreso: '',
  documento: '',
  nombre: '',
  apellido: '',
  direccion: '',
  telefono: ''
})

// 🔹 Cargar lista de pacientes
const cargarPacientes = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/pacientes/')
    pacientes.value = response.data.pacientes || response.data
  } catch (error) {
    console.error('Error al cargar pacientes:', error)
  } finally {
    cargando.value = false
  }
}

// 🔹 Computed: filtro de búsqueda
const pacientesFiltrados = computed(() => {
  if (!busqueda.value) return pacientes.value
  const b = busqueda.value.toLowerCase()
  return pacientes.value.filter(p =>
    p.nombre.toLowerCase().includes(b) ||
    p.apellido.toLowerCase().includes(b) ||
    p.documento.toLowerCase().includes(b)
  )
})

// 🔹 Crear paciente nuevo
const crearPaciente = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/pacientes/', nuevoPaciente.value)
    alert('Paciente agregado exitosamente')
    Object.keys(nuevoPaciente.value).forEach(k => nuevoPaciente.value[k] = '')
    await cargarPacientes()
  } catch (error) {
    console.error('Error al crear paciente:', error)
  }
}

// 🔹 Editar paciente 
const editarPaciente = (paciente) => {
  alert(`Editar paciente ID: ${paciente.id}`)
  // Aquí luego puedes abrir un formulario o redirigir a /editar/:id
}

// 🔹 Eliminar paciente
const eliminarPaciente = async (id) => {
  if (confirm('¿Seguro que deseas eliminar este paciente?')) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/pacientes/${id}/`)
      alert('Paciente eliminado correctamente')
      await cargarPacientes()
    } catch (error) {
      console.error('Error al eliminar paciente:', error)
    }
  }
}

onMounted(cargarPacientes)
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
  background-color: #f4f7f6;
}

/* Contenido principal */
.main-content {
  flex-grow: 1;
  padding: 30px;
  max-width: 1400px; 
  margin: 0 auto;
}

/* Header */
.header {
  margin-bottom: 20px;
}

.header h1 {
  font-size: 2em;
  color: #2c3e50;
}

.header h1 span {
  color: #1abc9c;
  margin-right: 10px;
}

/* Buscador */
.search-bar {
  margin-bottom: 20px;
  display: flex;
}

.search-bar input {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 20px;
  width: 100%;
  font-size: 1em;
  outline: none;
}

/* Tabla */
.form-container {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-width: 1300px; /* Ajuste del ancho máximo  */
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

/* Acciones */
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

.btn-green {
  background-color: #27ae60;
  color: white;
}

.btn-green:hover {
  background-color: #2ecc71;
}

.action-section {
  margin-top: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.form-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.form-inline input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #777;
}

.content {
  width: 90%; /* ✅ asegura que use todo el espacio disponible */
  max-width: 100%;
}

</style>
