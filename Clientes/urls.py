from django.urls import path
from .views import (
    borrar_cliente,
    detalle_cliente,
    detalle_cliente_admin,
    editar_cliente,
    lista_clientes_admin,
    perfil,
    mis_hosts,
    registrar_cliente,
)
from django.shortcuts import render
from . import views


app_name = 'clientes' #Namespace para la app
    
urlpatterns = [
    path('registrar/', registrar_cliente, name='registrar_cliente'),
    path('exito/', lambda request: render(request, 'exito.html'), name='registro_exitoso'),
    path('detalle/', detalle_cliente, name='detalle_cliente'),
    path('editar/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('borrar/', borrar_cliente, name='borrar_cliente'),
    path('mis-hosts/', mis_hosts, name='mis_hosts'),
    path('perfil/', perfil, name='perfil'),
    path('home/', views.home_cliente, name='home_clientes'),
    path('quiero-ser-distribuidor/', views.quiero_ser_distribuidor, name='quiero_ser_distribuidor'),
    path('confirmar-ser-distribuidor/', views.hacer_distribuidor, name='hacer_distribuidor'),
    path('distribuidor-exito/', views.distribuidor_exito, name='distribuidor_exito'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('registro-exitoso/', views.registro_exitoso, name='registro_exitoso'),
    path('admin/lista/', lista_clientes_admin, name='lista_clientes_admin'),
    path('admin/<int:cliente_id>/', detalle_cliente_admin, name='detalle_cliente_admin'),
]