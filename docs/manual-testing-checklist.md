# Lista de verificación manual (Docker)



Guía para probar ChibchaWeb en el navegador con **Docker Compose**. La verificación automática (`scripts/verify_all_eo.py`) cubre humo HTTP; esta lista valida la experiencia real del usuario.



## Requisitos previos



1. Docker Desktop en ejecución.

2. Ejecutar desde la raíz del proyecto:



```powershell

cd c:\Users\Vortex\Documents\personal\ChibchaWeb

docker compose build

docker compose up -d

docker compose exec web python manage.py migrate --noinput

docker compose exec web python scripts/setup_test_users.py

```



3. Abrir **http://localhost:8000**

4. Contraseña de usuarios de prueba: **`Test1234!`** (admin: `TestAdmin123!` si aplica)



---



## EO-01 — Verificación de dominio



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Ir a **Dominios** (`/dominios/`) | Formulario de verificación visible |

| 2 | Ingresar `prueba-manual-123.com` y enviar | Mensaje de disponibilidad o no disponible |

| 3 | (Opcional, con sesión cliente) Repetir búsqueda | Entrada aparece luego en historial (EO-14) |



---



## EO-02 — Registro de cliente



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | **Registrarse** → completar formulario con usuario nuevo | Redirección a página de éxito o mensaje claro |

| 2 | Intentar login con el nuevo usuario | Acceso según activación de cuenta configurada |



> Nota: en Docker el correo SMTP puede fallar; la cuenta debe crearse igualmente.



---



## EO-03 — Admin: gestión de usuarios



| Usuario | `eo_admin` |

| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Login en **Portal Administradores** | Dashboard admin |

| 2 | Ir a **Usuarios** (`/administradores/usuarios/`) | Lista de usuarios, opciones crear/editar |



---



## EO-04 — Contratación de plan (cliente)



| Usuario | `eo_client` (sin suscripción activa tras `setup_test_users.py`) |

| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Login cliente → **Ver Planes** o `/pagos/seleccionar-plan/` | Catálogo de planes |

| 2 | Elegir plan y avanzar en el flujo | Formularios de dirección/tarjeta o resumen según estado |



---



## EO-05 — Editar perfil



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | **Configuración** (`/Clientes/detalle/`) | Datos del cliente visibles |

| 2 | **Editar perfil** | Formulario guarda cambios con mensaje de éxito |



---



## EO-06 — Tarjetas de crédito



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | `/pagos/registrar-tarjeta/` | Formulario de tarjeta |

| 2 | Registrar tarjeta de prueba (datos de demo) | Tarjeta listada o confirmación |

| 3 | Eliminar tarjeta (si la UI lo permite) | Lista actualizada |



---



## EO-07 — Crear ticket



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | `/tickets/nuevo/` o menú **Crear Ticket** | Formulario asunto/descripción |

| 2 | Enviar ticket | Confirmación o ticket en listado cliente |



---



## EO-08 — Cerrar sesión



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Menú **Cerrar sesión** | Redirección a inicio/login |

| 2 | Volver a ruta protegida | Pide login de nuevo |



---



## EO-09 — Mis hosts



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | `/Clientes/mis-hosts/` | Listado (vacío o con hosts) sin error 404 |

| 2 | Si requiere suscripción | Mensaje o enlace a contratar plan |



---



## EO-10 / EO-11 — Supervisor



| Usuario | `eo_supervisor` |

| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Login **Portal Empleados** (`/empleados/log/`) | Dashboard supervisor |

| 2 | Revisar tickets sin asignar y empleados | Listas y acciones de asignación/gestión |



---



## EO-12 — Agente



| Usuario | `eo_agent` |

| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Login empleados | Dashboard agente |

| 2 | **Mis tickets** (`/empleados/mis-tickets/`) | Tickets asignados y opciones de actualización |



---



## EO-13 — Foto de perfil



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Editar perfil → sección **Foto de perfil** | Input `foto` visible |

| 2 | Subir imagen JPG/PNG pequeña | Vista previa o foto en perfil tras guardar |



---



## EO-14 — Historial de búsquedas



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Buscar dominio en **Dominios** (logueado como cliente) | — |

| 2 | `/Clientes/historial-busquedas/` | Tabla con dominio, fecha y resultado |



---



## EO-15 / EO-16 — Idioma



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Selector **English** en barra superior | UI en inglés; URL puede usar prefijo `/en/` |

| 2 | Cerrar sesión y volver a entrar | Interfaz mantiene inglés (`preferred_language`) |

| 3 | Cambiar a **Español** | UI en español |



---



## EO-17 — Diseño responsive



| Paso | Acción | Resultado esperado |

|------|--------|-------------------|

| 1 | Abrir inicio y dashboard cliente | Sin scroll horizontal roto |

| 2 | Reducir ventana a ~375px (móvil) o DevTools | Menú hamburguesa usable, contenido legible |

| 3 | Comprobar en login y admin | Meta viewport presente (no zoom forzado raro) |



---



## Verificación rápida automatizada



```powershell

docker compose exec web python scripts/verify_all_eo.py

```



Debe terminar con **0 FAIL**.



---



## Problemas frecuentes



| Síntoma | Causa probable | Solución |

|---------|----------------|----------|

| 404 en rutas tras cambiar idioma | Prefijo `/en/` requerido | Usar enlaces del sitio o `/en/ruta/` |

| `eo_supervisor` / `eo_agent` no entran | Usuarios no creados | `docker compose exec web python scripts/setup_test_users.py` |

| Contenedor web no arranca | BD no lista | `docker compose logs db` y esperar healthcheck |

| Correo de registro no llega | SMTP no configurado en `.env` | Normal en local; verificar que la cuenta se creó |



---



## Registro de prueba (opcional)



| Fecha | Probador | EO probados | Incidencias |

|-------|----------|-------------|-------------|

| | | | |

