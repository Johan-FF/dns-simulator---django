from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from Clientes.models import Cliente
from .planes import PLANES_DISPONIBLES
# #region agent log
import logging
_dbg = logging.getLogger('debug_491cc5')
# #endregion


def home(request):
    # #region agent log
    _dbg.debug('[H1-H4] home view ENTERED, path=%s, lang=%s', request.path, getattr(request, 'LANGUAGE_CODE', 'N/A'))
    # #endregion
    try:
        total_clientes = Cliente.objects.count()
        # #region agent log
        _dbg.debug('[H2-H3] Cliente.objects.count() OK = %s', total_clientes)
        # #endregion
    except Exception as exc:
        # #region agent log
        _dbg.error('[H3] Cliente.objects.count() FAILED: %s', exc, exc_info=True)
        # #endregion
        raise

    sitios_web_estimados = total_clientes * 2 if total_clientes > 0 else 0
    estadisticas = {
        'clientes': total_clientes,
        'sitios_web': int(sitios_web_estimados),
        'uptime': '99.99%',
        'tiempo_carga': '2.1s'
    }

    try:
        # #region agent log
        _dbg.debug('[H1] About to render informacion.html')
        # #endregion
        response = render(request, 'informacion.html', {
            'planes': PLANES_DISPONIBLES,
            'estadisticas': estadisticas
        })
        # #region agent log
        _dbg.debug('[H1] render OK, status=%s', response.status_code)
        # #endregion
        return response
    except Exception as exc:
        # #region agent log
        _dbg.error('[H1] render informacion.html FAILED: %s', exc, exc_info=True)
        # #endregion
        raise

class ClienteLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        user = form.get_user()
        
        # Verificar que no sea un empleado
        if hasattr(user, 'empleado'):
            messages.error(self.request, 'Los empleados deben usar el portal de empleados.')
            return self.form_invalid(form)
            
        # Verificar que no sea un administrador
        if hasattr(user, 'administrador'):
            messages.error(self.request, 'Los administradores deben usar el portal de administradores.')
            return self.form_invalid(form)
            
        # Verificar que sea cliente
        if not hasattr(user, 'cliente'):
            messages.error(self.request, 'No tienes perfil de cliente. Contacta al administrador.')
            return self.form_invalid(form)
            
        messages.success(self.request, f'Bienvenido {user.username}!')
        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'cliente'):
            # Verificar si es distribuidor Y tiene perfil de distribuidor
            if user.cliente.es_distribuidor and hasattr(user.cliente, 'perfil_distribuidor'):
                return reverse_lazy('distribuidores:dashboard')
            else:
                return reverse_lazy('clientes:home_clientes')
        return reverse_lazy('home')    

@login_required
def vista_exito(request):
    return render(request, 'exitologin.html')