from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm  # Asegúrate de tener un formulario definido
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse


# Lista de productos
def lista_productos(request):
    productos_list = Producto.objects.all().order_by('id')  # Asegúrarse de que esto devuelve un queryset y no una función,  Ordena los productos por su ID
    paginator = Paginator(productos_list, 10)  # Muestra 10 productos por página
    page_number = request.GET.get('page')  # Obtiene el número de página de la petición
    productos = paginator.get_page(page_number)  # Devuelve los productos correspondientes a la página
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

# Agregar un producto
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al agregar el producto.')
    else:
        form = ProductoForm()
    return render(request, 'inventario/agregar_producto.html', {'form': form})

# Editar un producto
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto editado exitosamente')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Error al actualizar el producto.')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/editar_producto.html', {'form': form})

# Eliminar un producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

# Ver detalles del producto
def detalles_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'inventario/detalles_producto.html', {'producto': producto})

# Vista para el login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Inicia la sesión del usuario
            return redirect(reverse('dashboard')) # Redirige al dashboard después de iniciar sesión
        else:
            # En caso de error en el login, muestra un mensaje de error
            return render(request, 'inventario/login.html', {'error': 'Usuario o contraseña incorrectos.'})
    return render(request, 'inventario/login.html')

# vistas a usuarios autenticados, esta vista solo será accesible si el usuario ha iniciado sesión
@login_required
def inventario_view(request):
    return render(request, 'inventario/inventario.html')

# Vista de dashboard
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html') # Ruta relativa a "inventario_lab/inventario/templates"

# Vista para cerrar sesión
def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect(reverse('login'))  # Redirige a la página de inicio de sesión
