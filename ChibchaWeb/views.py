from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from Clientes.models import Cliente

from .planes import PLANES_DISPONIBLES





def home(request):

    total_clientes = Cliente.objects.count()

    sitios_web_estimados = total_clientes * 2 if total_clientes > 0 else 0

    estadisticas = {

        'clientes': total_clientes,

        'sitios_web': int(sitios_web_estimados),

        'uptime': '99.99%',

        'tiempo_carga': '2.1s',

    }

    return render(request, 'informacion.html', {

        'planes': PLANES_DISPONIBLES,

        'estadisticas': estadisticas,

    })





class ClienteLoginView(LoginView):

    template_name = 'login.html'

    redirect_authenticated_user = True



    def form_valid(self, form):

        user = form.get_user()



        if hasattr(user, 'empleado'):

            messages.error(self.request, 'Los empleados deben usar el portal de empleados.')

            return self.form_invalid(form)



        if hasattr(user, 'administrador'):

            messages.error(self.request, 'Los administradores deben usar el portal de administradores.')

            return self.form_invalid(form)



        if not hasattr(user, 'cliente'):

            messages.error(self.request, 'No tienes perfil de cliente. Contacta al administrador.')

            return self.form_invalid(form)



        messages.success(self.request, f'Bienvenido {user.username}!')

        return super().form_valid(form)



    def get_success_url(self):

        user = self.request.user

        if hasattr(user, 'cliente'):

            if user.cliente.es_distribuidor and hasattr(user.cliente, 'perfil_distribuidor'):

                return reverse_lazy('distribuidores:dashboard')

            return reverse_lazy('clientes:home_clientes')

        return reverse_lazy('home')





@login_required

def vista_exito(request):

    return render(request, 'exitologin.html')

