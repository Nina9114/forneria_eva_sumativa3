from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

from django.utils.safestring import mark_safe
from .models import Productos, Clientes, Ventas, Alertas, Categorias


# ============= AUTENTICACIÓN Y SESIONES =============

def login_view(request):
    """Vista de login personalizada"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Configurar datos de sesión específicos
            request.session['forneria_user_id'] = user.id
            request.session['forneria_username'] = user.username
            request.session['forneria_login_time'] = timezone.now().isoformat()
            
            # Contador de visitas
            visitas = request.session.get('visitas_forneria', 0)
            request.session['visitas_forneria'] = visitas + 1
            
            messages.success(request, f'¡Bienvenido/a {user.first_name or user.username}!')
            
            # Redireccionar según rol
            if user.groups.filter(name='Vendedor').exists():
                return redirect('forneria:dashboard_vendedor')
            else:
                return redirect('forneria:dashboard_admin')
        else:
            messages.error(request, 'Credenciales incorrectas.')
    
    return render(request, 'shop/login.html')


def logout_view(request):
    """Vista de logout personalizada"""
    # Limpiar datos específicos
    request.session.pop('forneria_user_id', None)
    request.session.pop('forneria_username', None)
    request.session.pop('forneria_login_time', None)
    request.session.pop('carrito_forneria', None)
    
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('forneria:login')


@login_required
def dashboard_admin(request):
    """Dashboard para administradores"""
    total_productos = Productos.objects.count()
    total_clientes = Clientes.objects.count()
    ventas_hoy = Ventas.objects.filter(fecha__date=timezone.now().date()).count()
    alertas_pendientes = Alertas.objects.filter(estado='pendiente').count()
    
    context = {
        'total_productos': total_productos,
        'total_clientes': total_clientes,
        'ventas_hoy': ventas_hoy,
        'alertas_pendientes': alertas_pendientes,
    }
    
    return render(request, 'shop/dashboard_admin.html', context)


@login_required
def dashboard_vendedor(request):
    """Dashboard para vendedores"""
    total_productos = Productos.objects.count()
    ventas_hoy = Ventas.objects.filter(fecha__date=timezone.now().date()).count()
    
    context = {
        'total_productos': total_productos,
        'ventas_hoy': ventas_hoy,
    }
    
    return render(request, 'shop/dashboard_vendedor.html', context)


@login_required
def session_info(request):
    """Información de la sesión actual"""
    session_data = {
        'user_id': request.session.get('forneria_user_id'),
        'username': request.session.get('forneria_username'),
        'login_time': request.session.get('forneria_login_time'),
        'visitas': request.session.get('visitas_forneria', 0),
        'session_key': request.session.session_key,
    }
    
    return render(request, 'shop/session_info.html', {'session_data': session_data})


@login_required
def clear_session_data(request):
    """Limpiar datos temporales de la sesión"""
    request.session.pop('carrito_forneria', None)
    request.session.pop('visitas_forneria', None)
    
    messages.success(request, 'Datos temporales limpiados.')
    return redirect('forneria:session_info')


# ============= CRUD PRODUCTOS =============

@login_required
def productos_list(request):
    """
    Lista de productos con paginación, búsqueda y filtros
    """
    productos = Productos.objects.all().order_by('-creado')
    
    # Búsqueda
    search = request.GET.get('search', '')
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) |
            Q(marca__icontains=search) |
            Q(descripcion__icontains=search)
        )
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(Categorias_id=categoria_id)
    
    tipo = request.GET.get('tipo')
    if tipo:
        productos = productos.filter(tipo=tipo)
    
    # Paginación
    paginator = Paginator(productos, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías para el filtro
    categorias = Categorias.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'categoria_selected': categoria_id,
        'tipo_selected': tipo,
        'categorias': categorias,
        'tipos': ['propia', 'envasado'],
        'user_can_add': request.user.has_perm('shop.add_productos'),
        'user_can_change': request.user.has_perm('shop.change_productos'),
        'user_can_delete': request.user.has_perm('shop.delete_productos'),
    }
    
    return render(request, 'shop/productos_list.html', context)


@login_required
def productos_create(request):
    """
    Crear nuevo producto
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion', '')
            marca = request.POST.get('marca', '')
            precio = request.POST.get('precio')
            caducidad = request.POST.get('caducidad')
            elaboracion = request.POST.get('elaboracion', '')
            tipo = request.POST.get('tipo')
            categoria_id = request.POST.get('categoria')
            stock_actual = request.POST.get('stock_actual', 0)
            stock_minimo = request.POST.get('stock_minimo', 5)
            stock_maximo = request.POST.get('stock_maximo', 100)
            presentacion = request.POST.get('presentacion', '')
            formato = request.POST.get('formato', '')
            
            # Crear producto
            producto = Productos.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                marca=marca,
                precio=precio,
                caducidad=caducidad,
                elaboracion=elaboracion if elaboracion else None,
                tipo=tipo,
                Categorias_id_id=categoria_id,
                stock_actual=stock_actual,
                stock_minimo=stock_minimo,
                stock_maximo=stock_maximo,
                presentacion=presentacion,
                formato=formato,
                Nutricional_id_id=1  # ID por defecto, se puede mejorar
            )
            
            messages.success(request, mark_safe(f'Producto "{producto.nombre}" creado exitosamente.'))
            return redirect('forneria:productos_list')
            
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    # GET - Mostrar formulario
    categorias = Categorias.objects.all()
    context = {
        'categorias': categorias,
        'tipos': ['propia', 'envasado'],
    }
    
    return render(request, 'shop/productos_create.html', context)


@login_required
def productos_edit(request, producto_id):
    """
    Editar producto existente
    """
    producto = get_object_or_404(Productos, id=producto_id)
    
    if request.method == 'POST':
        try:
            # Actualizar datos
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion', '')
            producto.marca = request.POST.get('marca', '')
            producto.precio = request.POST.get('precio')
            producto.caducidad = request.POST.get('caducidad')
            producto.elaboracion = request.POST.get('elaboracion') or None
            producto.tipo = request.POST.get('tipo')
            producto.Categorias_id_id = request.POST.get('categoria')
            producto.stock_actual = request.POST.get('stock_actual', 0)
            producto.stock_minimo = request.POST.get('stock_minimo', 5)
            producto.stock_maximo = request.POST.get('stock_maximo', 100)
            producto.presentacion = request.POST.get('presentacion', '')
            producto.formato = request.POST.get('formato', '')
            
            producto.save()
            
            messages.success(request, mark_safe(f'Producto "{producto.nombre}" actualizado exitosamente.'))
            return redirect('forneria:productos_list')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar producto: {str(e)}')
    
    # GET - Mostrar formulario
    categorias = Categorias.objects.all()
    context = {
        'producto': producto,
        'categorias': categorias,
        'tipos': ['propia', 'envasado'],
    }
    
    return render(request, 'shop/productos_edit.html', context)


@login_required
def productos_delete(request, producto_id):
    """
    Eliminar producto
    """
    producto = get_object_or_404(Productos, id=producto_id)
    
    if request.method == 'POST':
        try:
            nombre = producto.nombre
            producto.delete()
            messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al eliminar producto: {str(e)}')
    
    return redirect('forneria:productos_list')


@login_required
def productos_detail(request, producto_id):
    """
    Ver detalles de un producto
    """
    producto = get_object_or_404(Productos, id=producto_id)
    
    context = {
        'producto': producto,
        'user_can_change': request.user.has_perm('shop.change_productos'),
        'user_can_delete': request.user.has_perm('shop.delete_productos'),
    }
    
    return render(request, 'shop/productos_detail.html', context)