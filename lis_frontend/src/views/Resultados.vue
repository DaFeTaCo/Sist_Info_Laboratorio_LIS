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
              <th>Nombre</th>
              <th>Colesterol Total</th>
              <th>Colesterol HDL</th>
              <th>Colesterol LDL</th>
              <th>Triglicéridos</th>
              <th>Laboratorista</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in resultadosFiltrados" :key="r.id">
              <template v-if="resultadoEditando?.id === r.id">
                <td>{{ r.id }}</td>
                <td>{{ r.codigo_ingreso }}</td>
                <td>{{ obtenerNombrePaciente(r.codigo_ingreso) }}</td>
                <td><input type="number" v-model="resultadoEditando.colesterol_total" /></td>
                <td><input type="number" v-model="resultadoEditando.colesterol_hdl" /></td>
                <td><input type="number" v-model="resultadoEditando.colesterol_ldl" /></td>
                <td><input type="number" v-model="resultadoEditando.trigliceridos" /></td>
                <td><input v-model="resultadoEditando.laboratorista" /></td>
                <td>
                  <button class="btn btn-green" @click="guardarEdicion" :disabled="!formularioEdicionCompleto">Guardar</button>
                  <button class="btn btn-delete" @click="cancelarEdicion">Cancelar</button>
                </td>
              </template>

              <template v-else>
                <td>{{ r.id }}</td>
                <td>{{ r.codigo_ingreso }}</td>
                <td>{{ obtenerNombrePaciente(r.codigo_ingreso) }}</td>
                <td>{{ r.colesterol_total }}</td>
                <td>{{ r.colesterol_hdl }}</td>
                <td>{{ r.colesterol_ldl }}</td>
                <td>{{ r.trigliceridos }}</td>
                <td>{{ r.laboratorista }}</td>
                <td>
                  <button class="btn btn-edit" @click="editarResultado(r)">Editar</button>
                  <button class="btn btn-delete" @click="eliminarResultado(r.id)">Eliminar</button>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
        <div v-if="resultadosFiltrados.length === 0" class="no-data">
          No se encontraron resultados.
        </div>
      </div>

      <!-- Crear nuevo resultado -->
      <div class="action-section">
        <h3>Agregar nuevo resultado</h3>
        <form @submit.prevent="crearResultado" class="form-inline">
          <select v-model="nuevoResultado.codigo_ingreso" required>
            <option disabled value="">Seleccione código ingreso</option>
            <option v-for="p in pacientes" :key="p.id" :value="p.codigo_ingreso">
              {{ p.codigo_ingreso }} - {{ p.nombre }} {{ p.apellido }}
            </option>
          </select>

          <input type="number" v-model="nuevoResultado.colesterol_total" placeholder="Colesterol total" required />
          <input type="number" v-model="nuevoResultado.colesterol_hdl" placeholder="Colesterol HDL" required />
          <input type="number" v-model="nuevoResultado.colesterol_ldl" placeholder="Colesterol LDL" required />
          <input type="number" v-model="nuevoResultado.trigliceridos" placeholder="Triglicéridos" required />
          <input v-model="nuevoResultado.laboratorista" placeholder="Código laboratorista" required />

          <button class="btn btn-green" type="submit" :disabled="!formularioNuevoCompleto">Agregar</button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const resultados = ref([])
const pacientes = ref([])
const busqueda = ref('')
const cargando = ref(true)
const resultadoEditando = ref(null)

const nuevoResultado = ref({
  codigo_ingreso: '',
  colesterol_total: '',
  colesterol_hdl: '',
  colesterol_ldl: '',
  trigliceridos: '',
  laboratorista: ''
})

// 🔹 Validación de formularios
const formularioNuevoCompleto = computed(() => {
  const r = nuevoResultado.value
  return r.codigo_ingreso && r.colesterol_total && r.colesterol_hdl && r.colesterol_ldl && r.trigliceridos && r.laboratorista
})

const formularioEdicionCompleto = computed(() => {
  const r = resultadoEditando.value
  return r && r.colesterol_total && r.colesterol_hdl && r.colesterol_ldl && r.trigliceridos && r.laboratorista
})

// 🔹 Cargar datos
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

const cargarPacientes = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/pacientes/')
    pacientes.value = response.data.pacientes || response.data
  } catch (error) {
    console.error('Error al cargar pacientes:', error)
  }
}

// 🔹 Obtener nombre del paciente por código de ingreso
const obtenerNombrePaciente = (codigo) => {
  const paciente = pacientes.value.find(p => p.codigo_ingreso === codigo)
  return paciente ? `${paciente.nombre} ${paciente.apellido}` : 'Desconocido'
}

// 🔹 Filtro de búsqueda
const resultadosFiltrados = computed(() => {
  if (!busqueda.value) return resultados.value
  const b = busqueda.value.toLowerCase()
  return resultados.value.filter(r =>
    r.codigo_ingreso.toLowerCase().includes(b)
  )
})

// 🔹 Crear resultado
const crearResultado = async () => {
  if (!formularioNuevoCompleto.value) {
    alert('Completa todos los campos antes de guardar.')
    return
  }
  try {
    await axios.post('http://127.0.0.1:8000/api/resultados/', nuevoResultado.value)
    alert('Resultado agregado exitosamente')
    Object.keys(nuevoResultado.value).forEach(k => nuevoResultado.value[k] = '')
    await cargarResultados()
  } catch (error) {
    console.error('Error al crear resultado:', error)
  }
}

// 🔹 Editar resultado
const editarResultado = (resultado) => {
  resultadoEditando.value = { ...resultado }
}

const guardarEdicion = async () => {
  if (!formularioEdicionCompleto.value) {
    alert('Completa todos los campos antes de guardar.')
    return
  }
  try {
    await axios.put(`http://127.0.0.1:8000/api/resultados/${resultadoEditando.value.id}/`, {
      colesterol_total: resultadoEditando.value.colesterol_total,
      colesterol_hdl: resultadoEditando.value.colesterol_hdl,
      colesterol_ldl: resultadoEditando.value.colesterol_ldl,
      trigliceridos: resultadoEditando.value.trigliceridos,
      laboratorista: resultadoEditando.value.laboratorista
    })
    alert('Resultado actualizado exitosamente')
    resultadoEditando.value = null
    await cargarResultados()
  } catch (error) {
    console.error('Error al actualizar resultado:', error)
  }
}

const cancelarEdicion = () => {
  resultadoEditando.value = null
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

onMounted(() => {
  cargarResultados()
  cargarPacientes()
})
</script>

<style scoped>
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

