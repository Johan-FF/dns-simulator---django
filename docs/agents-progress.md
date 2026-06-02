# Registro de progreso de agentes



Última actualización: 2026-06-01



## Agente 1 — Verificación de escenarios desde el frontend



- Estado: **COMPLETADO**

- Objetivo: recorrer EO-01 a EO-17 desde la interfaz y corregir fallos

- Verificación automática (`python scripts/verify_all_eo.py`): **17/17 OK** (2026-06-01, Docker)

- Verificación en navegador: login cliente, historial de búsquedas y flujos principales OK en `http://localhost:8000`



### Checklist de escenarios



- [x] EO-01: Verificación de disponibilidad de un dominio

- [x] EO-02: Registro de nuevo cliente (cuenta persiste aunque falle el correo SMTP)

- [x] EO-03: Gestión de perfiles por admin

- [x] EO-04: Contratación de plan de hosting

- [x] EO-05: Edición de datos principales del perfil

- [x] EO-06: Gestión de tarjetas de crédito

- [x] EO-07: Creación de ticket de soporte

- [x] EO-08: Cerrar sesión

- [x] EO-09: Ver mis hosts

- [x] EO-10: Asignación de tickets (supervisor)

- [x] EO-11: Gestión de empleados (supervisor)

- [x] EO-12: Gestión de tickets (agente)

- [x] EO-13: Foto de perfil (formulario con campo `foto`)

- [x] EO-14: Historial de búsqueda de hosts

- [x] EO-15: Cambio de idioma (UI en inglés con prefijo `/en/`)

- [x] EO-16: Persistencia de idioma (`preferred_language`)

- [x] EO-17: Responsive (meta viewport en plantillas base)



### Correcciones aplicadas (Fase 1)



| Área | Cambio |

|------|--------|

| `ChibchaWeb/core/decorators.py` | Redirect de empleados: `empleados:log` (antes `empleados:login` inexistente) |

| `scripts/setup_test_users.py` | Teléfonos dentro de rango `IntegerField`; `eo_client` sin suscripción para EO-04; idioma `es` por defecto |

| `scripts/verify_all_eo.py` | URLs localizadas (`/en/...`); reset de idioma; EO-17 con ruta correcta |

| `Clientes/views.py` | Registro: usuario se guarda aunque falle el envío de correo |

| `Clientes/models.py` + migraciones | `preferred_language`, `HostSearchHistory`, `foto` |

| Middleware i18n | Persistencia y activación de idioma por perfil |



### Usuarios de prueba



| Usuario | Contraseña | Rol |

|---------|------------|-----|

| `eo_client` | `Test1234!` | Cliente |

| `eo_admin` | `TestAdmin123!` o `Test1234!` | Administrador |

| `eo_supervisor` | `Test1234!` | Supervisor |

| `eo_agent` | `Test1234!` | Agente |



---



## Agente 2 — Buenas prácticas, nombres en inglés/PascalCase y UI/UX



- Estado: **COMPLETADO** (alcance seguro, sin renombrar apps/URLs)



### Cambios aplicados



- Eliminación de logs de depuración temporales (`ChibchaWeb/views.py`, `Clientes/context_processors.py`)

- Atributo `lang` dinámico en `base.html` según `LANGUAGE_CODE`

- Decoradores y scripts alineados con convenciones del proyecto



### Fuera de alcance (requiere plan de migración)



- Renombrar rutas `Clientes/` → `clients/` u otras apps

- Cambiar `IntegerField` de teléfono a `CharField` (mejora de modelo)



---



## Comandos Docker



```powershell

cd c:\Users\Vortex\Documents\personal\ChibchaWeb

docker compose build

docker compose up -d

docker compose exec web python manage.py makemigrations Pagos Clientes --noinput

docker compose exec web python manage.py migrate --noinput

docker compose exec web python scripts/setup_test_users.py

docker compose exec web python scripts/verify_all_eo.py

```



App: **http://localhost:8000**



### SMTP (Docker Compose)



- Gmail SMTP configurado vía `.env` (`env_file` en `docker-compose.yml` → servicio `web`; sin secretos en el repo).
- Variables: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL` (ver `.env.example`).
- Prueba manual (2026-06-01): `send_mail` desde el contenedor → **OK** (sin error SMTP).
- Reproducir prueba:

```powershell
docker compose exec web python manage.py shell -c "from django.core.mail import send_mail; send_mail('Docker SMTP test', 'OK', None, ['noreplychibchaweb@gmail.com'], fail_silently=False)"
```



---



## Notas



- No se realizan commits salvo solicitud explícita del usuario.

- Código y commits en inglés; comunicación en español.

- Pruebas manuales detalladas: `docs/manual-testing-checklist.md`

