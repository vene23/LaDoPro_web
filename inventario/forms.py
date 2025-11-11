from django import forms
from .models import Producto  # Asegúrate de importar el modelo correctamente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'marca', 'modelo', 'numero_serie', 'objetivo_uso', 'cantidad', 'estado', 'clasificacion_riesgo', 'mantenimiento_calibracion', 'fecha_adquisicion', 'anio_adquisicion', 'informacion_adicional']


