"""
Decoradores personalizados para control de permisos
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse


def require_permission(permission_name):
    """
    Decorador que requiere un permiso específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission_name):
                messages.error(request, 'No tienes permisos para realizar esta acción.')
                return redirect('forneria:dashboard_admin')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_group(group_name):
    """
    Decorador que requiere pertenecer a un grupo específico
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                messages.error(request, f'Necesitas ser {group_name} para acceder a esta función.')
                return redirect('forneria:dashboard_admin')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def ajax_required(view_func):
    """
    Decorador que requiere que la petición sea AJAX
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Esta acción requiere AJAX'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    """
    Decorador que requiere ser administrador (no vendedor)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Vendedor').exists():
            messages.error(request, 'Solo los administradores pueden acceder a esta función.')
            return redirect('forneria:dashboard_vendedor')
        return view_func(request, *args, **kwargs)
    return wrapper


def vendedor_or_admin(view_func):
    """
    Decorador que permite tanto vendedores como administradores
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.groups.filter(name='Vendedor').exists() or 
                request.user.groups.filter(name='Administrador').exists() or
                request.user.is_superuser):
            messages.error(request, 'Necesitas ser vendedor o administrador para acceder a esta función.')
            return redirect('forneria:login')
        return view_func(request, *args, **kwargs)
    return wrapper