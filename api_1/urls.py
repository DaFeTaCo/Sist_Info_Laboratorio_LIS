from django.urls import path
from .views import  PacienteView, ResultadoView #  LaboratoristaView

urlpatterns = [
    # path("laboratoristas/", LaboratoristaView.as_view(), name="laboratoristas_list"),
    # path("laboratoristas/<int:id>", LaboratoristaView.as_view(), name="laboratoristas_process"),    
    path("pacientes/", PacienteView.as_view(), name="pacientes_list"),    
    path("resultados/", ResultadoView.as_view(), name="resultados_list"),
    
    path('api/resultados/<int:id>/', ResultadoView.as_view()),
    path('pacientes/<int:id>/', PacienteView.as_view()), 
]


urlpatterns = [
    # Rutas de Pacientes (GET, GET<ID>, PUT<ID>, DELETE<ID>)
    path("pacientes/", PacienteView.as_view(), name="pacientes_list"),
    path("pacientes/<int:id>/", PacienteView.as_view(), name="pacientes_process"), #

    # Rutas de Resultados (GET, POST)
    path("resultados/", ResultadoView.as_view(), name="resultados_list"),
    # La ruta es "resultados/<ID>/" sin el prefijo "api/".
    path("resultados/<int:id>/", ResultadoView.as_view(), name="resultados_process"),
]
