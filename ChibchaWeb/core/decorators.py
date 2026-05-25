"""
Centralized authentication and authorization decorators for ChibchaWeb.
"""
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone

from Clientes.models import Cliente
from Empleados.models import Empleado


def cliente_required(view_func):
    """Require an authenticated user with a Cliente profile."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('login')

        try:
            cliente = Cliente.objects.select_related('user').get(user=request.user)
        except Cliente.DoesNotExist:
            messages.error(request, "No tienes permisos de cliente para acceder a esta página.")
            return redirect('login')

        request.cliente = cliente
        return view_func(request, *args, **kwargs)

    return wrapper


def distribuidor_required(view_func):
    """Require an authenticated Cliente with distributor flag."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('login')

        try:
            cliente = Cliente.objects.select_related('user').get(user=request.user)
        except Cliente.DoesNotExist:
            messages.error(request, "No tienes perfil de cliente para acceder a esta página.")
            return redirect('login')

        if not cliente.es_distribuidor:
            messages.error(request, "No tienes permisos de distribuidor para acceder a esta página.")
            return redirect('clientes:home_clientes')

        request.cliente = cliente
        return view_func(request, *args, **kwargs)

    return wrapper


def empleado_required(view_func):
    """Require an authenticated active Empleado."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('empleados:login')

        try:
            empleado = Empleado.objects.select_related('user').get(user=request.user)
        except Empleado.DoesNotExist:
            messages.error(request, "No tienes permisos de empleado para acceder a esta página.")
            return redirect('empleados:login')

        if not empleado.activo:
            messages.error(request, "Tu cuenta de empleado está desactivada.")
            return redirect('empleados:login')

        request.empleado = empleado
        return view_func(request, *args, **kwargs)

    return wrapper


def supervisor_required(view_func):
    """Require an authenticated active supervisor Empleado."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('empleados:login')

        try:
            empleado = Empleado.objects.select_related('user').get(user=request.user)
        except Empleado.DoesNotExist:
            messages.error(request, "No tienes permisos de empleado para acceder a esta página.")
            return redirect('empleados:login')

        if not empleado.activo:
            messages.error(request, "Tu cuenta de empleado está desactivada.")
            return redirect('empleados:login')

        if empleado.rol != 'supervisor':
            messages.error(request, "Solo supervisores pueden acceder a esta página.")
            return redirect('empleados:dashboard')

        request.empleado = empleado
        return view_func(request, *args, **kwargs)

    return wrapper


def agente_required(view_func):
    """Require an authenticated active agent Empleado."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('empleados:login')

        try:
            empleado = Empleado.objects.select_related('user').get(user=request.user)
        except Empleado.DoesNotExist:
            messages.error(request, "No tienes permisos de empleado para acceder a esta página.")
            return redirect('empleados:login')

        if not empleado.activo:
            messages.error(request, "Tu cuenta de empleado está desactivada.")
            return redirect('empleados:login')

        if empleado.rol != 'agente':
            messages.error(request, "Solo agentes pueden acceder a esta página.")
            return redirect('empleados:dashboard')

        request.empleado = empleado
        return view_func(request, *args, **kwargs)

    return wrapper


def administrador_required(view_func):
    """Require an authenticated active Administrador."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect('administradores:login')

        from Administradores.models import Administrador

        try:
            administrador = Administrador.objects.select_related('user').get(user=request.user)
        except Administrador.DoesNotExist:
            messages.error(request, "No tienes permisos de administrador para acceder a esta página.")
            return redirect('administradores:login')

        if not administrador.activo:
            messages.error(request, "Tu cuenta de administrador está desactivada.")
            return redirect('administradores:login')

        administrador.ultimo_acceso = timezone.now()
        administrador.save(update_fields=['ultimo_acceso'])

        request.administrador = administrador
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_permission_required(permission_field):
    """Require administrador role and a specific permission flag before the view runs."""

    def decorator(view_func):
        @wraps(view_func)
        @administrador_required
        def wrapper(request, *args, **kwargs):
            if not getattr(request.administrador, permission_field, False):
                messages.error(request, "No tienes permisos suficientes para realizar esta acción.")
                return redirect('administradores:dashboard')
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
