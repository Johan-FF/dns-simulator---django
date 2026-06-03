from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from ChibchaWeb import settings
from ChibchaWeb.decorators import cliente_required
from .forms import VerificarURLForm, AgregarDominioForm
from .models import Dominios
from .domain_availability import (
    DomainRegistrationStatus,
    check_domain_registration,
)
import xml.etree.ElementTree as ET
from Pagos.models import PagoDistribuidor
from django.core.mail import EmailMessage
from django.conf import settings


def _normalize_host_input(value: str) -> str:
    host = value.strip()
    if host.startswith("http://"):
        host = host[7:]
    if host.startswith("https://"):
        host = host[8:]
    if host.startswith("www."):
        host = host[4:]
    return host.split("/")[0].split("?")[0]


def _spanish_registration_message(result) -> str:
    if result.status == DomainRegistrationStatus.AVAILABLE:
        return (
            "La URL no está siendo ocupada y la puedes usar!."
        )
    if result.status == DomainRegistrationStatus.REGISTERED:
        if result.web_active:
            return f"El dominio ya está registrado y tiene un sitio web activo."
        return f"El dominio ya está registrado (sin sitio web público activo detectado)."
    return (
        "No pudimos verificar la disponibilidad del dominio. "
        "Intenta de nuevo en unos minutos."
    )


def verificar_url(request):
    resultado = None
    valido = True

    if request.method == 'POST':
        form = VerificarURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            dominio = _normalize_host_input(url)
            availability = check_domain_registration(dominio)
            resultado = _spanish_registration_message(availability)
            valido = availability.is_available

            if request.user.is_authenticated and resultado:
                try:
                    from Clientes.models import Cliente, HostSearchHistory

                    cliente = Cliente.objects.get(user=request.user)
                    HostSearchHistory.objects.create(
                        cliente=cliente,
                        query=dominio,
                        available=valido,
                        result_message=resultado,
                    )
                except Cliente.DoesNotExist:
                    pass
    else:
        form = VerificarURLForm()

    return render(request, 'verificar_url.html', {'form': form, 'resultado': resultado,  'valido': valido,})


@cliente_required
def agregar_dominio(request):
    """
    Vista para que los clientes agreguen dominios a su cuenta
    """
    cliente = request.cliente
    
    # Verificar si viene desde un distribuidor
    from_distribuidor = request.GET.get('from') == 'distribuidor'
    compra_distribuidor = from_distribuidor
    
    # Verificar que tenga suscripción activa
    if not cliente.suscripcion_activa:
        messages.warning(request, "Necesitas una suscripción activa para agregar dominios.")
        return redirect('clientes:home_clientes')
    
    # Verificar límite de dominios según el plan (solo si no viene de distribuidor)
    if not from_distribuidor and not cliente.puede_agregar_dominios:
        messages.error(request, f"Has alcanzado el límite de dominios para tu plan {cliente.plan} ({cliente.limite_dominios} dominios). Considera actualizar tu plan para agregar más dominios.")
        return redirect('clientes:mis_hosts')
    
    form = AgregarDominioForm()
    dominio_validado = False
    dominio_disponible = False
    dominio_existe = False
    dominio_estado = ""
    dominio_web_activo = False
    dominio_valor = ""
    
    if request.method == 'POST':
        form = AgregarDominioForm(request.POST)
        accion = request.POST.get('accion')
        if form.is_valid():
            dominio = form.cleaned_data['dominio']
            dominio_valor = dominio
            # Verificar si el dominio ya existe en nuestra base de datos
            if Dominios.objects.filter(nombreDominio=dominio).exists():
                messages.error(request, f"El dominio '{dominio}' ya está registrado en nuestro sistema.")
                return render(request, 'agregar_dominio.html', {
                    'form': form, 
                    'cliente': cliente,
                    'dominio_validado': False,
                    'dominio_disponible': False,
                    'dominio_existe': False,
                    'dominio_valor': dominio_valor,
                    'from_distribuidor': from_distribuidor
                })
            if accion == 'validar':
                availability = check_domain_registration(dominio)
                dominio_validado = True
                dominio_disponible = availability.is_available
                dominio_existe = availability.status == DomainRegistrationStatus.REGISTERED
                dominio_estado = availability.status.value
                dominio_web_activo = availability.web_active

                if availability.status == DomainRegistrationStatus.AVAILABLE:
                    messages.success(
                        request,
                        f"¡Perfecto! El dominio '{dominio}' está disponible y listo "
                        f"para usar en tu hosting.",
                    )
                elif availability.status == DomainRegistrationStatus.REGISTERED:
                    if availability.web_active:
                        messages.warning(
                            request,
                            f"El dominio '{dominio}' ya está registrado y tiene un sitio "
                            f"web activo. Si te pertenece y quieres transferirlo a "
                            f"ChibchaWeb, contacta a soporte.",
                        )
                    else:
                        messages.warning(
                            request,
                            f"El dominio '{dominio}' ya está registrado. Elige otro "
                            f"dominio o contáctanos si este te pertenece.",
                        )
                else:
                    messages.error(request, _spanish_registration_message(availability))

            elif accion == 'agregar':
                availability = check_domain_registration(dominio)
                if not availability.is_available:
                    if availability.status == DomainRegistrationStatus.ERROR:
                        messages.error(
                            request,
                            _spanish_registration_message(availability),
                        )
                    else:
                        messages.error(
                            request,
                            f"No se puede agregar el dominio '{dominio}' porque ya está "
                            f"registrado. Elige otro dominio o contacta a soporte si "
                            f"este te pertenece.",
                        )
                    return render(request, 'agregar_dominio.html', {
                        'form': form,
                        'cliente': cliente,
                        'dominio_validado': True,
                        'dominio_disponible': False,
                        'dominio_existe': availability.status
                        == DomainRegistrationStatus.REGISTERED,
                        'dominio_estado': availability.status.value,
                        'dominio_web_activo': availability.web_active,
                        'dominio_valor': dominio_valor,
                        'from_distribuidor': from_distribuidor,
                    })
                
                # Crear el registro del dominio
                nuevo_dominio = Dominios.objects.create(
                    clienteId=cliente,
                    nombreDominio=dominio,
                    compraDistribuidor=compra_distribuidor
                )
                
                # Si viene desde distribuidor, actualizar contador de páginas vendidas
                if from_distribuidor and hasattr(cliente, 'perfil_distribuidor'):
                    distribuidor = cliente.perfil_distribuidor
                    if distribuidor.paginas_disponibles > 0:
                        distribuidor.paginas_vendidas += 1
                        distribuidor.save()
                        # Calcular comisión y registrar pago negativo
                        precio_base = settings.PRECIO_POR_PAGINA_DISTRIBUIDOR
                        monto_comision = -precio_base * distribuidor.comision  # Negativo por agregar
                        pago = PagoDistribuidor.objects.filter(cliente=cliente).order_by('-fecha').first()
                        if pago:
                            direc = pago.direccion         # Instancia de Direccion o None
                            tarjeta = pago.tarjeta_usada  
                        PagoDistribuidor.objects.create(
                            cliente=cliente,
                            monto=monto_comision,
                            cantidad_paginas=1,
                            tarjeta_usada=tarjeta,
                            direccion=direc,
                            descripcion=f"Comisión por agregar dominio '{dominio}'"
                        )
                        messages.info(request, f"Se ha usado 1 espacio de tu paquete de distribuidor. Tienes {distribuidor.paginas_disponibles - 1} espacios restantes.")
                    else:
                        # Esto no debería pasar si se valida correctamente en el frontend
                        messages.warning(request, "No tienes espacios disponibles en tu paquete de distribuidor.")
                
                # Generar XML para uso interno
                generar_xml_interno(cliente, dominio)
                
                messages.success(request, f"¡Perfecto! El dominio '{dominio}' ha sido agregado exitosamente a tu cuenta.")
                
                # Redirigir según el origen
                if from_distribuidor:
                    return redirect('distribuidores:mis_paquetes')
                else:
                    return redirect('clientes:mis_hosts')
    
    return render(request, 'agregar_dominio.html', {
        'form': form, 
        'cliente': cliente,
        'dominio_validado': dominio_validado,
        'dominio_disponible': dominio_disponible,
        'dominio_existe': dominio_existe,
        'dominio_estado': dominio_estado,
        'dominio_web_activo': dominio_web_activo,
        'dominio_valor': dominio_valor,
        'from_distribuidor': from_distribuidor
    })

def generar_xml_interno(cliente, dominio):
    """
    Genera un XML interno para el equipo de ChibchaWeb
    """
    root = ET.Element('SolicitudDominio')
    ET.SubElement(root, 'Cliente').text = cliente.user.get_full_name() or cliente.user.username
    ET.SubElement(root, 'Email').text = cliente.user.email
    ET.SubElement(root, 'UserId').text = str(cliente.user.id)
    ET.SubElement(root, 'ClienteId').text = str(cliente.id)
    ET.SubElement(root, 'Dominio').text = dominio
    ET.SubElement(root, 'Plan').text = cliente.plan or "N/A"
    ET.SubElement(root, 'FechaSolicitud').text = str(timezone.now())
    
    # Guardar XML en directorio interno (opcional)
    xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    email = EmailMessage(
        subject="Solicitud de Dominio - ChibchaWeb",
        body="Adjunto XML de solicitud de dominio.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.EMAIL_PRUEBA],  # O cualquier destinatario
    )
    email.attach('solicitud_dominio.xml', xml_string, 'application/xml')
    email.send()

@cliente_required
def configurar_dominio(request, dominio_id):
    """Muestra datos del dominio y orientación DNS para el cliente."""
    cliente = request.cliente
    from_distribuidor = request.GET.get('from') == 'distribuidor'

    if not from_distribuidor and not cliente.suscripcion_activa:
        messages.warning(
            request,
            "Necesitas una suscripción activa para configurar dominios.",
        )
        return redirect('clientes:home_clientes')

    try:
        dominio = Dominios.objects.get(id=dominio_id, clienteId=cliente)
    except Dominios.DoesNotExist:
        messages.error(request, "El dominio no existe o no te pertenece.")
        if from_distribuidor:
            return redirect('distribuidores:mis_paquetes')
        return redirect('clientes:mis_hosts')

    return render(
        request,
        'configurar_dominio.html',
        {
            'dominio': dominio,
            'cliente': cliente,
            'from_distribuidor': from_distribuidor,
        },
    )


@cliente_required
def eliminar_dominio(request, dominio_id):
    """
    Vista para eliminar dominios del cliente
    """
    cliente = request.cliente
    
    # Verificar si viene desde un distribuidor
    from_distribuidor = request.GET.get('from') == 'distribuidor'
    
    try:
        dominio = Dominios.objects.get(id=dominio_id, clienteId=cliente)
    except Dominios.DoesNotExist:
        messages.error(request, "El dominio no existe o no te pertenece.")
        if from_distribuidor:
            return redirect('distribuidores:mis_paquetes')
        else:
            return redirect('clientes:mis_hosts')
    
    if request.method == 'POST':
        nombre_dominio = dominio.nombreDominio
        es_dominio_distribuidor = dominio.compraDistribuidor
        
        # Si era un dominio del distribuidor, decrementar el contador
        if es_dominio_distribuidor and hasattr(cliente, 'perfil_distribuidor'):
            distribuidor = cliente.perfil_distribuidor
            if distribuidor.paginas_vendidas > 0:
                distribuidor.paginas_vendidas -= 1
                distribuidor.save()
                precio_base = settings.PRECIO_POR_PAGINA_DISTRIBUIDOR
                monto_comision = precio_base * distribuidor.comision  # Negativo por agregar
                pago = PagoDistribuidor.objects.filter(cliente=cliente).order_by('-fecha').first()
                if pago:
                    direc = pago.direccion         # Instancia de Direccion o None
                    tarjeta = pago.tarjeta_usada  
                    PagoDistribuidor.objects.create(
                        cliente=cliente,
                        monto=monto_comision,
                        cantidad_paginas=1,
                        tarjeta_usada=tarjeta,
                        direccion=direc,
                        descripcion=f"Comisión por eliminar dominio '{dominio}'"
                    )
                messages.info(request, f"Se ha liberado 1 espacio en tu paquete de distribuidor. Tienes {distribuidor.paginas_disponibles} espacios disponibles.")
        
        dominio.delete()
        messages.success(request, f"El dominio '{nombre_dominio}' ha sido eliminado de tu cuenta exitosamente.")
        
        # Redirigir según el origen
        if from_distribuidor:
            return redirect('distribuidores:mis_paquetes')
        else:
            return redirect('clientes:mis_hosts')
    
    return render(request, 'eliminar_dominio.html', {
        'dominio': dominio,
        'cliente': cliente,
        'from_distribuidor': from_distribuidor
    })