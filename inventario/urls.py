# inventario/urls.py
from django.urls import path
from . import views  # Esto importa el archivo views.py
from .views import lista_productos, agregar_producto, editar_producto, eliminar_producto, detalles_producto

urlpatterns = [
    path('lista_productos/', lista_productos, name='lista_productos'),  # Asegúrate de que esta sea la vista principal
    path('agregar/', agregar_producto, name='agregar_producto'),
    path('editar/<int:pk>/', editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),
    path('detalles/<int:pk>/', detalles_producto, name='detalles_producto'),  # Nueva ruta
    path('inventario/', views.inventario_view, name='inventario'),  # URL para la vista de inventario
    path('logout/', views.logout_view, name='logout'),  # URL para cerrar sesión
    path('login/', views.login_view, name='login'),  # URL para el login
    path('dashboard/', views.dashboard_view, name='dashboard'),
]

