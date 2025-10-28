<template>
  <div class="home-container">
    <main class="content">
      <div class="text-and-cards">
        <!-- Texto a la izquierda -->
        <div class="text-section">
          <h1>LIS - Sistema de Información de Laboratorio</h1>
          <p>
            En la era actual, donde la transformación digital es fundamental en el sector de la salud, 
            la gestión eficiente y segura de la información clínica es una prioridad. En BioLab, hemos 
            optado este paradigma de automatización y sistematización para garantizar la excelencia 
            de nuestros servicios.
          </p>
          <p>
            Comprendiendo la necesidad de un sistema que realmente se ajuste a nuestras operaciones diarias, 
            BioLab LIS (Sistema de Información de Laboratorios), es una solución tecnológica diseñada para 
            facilitar la gestión de nuestros pacientes, personal especialista e ingreso de registros de resultados.
          </p>
        </div>

        <!-- Tarjetas a la derecha -->
        <div class="cards">
          <div class="card">
            <div class="card-header">Especialistas</div>
            <div class="card-body">
              El sistema se ha diseñado para que los laboratoristas tengan acceso a la información de pacientes, 
              efectúen registros de resultados y se gestione la base de datos de los profesionales que se encuentran en la institución.
            </div>
          </div>

          <div class="card">
            <div class="card-header">Pacientes</div>
            <div class="card-body">
              Registro e identificación por documento y generación automática de un código de ingreso único para cada visita.
            </div>
          </div>

          <div class="card">
            <div class="card-header">Resultados</div>
            <div class="card-body">
              Mediante un formulario se ingresan los datos del perfil lipídico de un paciente en particular, con opciones de consulta, edición y eliminación de registros.
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "HomeView"
};
</script>

<style scoped>
.home-container {
  display: flex;
  min-height: 100vh;
  background-color: #f4f7f6;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Contenido principal */
.content {
  flex: 1;
  padding: 40px;
}

/* Contenedor general de texto + tarjetas */
.text-and-cards {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

/* Texto a la izquierda */
.text-section {
  flex: 1;
  max-width: 55%;
}

.text-section h1 {
  font-size: 2em;
  margin-bottom: 20px;
  color: #2c3e50;
}

.text-section p {
  margin-bottom: 20px;
  line-height: 1.6;
  color: #555;
}

/* Tarjetas a la derecha */
.cards {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex: 1;
  max-width: 40%;
}

.card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.card-header {
  font-weight: bold;
  font-size: 1.1em;
  margin-bottom: 10px;
  color: #8e44ad;
}

.card-body {
  color: #555;
  line-height: 1.5;
  font-size: 0.95em;
}

.content {
  width: 90%; /* ✅ asegura que use todo el espacio disponible */
  max-width: 100%;
}

</style>
