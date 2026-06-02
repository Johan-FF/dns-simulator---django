from Clientes.models import Cliente





def cliente_context(request):

    if request.user.is_authenticated:

        try:

            cliente = Cliente.objects.select_related('user').get(user=request.user)

            return {'cliente': cliente}

        except Cliente.DoesNotExist:

            return {}

    return {}

