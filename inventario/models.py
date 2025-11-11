from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    marca = models.CharField(max_length=255)  # campo obligatorio
    modelo = models.CharField(max_length=255, null=True, blank=True)
    numero_serie = models.CharField(max_length=255, null=True, blank=True)  # Modificado para permitir valores nulos
    objetivo_uso = models.CharField(max_length=255)  # campo obligatorio
    cantidad = models.IntegerField(default=0)
    estado = models.CharField(max_length=255, default='Funcionando')
    clasificacion_riesgo = models.CharField(max_length=255, null=True, blank=True)
    mantenimiento_calibracion = models.CharField(max_length=300, blank=True, null=True)
    fecha_adquisicion = models.CharField(max_length=255, null=True, blank=True)
    anio_adquisicion = models.IntegerField(null=True, blank=True)
    informacion_adicional = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

