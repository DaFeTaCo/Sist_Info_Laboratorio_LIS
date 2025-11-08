from django.db import models

class Laboratoristas(models.Model):
    nombre = models.CharField(max_length=50)
    codigo_interno = models.CharField(max_length=100, unique=True) 
    titulo = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre}"


class Paciente(models.Model):
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
