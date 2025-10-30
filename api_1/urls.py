from django.urls import path
from .views import  PacienteView, ResultadoView #  LaboratoristaView

urlpatterns = [
    # path("laboratoristas/", LaboratoristaView.as_view(), name="laboratoristas_list"),
    # path("laboratoristas/<int:id>", LaboratoristaView.as_view(), name="laboratoristas_process"),    
    path("pacientes/", PacienteView.as_view(), name="pacientes_list"),    
    path("pacientes/<int:id>", PacienteView.as_view(), name="pacientes_process"),
    path("resultados/", ResultadoView.as_view(), name="resultados_list"),
    path("resultados/<int:id>", ResultadoView.as_view(), name="resultados_process")
]
