from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Productos, Clientes, Ventas, Alertas


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








