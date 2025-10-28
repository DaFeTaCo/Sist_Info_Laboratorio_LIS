from django.db import models

class laboratoristas(models.Model):

    nombre = models.CharField(max_length=50, )
    codigo_interno = models.CharField(max_length=100,)
    titulo = models.CharField(max_length=150,)
    telefono = models.CharField(max_length=150,)

class Paciente(models.Model):
    # El campo 'id' (Primary Key) se crea automáticamente por Django

    documento = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    codigo_ingreso = models.CharField(max_length=150, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
class Resultado(models.Model):

    codigo_ingreso = models.CharField(max_length=10) 

    # Los campos de colesterol y triglicéridos tienen valores con unidades (ej. "180 mg/dL").

    colesterol_total = models.CharField(max_length=20)
    colesterol_hdl = models.CharField(max_length=20)
    colesterol_ldl = models.CharField(max_length=20)
    trigliceridos = models.CharField(max_length=20)
    
    # laboratorista: Código del laboratorista, también como CharField.
    laboratorista = models.CharField(max_length=10) # Basado en los ejemplos 'LAB001'
