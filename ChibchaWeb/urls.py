from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('Clientes/', include('Clientes.urls')),
    path('pagos/', include('Pagos.urls')),
    path('empleados/', include('Empleados.urls')),
    path('login/', views.ClienteLoginView.as_view(), name='login'),
    path('exitologin/', views.vista_exito, name='exitologin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('tickets/', include('Tickets.urls', namespace='tickets')),
    path('distribuidor/', include('Distribuidor.urls', namespace='distribuidores')),
    path('dominios/', include('Dominios.urls', namespace='dominios')),
    path('administradores/', include('Administradores.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
