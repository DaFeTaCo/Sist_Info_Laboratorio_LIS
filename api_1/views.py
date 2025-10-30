# Create your views here.

from django.http import JsonResponse
from django.views import View

from .models import Paciente
import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import json
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Asegúrate de que tu modelo se llama Paciente y tiene estos campos
from .models import Paciente 
from .models import Resultado


class PacienteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # --- GET Method (Retrieve data) ---
    def get(self, request, id=0):
        if (id > 0):
            # Obtener un paciente por ID
            pacientes = list(Paciente.objects.filter(id=id).values())
            if len(pacientes) > 0:
                paciente = pacientes[0]
                datos = {"Message": "Success", "paciente": paciente}
            else:
                datos = {"Message": "Paciente no encontrado..."}
            return JsonResponse(datos)

        else:
            # Obtener todos los pacientes
            pacientes = list(Paciente.objects.values())
            if len(pacientes) > 0:
                datos = {"Message": "Success", "pacientes": pacientes}
            else:
                datos = {"Message": "Pacientes no encontrados..."}
            return JsonResponse(datos)
    
    # --- POST Method (Create new data) ---
    def post(self, request):
        try:
            JsonData = json.loads(request.body)
            Paciente.objects.create(
                documento=JsonData["documento"],
                nombre=JsonData["nombre"],
                # Campo nuevo/modificado: Usamos 'apellido'
                apellido=JsonData["apellido"], 
                codigo_ingreso=JsonData.get("codigo_ingreso"), # Usamos .get por si es opcional/NULL
                direccion=JsonData.get("direccion"),
                telefono=JsonData.get("telefono")
            )
            datos = {"Message": "Success: Paciente creado"}
        except Exception as e:
            datos = {"Message": f"Error al crear: {str(e)}"}
        return JsonResponse(datos)
    
    # --- PUT Method (Update existing data) ---
    def put(self, request, id):
        JsonData = json.loads(request.body)
        
        try:
            paciente = Paciente.objects.get(id=id)
            
            # Actualizar campos
            paciente.documento = JsonData.get("documento", paciente.documento)
            paciente.nombre = JsonData.get("nombre", paciente.nombre)
            paciente.apellido = JsonData.get("apellido", paciente.apellido) # Campo nuevo/modificado
            paciente.codigo_ingreso = JsonData.get("codigo_ingreso", paciente.codigo_ingreso)
            paciente.direccion = JsonData.get("direccion", paciente.direccion)
            paciente.telefono = JsonData.get("telefono", paciente.telefono)
            
            paciente.save()
            datos = {"Message": "Success: Paciente actualizado"}
        except Paciente.DoesNotExist:
            datos = {"Message": "Paciente no encontrado..."}
        except Exception as e:
            datos = {"Message": f"Error al actualizar: {str(e)}"}
        return JsonResponse(datos)
    
    # --- DELETE Method (Delete data) ---
    def delete(self, request, id):
        try:
            paciente = Paciente.objects.get(id=id)
            paciente.delete()
            datos = {"Message": "Success: Paciente eliminado"}
        except Paciente.DoesNotExist:
            datos = {"Message": "Paciente no encontrado..."}
        except Exception as e:
            datos = {"Message": f"Error al eliminar: {str(e)}"}
        return JsonResponse(datos)
    def delete(slef, request, id):
        patients = list(Paciente.objects.filter(id=id).values())
        if len(patients)>0:
            Paciente.objects.filter(id=id).delete()
            datos = {"Message" : "Success"}
        else:
            datos = {"Message" : "Patient not found..."}
        return JsonResponse(datos)


class ResultadoView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # --- GET Method ---
    def get(self, request, id=0):
        if id > 0:
            resultados = list(Resultado.objects.filter(id=id).values())
            if resultados:
                return JsonResponse({"Message": "Success", "resultado": resultados[0]})
            else:
                return JsonResponse({"Message": "Resultado no encontrado..."})
        else:
            resultados = list(Resultado.objects.values())
            if resultados:
                return JsonResponse({"Message": "Success", "resultados": resultados})
            else:
                return JsonResponse({"Message": "Resultados no encontrados..."})

    # --- POST Method ---
    def post(self, request):
        try:
            JsonData = json.loads(request.body)
            Resultado.objects.create(
                codigo_ingreso=JsonData["codigo_ingreso"],
                colesterol_total=JsonData["colesterol_total"],
                colesterol_hdl=JsonData["colesterol_hdl"],
                colesterol_ldl=JsonData["colesterol_ldl"],
                trigliceridos=JsonData["trigliceridos"],
                laboratorista=JsonData["laboratorista"]
            )
            return JsonResponse({"Message": "Success: Resultado creado"})
        except Exception as e:
            return JsonResponse({"Message": f"Error al crear: {str(e)}"})

    # --- DELETE Method ---
    def delete(self, request, id):
        try:
            resultado = Resultado.objects.get(id=id)
            resultado.delete()
            return JsonResponse({"Message": "Success: Resultado eliminado"})
        except Resultado.DoesNotExist:
            return JsonResponse({"Message": "Resultado no encontrado..."})
        except Exception as e:
            return JsonResponse({"Message": f"Error al eliminar: {str(e)}"})

