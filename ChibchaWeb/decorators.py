"""Backward-compatible re-exports. Prefer ChibchaWeb.core.decorators."""
from ChibchaWeb.core.decorators import (  # noqa: F401
    admin_permission_required,
    administrador_required,
    agente_required,
    cliente_required,
    distribuidor_required,
    empleado_required,
    supervisor_required,
)
