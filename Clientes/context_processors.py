from Clientes.models import Cliente
# #region agent log
import logging
_dbg = logging.getLogger('debug_491cc5')
# #endregion


def cliente_context(request):
    # #region agent log
    _dbg.debug('[H2] cliente_context called, user.is_authenticated=%s', request.user.is_authenticated)
    # #endregion
    if request.user.is_authenticated:
        try:
            cliente = Cliente.objects.select_related('user').get(user=request.user)
            # #region agent log
            _dbg.debug('[H2] cliente_context found cliente=%s', cliente)
            # #endregion
            return {'cliente': cliente}
        except Cliente.DoesNotExist:
            # #region agent log
            _dbg.debug('[H2] cliente_context DoesNotExist for user=%s', request.user)
            # #endregion
            return {}
        except Exception as exc:
            # #region agent log
            _dbg.error('[H2] cliente_context UNEXPECTED ERROR: %s', exc, exc_info=True)
            # #endregion
            return {}
    return {}
