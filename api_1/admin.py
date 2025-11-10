from django.contrib import admin
from .models import Paciente, Resultado # laboratoristas
# Register your models here.

admin.site.register(Paciente)
# admin.site.register(laboratoristas)    
admin.site.register(Resultado)
