<template>
  <div class="dashboard-container">
    <main class="main-content">
      <header class="header">
        <h1><span>BioLab</span> Gestión de Pacientes</h1>
      </header>

      <!-- Barra de búsqueda -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="Buscar por documento o nombre/apellido"
          v-model="busqueda"
        />
      </div>

      <!-- Tabla de Pacientes -->
      <div class="form-container">
        <h2>Listado de Pacientes ({{ pacientesFiltrados.length }} registros)</h2>

        <div v-if="cargando">Cargando pacientes...</div>

        <table v-else>
          <thead>
            <tr>
              <th>ID</th>
              <th>Documento</th>
              <th>Nombre</th>
              <th>Apellido</th>
              <th>Cod. Ingreso</th>
              <th>Dirección</th>
              <th>Teléfono</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in pacientesFiltrados" :key="p.id">
              <!-- MODO EDICIÓN -->
              <template v-if="pacienteEditando?.id === p.id">
                <td>{{ p.id }}</td>
                <td><input v-model="pacienteEditando.documento" /></td>
                <td><input v-model="pacienteEditando.nombre" /></td>
                <td><input v-model="pacienteEditando.apellido" /></td>
                <!-- El código de ingreso se mantiene estático en la edición en línea -->
                <td>{{ p.codigo_ingreso }}</td> 
                <td><input v-model="pacienteEditando.direccion" /></td>
                <td><input v-model="pacienteEditando.telefono" /></td>
                <td>
                  <button class="btn btn-green" @click="guardarEdicion" :disabled="!formularioEdicionCompleto">Guardar</button>
                  <button class="btn btn-delete" @click="cancelarEdicion">Cancelar</button>
                </td>
              </template>

              <!-- MODO VISTA -->
              <template v-else>
                <td>{{ p.id }}</td>
                <td>{{ p.documento }}</td>
                <td>{{ p.nombre }}</td>
                <td>{{ p.apellido }}</td>
                <td>{{ p.codigo_ingreso }}</td>
                <td>{{ p.direccion }}</td>
                <td>{{ p.telefono }}</td>
                <td>
                  <button class="btn btn-edit" @click="editarPaciente(p)">Editar</button>
                  <button class="btn btn-delete" @click="mostrarConfirmacionModal(p.id)">Eliminar</button>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
        <div v-if="pacientesFiltrados.length === 0" class="no-data">
          No se encontraron pacientes.
        </div>
      </div>

      <!-- Crear nuevo paciente (Mantenido según la solicitud) -->
      <div class="action-section">
        <h3>Registrar nuevo paciente</h3>
        <form @submit.prevent="crearPaciente" class="form-inline">
          <input v-model="nuevoPaciente.documento" placeholder="Documento" required />
          <input v-model="nuevoPaciente.nombre" placeholder="Nombre" required />
          <input v-model="nuevoPaciente.apellido" placeholder="Apellido" required />
          <input v-model="nuevoPaciente.codigo_ingreso" placeholder="Código de Ingreso" required />
          <input v-model="nuevoPaciente.direccion" placeholder="Dirección (Opcional)" />
          <input v-model="nuevoPaciente.telefono" placeholder="Teléfono (Opcional)" />

          <button class="btn btn-green" type="submit" :disabled="!formularioNuevoCompleto">Agregar</button>
        </form>
      </div>
    </main>

    <!-- MODAL DE CONFIRMACIÓN -->
    <div v-if="mostrarConfirmacion" class="modal-overlay" @click.self="mostrarConfirmacion = false">
      <div class="modal-content">
        <h3>Confirmar Eliminación</h3>
        <p>¿Estás seguro de que deseas eliminar este paciente? Esta acción es irreversible y podría afectar resultados asociados.</p>
        <div class="modal-actions">
          <button class="btn btn-delete" @click="eliminarPacienteConfirmado">Eliminar</button>
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

// La URL base para la API de Pacientes
const API_URL = 'http://127.0.0.1:8000/api/pacientes/'

const pacientes = ref([])
const busqueda = ref('')
const cargando = ref(true)
const pacienteEditando = ref(null) // Usado para la edición en línea

// --- Estados para Notificación (Toast) ---
const mostrarMensaje = ref(false)
const mensajeTexto = ref('')
const isError = ref(false)

// --- Estados para Confirmación (Modal) ---
const mostrarConfirmacion = ref(false)
const idPacienteAEliminar = ref(null)

// El formulario de nuevo paciente se mantiene con todos los campos
const nuevoPaciente = ref({
  documento: '',
  nombre: '',
  apellido: '',
  codigo_ingreso: '',
  direccion: '',
  telefono: ''
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
// Campos obligatorios para la creación: documento, nombre, apellido, codigo_ingreso
const formularioNuevoCompleto = computed(() => {
  const p = nuevoPaciente.value
  return p.documento && p.nombre && p.apellido && p.codigo_ingreso
})

// Campos obligatorios para la edición (generalmente son los mismos)
const formularioEdicionCompleto = computed(() => {
  const p = pacienteEditando.value
  return p && p.documento && p.nombre && p.apellido && p.codigo_ingreso
})

// 🔹 Cargar datos
const cargarPacientes = async () => {
  try {
    const response = await axios.get(API_URL)
    pacientes.value = response.data.pacientes || response.data
  } catch (error) {
    console.error('Error al cargar pacientes:', error)
    mostrarNotificacion("Error al cargar pacientes.", true)
  } finally {
    cargando.value = false
  }
}

// 🔹 Filtro de búsqueda
const pacientesFiltrados = computed(() => {
  if (!busqueda.value) return pacientes.value
  const b = busqueda.value.toLowerCase()
  return pacientes.value.filter(p =>
    p.documento.toLowerCase().includes(b) ||
    p.nombre.toLowerCase().includes(b) ||
    p.apellido.toLowerCase().includes(b)
  )
})

// 🔹 Crear paciente
const crearPaciente = async () => {
  if (!formularioNuevoCompleto.value) {
    mostrarNotificacion('Completa los campos obligatorios (Documento, Nombre, Apellido, Cod. Ingreso).', true)
    return
  }
  try {
    await axios.post(API_URL, nuevoPaciente.value)
    mostrarNotificacion('Paciente registrado exitosamente')
    // Limpiar formulario
    Object.keys(nuevoPaciente.value).forEach(k => nuevoPaciente.value[k] = '')
    await cargarPacientes()
  } catch (error) {
    console.error('Error al crear paciente:', error)
    mostrarNotificacion(`Error al crear paciente: ${error.response?.data?.Message || error.message}`, true)
  }
}

// ------------------------------------
// 🔹 Lógica de Edición
// ------------------------------------
const editarPaciente = (paciente) => {
  // Clonar el objeto para no modificar el original directamente
  pacienteEditando.value = { ...paciente }
}

const guardarEdicion = async () => {
  if (!formularioEdicionCompleto.value) {
    mostrarNotificacion('Completa los campos obligatorios antes de guardar.', true)
    return
  }
  try {
    const id = pacienteEditando.value.id
    // Enviamos solo los campos editables. El codigo_ingreso no se envía ya que debe ser inmutable o manejarse aparte
    await axios.put(`${API_URL}${id}/`, {
      documento: pacienteEditando.value.documento,
      nombre: pacienteEditando.value.nombre,
      apellido: pacienteEditando.value.apellido,
      direccion: pacienteEditando.value.direccion,
      telefono: pacienteEditando.value.telefono
    })
    
    mostrarNotificacion('Paciente actualizado exitosamente')
    pacienteEditando.value = null
    await cargarPacientes() // Recargar para mostrar los cambios
  } catch (error) {
    console.error('Error al actualizar paciente:', error)
    mostrarNotificacion(`Error al actualizar paciente: ${error.response?.data?.Message || error.message}`, true)
  }
}

const cancelarEdicion = () => {
  pacienteEditando.value = null
}

// ------------------------------------
// 🔹 Lógica de Eliminación (con Modal y Toast)
// ------------------------------------

// 1. Mostrar el modal y guardar el ID
const mostrarConfirmacionModal = (id) => {
  idPacienteAEliminar.value = id
  mostrarConfirmacion.value = true
}

// 2. Ejecutar la eliminación tras confirmar
const eliminarPacienteConfirmado = async () => {
  const id = idPacienteAEliminar.value
  mostrarConfirmacion.value = false // Cerrar modal inmediatamente

  if (!id) return

  try {
    // URL de eliminación: /api/pacientes/ID/
    await axios.delete(`${API_URL}${id}/`)
    mostrarNotificacion('Paciente eliminado correctamente')
    idPacienteAEliminar.value = null
    await cargarPacientes()
  } catch (error) {
    console.error('Error al eliminar paciente:', error)
    // Muestra el mensaje de error de Django si está disponible
    mostrarNotificacion(`Error al eliminar paciente: ${error.response?.data?.Message || error.message || 'Error de red o del servidor'}`, true)
  }
}

onMounted(() => {
  cargarPacientes()
})
</script>

<style scoped>
/* Estilos generales */
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
  margin-bottom: 20px;
}
.form-container, .action-section {
  background: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  max-width: 1300px;
  margin-top: 20px;
}
/* Color gris oscuro para el H2 (el color #2c3e50 fue aplicado en el turno anterior) */
h2 {
  color: #2c3e50; 
  margin-bottom: 15px;
}

/* Color negro para el H3 "Registrar nuevo paciente" */
h3 {
  color: #000;
  margin-bottom: 15px;
}


/* Tabla */
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
tr:hover:not(:has(.btn-green)) {
  background-color: #f9f9f9;
}

/* Campos de entrada para Edición de Tabla */
td input {
  width: 100%;
  padding: 5px;
  border: 1px solid #060505;
  border-radius: 4px;
  box-sizing: border-box;
}


/* Botones */
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

/* Formulario de Creación */
.form-inline {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  color: #000;
}
.form-inline input {
  /* Nueva configuración para forzar la horizontalidad en desktop/tablet */
  /* 6 inputs, 1/6th width each, adjusted for 10px gap */
  flex: 1 1 calc(16.66% - 10px); 
  min-width: 100px;
  padding: 8px 10px; /* Ajuste de padding para que se vea bien */
  border: 1px solid #0f0e0e;
  border-radius: 4px;
  box-sizing: border-box;
}
.form-inline .btn {
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
  color:#2c3e50;
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
  color: rgb(12, 6, 6);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1010;
  font-weight: 600;
}

.toast-error {
  background-color: #e74c3c; /* Error */
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-content {
    padding: 15px;
  }
  .form-inline {
    flex-direction: column;
    gap: 15px;
  }
  .form-inline input, .form-inline select, .form-inline button {
    width: 100%;
    margin-right: 0 !important;
  }
  table, thead, tbody, th, td, tr {
    display: block;
  }
  thead tr {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
  tr { border: 1px solid #ccc; margin-bottom: 10px; border-radius: 8px;}
  td {
    border: none;
    border-bottom: 1px solid #eee;
    position: relative;
    padding-left: 50%;
    text-align: right;
  }
  td:before {
    position: absolute;
    top: 6px;
    left: 6px;
    width: 45%;
    padding-right: 10px;
    white-space: nowrap;
    content: attr(data-label);
    font-weight: bold;
    text-align: left;
    color: #34495e;
  }
  /* Labels for mobile view */
  td:nth-of-type(1):before { content: "ID"; }
  td:nth-of-type(2):before { content: "Documento"; }
  td:nth-of-type(3):before { content: "Nombre"; }
  td:nth-of-type(4):before { content: "Apellido"; }
  td:nth-of-type(5):before { content: "Cod. Ingreso"; }
  td:nth-of-type(6):before { content: "Dirección"; }
  td:nth-of-type(7):before { content: "Teléfono"; }
  td:nth-of-type(8) { text-align: center; } /* Actions */
  
  .toast-notification {
    left: 10px;
    right: 10px;
    bottom: 10px;
    text-align: center;
  }
}
</style>
