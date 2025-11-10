<template>
  <div class="dashboard-container">
    <main class="main-content">
      <header class="header">
        <h1><span>BioLab</span> Laboratoristas</h1>
      </header>

      <!-- Barra de búsqueda -->
      <div class="search-bar">
        <input
          type="text"
          placeholder="Buscar por nombre o código interno"
          v-model="busqueda"
        />
      </div>

      <!-- Tabla de Laboratoristas -->
      <div class="form-container">
        <h2>Listado de Laboratoristas ({{ laboratoristasFiltrados.length }} registros)</h2>

        <div v-if="cargando">Cargando datos...</div>

        <div class="tabla-scroll" v-else>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Código Interno</th>
                <th>Nombre</th>
                <th>Título Profesional</th>
                <th>Teléfono</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="l in laboratoristasFiltrados" :key="l.id">
                
                <!-- MODO EDICIÓN -->
                <template v-if="laboratoristaEditando?.codigo_interno === l.codigo_interno">
                  <td data-label="ID">{{ l.id }}</td>
                  <td data-label="Código Interno">{{ l.codigo_interno }}</td>
                  <td data-label="Nombre"><input v-model="laboratoristaEditando.nombre" /></td>
                  <td data-label="Título Profesional">
                    <select v-model="laboratoristaEditando.titulo">
                      <option value="Bacteriólogo/a">Bacteriólogo/a</option>
                      <option value="Microbiólogo/a">Microbiólogo/a</option>
                      <option value="Biólogo/a">Biólogo/a</option>
                    </select>
                  </td>
                  <td data-label="Teléfono"><input v-model="laboratoristaEditando.telefono" @input="soloNumeros" /></td>
                  <td>
                    <button class="btn btn-green" @click="guardarEdicion" :disabled="!formularioEdicionCompleto">Guardar</button>
                    <button class="btn btn-delete" @click="cancelarEdicion">Cancelar</button>
                  </td>
                </template>

                <!-- MODO VISTA -->
                <template v-else>
                  <td data-label="ID">{{ l.id }}</td>
                  <td data-label="Código Interno">{{ l.codigo_interno }}</td>
                  <td data-label="Nombre">{{ l.nombre }}</td>
                  <td data-label="Título Profesional">{{ l.titulo }}</td>
                  <td data-label="Teléfono">{{ l.telefono }}</td>
                  <td>
                    <button class="btn btn-edit" @click="editarLaboratorista(l)">Editar</button>
                    <button class="btn btn-delete" @click="mostrarConfirmacionModal(l.codigo_interno)">Eliminar</button>
                  </td>
                </template>

              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="laboratoristasFiltrados.length === 0 && !cargando" class="no-data">
        No se encontraron registros.
      </div>

      <!-- Crear nuevo laboratorista -->
      <div class="action-section">
        <h3>Registrar nuevo laboratorista</h3>
        <form @submit.prevent="crearLaboratorista" class="form-inline">
          <input v-model="nuevoLaboratorista.codigo_interno" placeholder="Código Interno" required />
          <input v-model="nuevoLaboratorista.nombre" placeholder="Nombre completo" required />
          <select v-model="nuevoLaboratorista.titulo" required>
            <option disabled value="">Seleccione título</option>
            <option value="Bacteriólogo/a">Bacteriólogo/a</option>
            <option value="Microbiólogo/a">Microbiólogo/a</option>
            <option value="Biólogo/a">Biólogo/a</option>
          </select>
          <input v-model="nuevoLaboratorista.telefono" placeholder="Teléfono" @input="soloNumeros"/>

          <button class="btn btn-green" type="submit" :disabled="!formularioNuevoCompleto">Agregar</button>
        </form>
      </div>

      <!-- MODAL -->
      <div v-if="mostrarConfirmacion" class="modal-overlay" @click.self="mostrarConfirmacion = false">
        <div class="modal-content">
          <h3>Confirmar Eliminación</h3>
          <p>¿Seguro que deseas eliminar este laboratorista?</p>
          <div class="modal-actions">
            <button class="btn btn-delete" @click="eliminarLaboratoristaConfirmado">Eliminar</button>
            <button class="btn btn-edit" @click="mostrarConfirmacion = false">Cancelar</button>
          </div>
        </div>
      </div>

      <!-- TOAST -->
      <transition name="slide-fade">
        <div v-if="mostrarMensaje" :class="['toast-notification', {'toast-error': isError}]">
          {{ mensajeTexto }}
        </div>
      </transition>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// URL API
const API_URL = 'http://127.0.0.1:8000/api/laboratoristas/'

const laboratoristas = ref([])
const busqueda = ref('')
const cargando = ref(true)

const laboratoristaEditando = ref(null)

const mostrarMensaje = ref(false)
const mensajeTexto = ref('')
const isError = ref(false)

const mostrarConfirmacion = ref(false)
const codigoAEliminar = ref(null)

const nuevoLaboratorista = ref({
  codigo_interno: '',
  nombre: '',
  titulo: '',
  telefono: ''
})


const mostrarNotificacion = (msg, error=false) => {
  mensajeTexto.value = msg
  isError.value = error
  mostrarMensaje.value = true
  setTimeout(() => mostrarMensaje.value = false, 3000)
}

// Validaciones
// Requerido: Código Interno, Nombre, Título
const formularioNuevoCompleto = computed(() => {
  const l = nuevoLaboratorista.value
  return l.codigo_interno && l.nombre && l.titulo
})

// Requerido: Nombre, Título (el código interno no se edita)
const formularioEdicionCompleto = computed(() => {
  const l = laboratoristaEditando.value
  return l && l.nombre && l.titulo
})

// Cargar lista inicial
const cargarLaboratoristas = async () => {
  try {
    const res = await axios.get(API_URL)
    // Asegurarse de que se accede correctamente a la lista (asumiendo que devuelve {laboratoristas: []})
    laboratoristas.value = res.data.laboratoristas || [] 
  } catch (err) {
    console.error("Error al cargar laboratoristas:", err)
    mostrarNotificacion("Error al cargar datos", true)
  } finally {
    cargando.value = false
  }
}


// Búsqueda
const laboratoristasFiltrados = computed(() => {
  if (!busqueda.value) return laboratoristas.value
  const b = busqueda.value.toLowerCase()
  return laboratoristas.value.filter(l =>
    l.nombre.toLowerCase().includes(b) ||
    l.codigo_interno.toLowerCase().includes(b)
  )
})

// Crear
const crearLaboratorista = async () => {
  if (!formularioNuevoCompleto.value) {
    mostrarNotificacion('Completa los campos obligatorios (Código Interno, Nombre, Título).', true)
    return
  }
  try {
    await axios.post(API_URL, nuevoLaboratorista.value)
    mostrarNotificacion("Laboratorista registrado")
    Object.keys(nuevoLaboratorista.value).forEach(k => nuevoLaboratorista.value[k]='')
    cargarLaboratoristas()
  } catch(err) {
    const msg = err.response?.data?.Message || "Error desconocido al registrar"
    console.error("Error al crear:", err)
    mostrarNotificacion(`Error al registrar: ${msg}`, true)
  }
}

// Editar
const editarLaboratorista = (l) => laboratoristaEditando.value = { ...l }

const guardarEdicion = async () => {
  if (!formularioEdicionCompleto.value) {
    mostrarNotificacion('Completa los campos obligatorios (Nombre, Título).', true)
    return
  }
  try {
    const codigo = laboratoristaEditando.value.codigo_interno
    
    // Solo enviamos los campos que se pueden modificar
    const payload = {
      nombre: laboratoristaEditando.value.nombre,
      titulo: laboratoristaEditando.value.titulo,
      telefono: laboratoristaEditando.value.telefono || ""
    }

    // Usamos codigo_interno en la URL, que el backend ahora está listo para recibir
    await axios.put(`${API_URL}${codigo}/`, payload)
    
    laboratoristaEditando.value = null
    mostrarNotificacion("Actualizado correctamente")
    cargarLaboratoristas()
  } catch(err) {
    const msg = err.response?.data?.Message || "Error desconocido al actualizar"
    console.error("Error al actualizar:", err)
    mostrarNotificacion(`Error al actualizar: ${msg}`, true)
  }
}

const cancelarEdicion = () => laboratoristaEditando.value = null

// Eliminar modal
const mostrarConfirmacionModal = (codigo) => {
  codigoAEliminar.value = codigo
  mostrarConfirmacion.value = true
}

const eliminarLaboratoristaConfirmado = async () => {
  mostrarConfirmacion.value = false
  try {
    // Usamos codigo_interno en la URL
    await axios.delete(`${API_URL}${codigoAEliminar.value}/`)
    mostrarNotificacion("Eliminado correctamente")
    cargarLaboratoristas()
  } catch(err) {
    const msg = err.response?.data?.Message || "Error desconocido al eliminar"
    console.error("Error al eliminar:", err)
    mostrarNotificacion(`Error al eliminar: ${msg}`, true)
  }
}

const soloNumeros = (event) => {
  event.target.value = event.target.value.replace(/\D/g, "").slice(0, 10)
}

onMounted(() => cargarLaboratoristas())
</script>


<style scoped>
/* Estilos generales */

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
  max-width: 1200px;
  margin-top: 20px;
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
td input, td select {
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
.form-inline input, .form-inline select {
  /* 4 inputs + 1 button. 1/4th width each, adjusted for gap */
  flex: 1 1 calc(25% - 10px); 
  min-width: 100px;
  padding: 8px 10px;
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
  /* Labels for mobile view (Must match data-label attribute in HTML) */
  td:nth-of-type(1):before { content: "ID"; }
  td:nth-of-type(2):before { content: "Código Interno"; }
  td:nth-of-type(3):before { content: "Nombre"; }
  td:nth-of-type(4):before { content: "Título Profesional"; }
  td:nth-of-type(5):before { content: "Teléfono"; }
  td:nth-of-type(6) { text-align: center; } /* Actions */
  
  .toast-notification {
    left: 10px;
    right: 10px;
    bottom: 10px;
    text-align: center;
  }
}
</style>