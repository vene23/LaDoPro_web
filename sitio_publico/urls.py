from django.urls import path
from .views import inicio, quienes_somos, servicios, contacto_view, notas_interes, actividades_academicas, suscribir_newsletter

urlpatterns = [
    path('', inicio, name='inicio'),
    path('quienes_somos/', quienes_somos, name='quienes_somos'),
    path('servicios/', servicios, name='servicios'),
    path('contacto', contacto_view, name='contacto'),
    path('formulario/', notas_interes, name='notas_interes'),
    path('actividades_academicas/', actividades_academicas, name='actividades_academicas'),
    path('api/suscribir/', suscribir_newsletter, name='suscribir_newsletter'),
]
