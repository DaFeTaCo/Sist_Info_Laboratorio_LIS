from django.urls import path
from .views import PacienteView, ResultadoView, LaboratoristaView

urlpatterns = [
    # --------------------
    # Rutas de Pacientes
    # --------------------
    path("pacientes/", PacienteView.as_view(), name="pacientes_list"),
    path("pacientes/<int:id>/", PacienteView.as_view(), name="pacientes_process"),

    # --------------------
    # Rutas de Laboratoristas
    # --------------------
    path('laboratoristas/', LaboratoristaView.as_view(), name='laboratoristas_listar_crear'),
    path('laboratoristas/<int:id>/', LaboratoristaView.as_view(), name='laboratoristas_detalle'),


    # --------------------
    # Rutas de Resultados
    # --------------------
    path("resultados/", ResultadoView.as_view(), name="resultados_list"),
    path("resultados/<int:id>/", ResultadoView.as_view(), name="resultados_process"),
]
