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

        <div class="tabla-scroll" v-else>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Código Ingreso</th>
                <th>Nombre</th>
                <th>Colesterol Total <br>(mg/dL)</th>
                <th>Colesterol HDL <br>(mg/dL)</th>
                <th>Colesterol LDL <br>(mg/dL)</th>
                <th>Triglicéridos <br>(mg/dL)</th>
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
                  <td><input type="number" step="0.1" min="0" v-model="resultadoEditando.colesterol_total" /></td>
                  <td><input type="number" step="0.1" min="0" v-model="resultadoEditando.colesterol_hdl" /></td>
                  <td><input type="number" step="0.1" min="0" v-model="resultadoEditando.colesterol_ldl" /></td>
                  <td><input type="number" step="0.1" min="0" v-model="resultadoEditando.trigliceridos" /></td>
                  <td>
                    <select v-model="resultadoEditando.laboratorista" required>
                      <option disabled value="">Laboratorista</option>
                      <option v-for="l in laboratoristas" :key="l.id" :value="l.codigo_interno">
                        {{ l.codigo_interno }} - {{ l.nombre }}
                      </option>
                    </select>
                  </td>
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
                    <button class="btn btn-delete" @click="mostrarConfirmacionModal(r.id)">Eliminar</button>
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="resultadosFiltrados.length === 0" class="no-data">
          No se encontraron resultados.
        </div>
      </div>

      <!-- Crear nuevo resultado -->
      <div class="action-section">
        <h3>Agregar nuevo resultado</h3>
        <form @submit.prevent="crearResultado" class="form-inline">
          <select v-model="nuevoResultado.codigo_ingreso" required>
            <option disabled value="">Código ingreso</option>
            <option v-for="p in pacientes" :key="p.id" :value="p.codigo_ingreso">
              {{ p.codigo_ingreso }} - {{ p.nombre }} {{ p.apellido }}
            </option>
          </select>

          <input type="number" step="0.1" min="0" v-model="nuevoResultado.colesterol_total" placeholder="Colesterol total" required />
          <input type="number" step="0.1" min="0" v-model="nuevoResultado.colesterol_hdl" placeholder="Colesterol HDL" required />
          <input type="number" step="0.1" min="0" v-model="nuevoResultado.colesterol_ldl" placeholder="Colesterol LDL" required />
          <input type="number" step="0.1" min="0" v-model="nuevoResultado.trigliceridos" placeholder="Triglicéridos" required />

          <select v-model="nuevoResultado.laboratorista" required>
            <option disabled value="">Laboratorista</option>
            <option v-for="l in laboratoristas" :key="l.id" :value="l.codigo_interno">
              {{ l.codigo_interno }} - {{ l.nombre }}
            </option>
          </select>

          <button class="btn btn-green" type="submit" :disabled="!formularioNuevoCompleto">Agregar</button>
        </form>
      </div>
    </main>

    <!-- MODAL DE CONFIRMACIÓN -->
    <div v-if="mostrarConfirmacion" class="modal-overlay" @click.self="mostrarConfirmacion = false">
      <div class="modal-content">
        <h3>Confirmar Eliminación</h3>
        <p>¿Estás seguro de que deseas eliminar este resultado? Esta acción es irreversible.</p>
        <div class="modal-actions">
          <button class="btn btn-delete" @click="eliminarResultadoConfirmado">Eliminar</button>
          <button class="btn btn-edit" @click="mostrarConfirmacion = false">Cancelar</button>
        </div>
      </div>
    </div>

    <!-- NOTIFICACIÓN TOAST -->
    <transition name="slide-fade">
      <div v-if="mostrarMensaje" :class="['toast-notification', {'toast-error': isError}]">
        {{ mensajeTexto }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// URLs base - Se elimina la barra diagonal final para evitar la doble barra en PUT/DELETE!
const BASE_URL = 'http://127.0.0.1:8000/api'
const RESULTADOS_API_URL = `${BASE_URL}/resultados`
const PACIENTES_API_URL = `${BASE_URL}/pacientes`
const LABORATORISTAS_API_URL = `${BASE_URL}/laboratoristas`

const resultados = ref([])
const pacientes = ref([])
const laboratoristas = ref([])
const busqueda = ref('')
const cargando = ref(true)
const resultadoEditando = ref(null)

// --- Estados para Notificación (Toast) ---
const mostrarMensaje = ref(false)
const mensajeTexto = ref('')
const isError = ref(false)

// --- Estados para Confirmación (Modal) ---
const mostrarConfirmacion = ref(false)
const idResultadoAEliminar = ref(null)

const nuevoResultado = ref({
  codigo_ingreso: '',
  colesterol_total: '',
  colesterol_hdl: '',
  colesterol_ldl: '',
  trigliceridos: '',
  laboratorista: ''
})

// 🔹 Función para mostrar la notificación
const mostrarNotificacion = (mensaje, error = false) => {
  mensajeTexto.value = mensaje
  isError.value = error
  mostrarMensaje.value = true
  setTimeout(() => {
    mostrarMensaje.value = false
  }, 3000)
}

// 🔹 Validación de formularios
const formularioNuevoCompleto = computed(() => {
  const r = nuevoResultado.value
  return r.codigo_ingreso && r.colesterol_total > 0 && r.colesterol_hdl > 0 && r.colesterol_ldl > 0 && r.trigliceridos > 0 && r.laboratorista
})

const formularioEdicionCompleto = computed(() => {
  const r = resultadoEditando.value
  return r && r.colesterol_total > 0 && r.colesterol_hdl > 0 && r.colesterol_ldl > 0 && r.trigliceridos > 0 && r.laboratorista
})

// 🔹 Cargar datos
const cargarResultados = async () => {
  try {
    // Se añade la barra diagonal aquí
    const response = await axios.get(RESULTADOS_API_URL + '/')
    // Asume que la API devuelve { "resultados": [...] }
    resultados.value = response.data.resultados || response.data
  } catch (error) {
    console.error('Error al cargar resultados:', error)
    mostrarNotificacion("Error al cargar resultados.", true)
  } finally {
    cargando.value = false
  }
}

const cargarPacientes = async () => {
  try {
    // Se añade la barra diagonal aquí
    const response = await axios.get(PACIENTES_API_URL + '/')
    // Asume que la API de pacientes devuelve { "pacientes": [...] }
    pacientes.value = response.data.pacientes || response.data
  } catch (error) {
    console.error('Error al cargar pacientes:', error)
  }
}

const cargarLaboratoristas = async () => {
  try {
    const response = await axios.get(LABORATORISTAS_API_URL + '/')
    laboratoristas.value = response.data.laboratoristas || response.data
  } catch (error) {
    console.error('Error al cargar laboratoristas:', error)
  }
}

// 🔹 Obtener nombre del paciente por código de ingreso
const obtenerNombrePaciente = (codigo) => {
  const paciente = pacientes.value.find(p => p.codigo_ingreso === codigo)
  return paciente ? `${paciente.nombre} ${paciente.apellido}` : 'Paciente eliminado'
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
    mostrarNotificacion('Completa todos los campos antes de guardar.', true)
    return
  }
  try {
    // Se añade la barra diagonal aquí
    await axios.post(RESULTADOS_API_URL + '/', nuevoResultado.value)
    mostrarNotificacion('Resultado agregado exitosamente')
    // Limpiar formulario
    Object.keys(nuevoResultado.value).forEach(k => nuevoResultado.value[k] = '')
    await cargarResultados()
  } catch (error) {
    console.error('Error al crear resultado:', error)
    // Captura el mensaje de error detallado del backend
    mostrarNotificacion(`Error al crear resultado: ${error.response?.data?.Message || error.message}`, true)
  }
}

// 🔹 Editar resultado
const editarResultado = (resultado) => {
  resultadoEditando.value = { ...resultado }
}

const guardarEdicion = async () => {
  if (!formularioEdicionCompleto.value) {
    mostrarNotificacion('Completa todos los campos antes de guardar.', true)
    return
  }
  try {
    // URL se construye como /resultados/ID/
    await axios.put(`${RESULTADOS_API_URL}/${resultadoEditando.value.id}/`, {
      colesterol_total: resultadoEditando.value.colesterol_total,
      colesterol_hdl: resultadoEditando.value.colesterol_hdl,
      colesterol_ldl: resultadoEditando.value.colesterol_ldl,
      trigliceridos: resultadoEditando.value.trigliceridos,
      laboratorista: resultadoEditando.value.laboratorista
    })
    
    mostrarNotificacion('Resultado actualizado exitosamente')
    resultadoEditando.value = null
    await cargarResultados()
  } catch (error) {
    console.error('Error al actualizar resultado:', error)
    mostrarNotificacion(`Error al actualizar resultado: ${error.response?.data?.Message || error.message}`, true)
  }
}

const cancelarEdicion = () => {
  resultadoEditando.value = null
}

// ------------------------------------
// 🔹 Lógica de Eliminación (con Modal y Toast)
// ------------------------------------

// 1. Mostrar el modal y guardar el ID
const mostrarConfirmacionModal = (id) => {
  idResultadoAEliminar.value = id
  mostrarConfirmacion.value = true
}

// 2. Ejecutar la eliminación tras confirmar
const eliminarResultadoConfirmado = async () => {
  const id = idResultadoAEliminar.value
  mostrarConfirmacion.value = false // Cerrar modal inmediatamente

  if (!id) return

  try {
    // URL se construye como /resultados/ID/
    await axios.delete(`${RESULTADOS_API_URL}/${id}/`)
    mostrarNotificacion('Resultado eliminado correctamente')
    idResultadoAEliminar.value = null
    await cargarResultados()
  } catch (error) {
    console.error('Error al eliminar resultado:', error)
    mostrarNotificacion(`Error al eliminar resultado: ${error.response?.data?.Message || error.message}`, true)
  }
}

onMounted(() => {
  cargarResultados()
  cargarPacientes()
  cargarLaboratoristas()
})
</script>

<style scoped>
/* Estilos existentes */

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
/* AÑADIDO: Estilo explícito para el H2 dentro del contenedor de la tabla */
.form-container h2 {
    font-size: 1.5em;
    color: #2c3e50; /* Gris oscuro para mayor contraste */
    margin-top: 0;
    margin-bottom: 15px;
}

.tabla-scroll {
  max-height: 250px;
  overflow-y: auto;
  overflow-x: auto;
  margin-top: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* Mantener títulos fijos arriba cuando haga scroll */
.tabla-scroll thead {
  position: sticky;
  top: 0;
  z-index: 2;
}



/* Fin de estilo añadido */
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
  text-align: left;
}
tr:hover:not(:has(.btn-green)) { /* Evita hover en filas de edición */
  background-color: #f9f9f9;
}
/* Estilo para inputs en modo edición de tabla */
td input {
    width: 100%;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

.btn {
  border: none;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  margin-right: 5px;
  transition: background-color 0.3s ease;
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
    background-color: #2ecc71;
    color: white;
}
.btn-green:hover:not(:disabled) {
    background-color: #27ae60;
}
.btn:disabled {
    background-color: #bdc3c7;
    cursor: not-allowed;
}
.no-data {
  text-align: center;
  padding: 20px;
  color: #777;
}
.action-section h3 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: #2c3e50;
}
.form-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
.form-inline input,
.form-inline select {
  flex: 1;
  min-width: 150px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-inline button {
  flex-shrink: 0;
  padding: 8px 15px;
}

/* ------------------------------------ */
/* Estilos para Modal y Toast */
/* ------------------------------------ */

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  width: 90%;
  text-align: center;
  /* CORRECCIÓN: Asegurar texto negro en el modal */
  color: #2c3e50; 
}

.modal-content h3 {
  margin-top: 0;
  color: #e74c3c;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

/* Toast Notification */
.toast-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 15px 20px;
  background-color: #2ecc71; /* Éxito */
  /* CORRECCIÓN: Cambiar texto a negro para mejor contraste con fondo de color */
  color: black; 
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1010;
  font-weight: 600;
}

.toast-error {
  background-color: #e74c3c; /* Error */
  /* CORRECCIÓN: Forzar texto blanco para mejor contraste con el fondo rojo de error */
  color: white; 
}

/* Transición para el Toast */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>


