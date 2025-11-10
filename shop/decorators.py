"""
Decoradores personalizados para control de permisos
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse


def require_permission(permission_name):
    """Decorador que requiere un permiso específico."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.has_perm(permission_name):
                messages.error(request, 'No tienes permisos para realizar esta acción.')
                return redirect('forneria:dashboard_admin')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def groups_required(groups, redirect_to='forneria:login', msg='No tienes permisos para acceder.'):
    """Garantiza que el usuario pertenezca a al menos uno de los grupos indicados o sea superuser."""
    if isinstance(groups, str):
        groups = [groups]

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Inicia sesión para continuar.")
                return redirect('forneria:login')

            if request.user.is_superuser or request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)

            messages.error(request, msg)
            return redirect(redirect_to)
        return wrapper
    return decorator


def ajax_required(view_func):
    """Decorador que requiere que la petición sea AJAX."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return JsonResponse({'error': 'Esta acción requiere AJAX'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Permite únicamente a usuarios en el grupo Administrador o superusuarios."""
    return groups_required(
        groups=['Administrador'],
        redirect_to='forneria:dashboard_vendedor',
        msg='Solo los administradores pueden acceder a esta función.'
    )(view_func)


def editor_or_admin_required(view_func):
    """Permite a usuarios en los grupos Editor o Administrador."""
    return groups_required(
        groups=['Editor', 'Administrador'],
        redirect_to='forneria:login',
        msg='Necesitas ser Editor o Administrador para acceder a esta función.'
    )(view_func)


def permission_or_redirect(perm_codename, redirect_to, msg="No tienes permisos para esta acción."):
    def _decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, "Inicia sesión para continuar.")
                return redirect('forneria:login')
            if not request.user.has_perm(perm_codename):
                messages.error(request, msg)
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return _wrapped
    return _decorator
