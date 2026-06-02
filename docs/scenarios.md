ESCENARIOS OPERACIONALES. 

EO-01: Verificación de disponibilidad de un dominio 

Stakeholder 

Usuario  

ID 

EO-01 

Descripción general de la funcionalidad 

Permitir que un usuario verifique si un nombre de dominio está disponible para su registro mediante la herramienta de verificación de URL. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere comprobar si un nombre de dominio que le interesa está libre para registrarlo. 

Describa cualquier entrada provista o disponible al momento del inicio 

Nombre de dominio introducido por el usuario (ej. misitio.com). 

Describa el contexto de la operación 

El usuario accede a la sección “Dominios” de ChibchaWeb y utiliza la herramienta de verificación. 

Describa cómo el sistema debe responder 

Consultar la disponibilidad del dominio en los registradores asociados y mostrar el resultado (disponible / no disponible). 

Describa las salidas que el sistema produce como resultado de la acción 

Mensaje indicando disponibilidad del dominio. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario utiliza la salida para decidir si continúa con el registro del dominio; el sistema utiliza la información para iniciar el flujo de compra si procede. 

Tabla No 1. Escenario operacional Verificación de disponibilidad de un dominio 

 

 

 

 

 

 

 

 

 

 

EO-02: Registro de nuevo cliente 

Stakeholder 

Cliente 

ID 

EO-02 

Descripción general de la funcionalidad 

Permitir que un usuario cree una cuenta como cliente en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere registrarse para poder contratar servicios de hosting. 

Describa cualquier entrada provista o disponible al momento del inicio 

Datos personales del cliente: nombre, correo electrónico, teléfono, contraseña, etc. 

Describa el contexto de la operación 

El usuario selecciona “Registrarse” en la plataforma y completa el formulario. 

Describa cómo el sistema debe responder 

Validar los datos, guardar la información en la base de datos y confirmar el registro. 

Describa las salidas que el sistema produce como resultado de la acción 

Mensaje de confirmación y cuenta creada. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente usa la confirmación para acceder a su cuenta; el sistema utiliza los datos para habilitar el perfil y permitir el uso de servicios. 

Tabla No 2. Escenario operacional Registro de nuevo cliente 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

EO-03: Gestión de perfiles de cliente, empleado y distribuidor 

Stakeholder 

Administrador 

ID 

EO-03 

Descripción general de la funcionalidad 

Permitir la búsqueda, visualización, edición y eliminación de perfiles en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El administrador podrá modificar la información de clientes, empleados y distribuidores, además de poder crearlos o eliminarlos. 

Describa cualquier entrada provista o disponible al momento del inicio 

Criterios de búsqueda o datos del perfil a modificar/eliminar. 

Describa el contexto de la operación 

El administrador inicia sesión y accede al módulo de gestión de perfiles. 

Describa cómo el sistema debe responder 

Mostrar la información solicitada, permitir modificaciones y guardar los cambios o eliminar el perfil. 

Describa las salidas que el sistema produce como resultado de la acción 

Datos actualizados o perfil eliminado; mensaje de confirmación. 

Describa quién o qué usa la salida y para qué es utilizada 

El administrador usa la salida para verificar cambios; el sistema actualiza la base de datos y refleja los cambios en tiempo real. 

Tabla No 3. Escenario operacional Gestión de perfiles de cliente, empleado y distribuidor 

 

 

 

 

 

 

 

 

 

 

EO-04: Contratación de plan de hosting por parte de un cliente 

Stakeholder 

Cliente 

ID 

EO-04 

Descripción general de la funcionalidad 

Permitir que un cliente sin plan activo seleccione y contrate uno de los planes de hosting disponibles. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere activar un plan de hosting con una modalidad de pago definida. 

Describa cualquier entrada provista o disponible al momento del inicio 

Catálogo de planes y modalidades, dirección de facturación, datos de tarjeta de crédito. 

Describa el contexto de la operación 

El cliente accede a “Mi perfil” y el sistema detecta que no tiene plan activo. 

Describa cómo el sistema debe responder 

Mostrar planes y modalidades, registrar tarjeta si no existe, generar resumen de compra, procesar pago y activar el plan. 

Describa las salidas que el sistema produce como resultado de la acción 

Confirmación de compra, plan activo, comprobante de pago. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente para confirmar la activación; el sistema para habilitar el servicio; el área contable para registrar la transacción. 

Tabla No 4. Escenario operacional Contratación de plan de hosting por parte de un cliente 

 

 

 

 

 

 

 

 

 

 

EO-05: Edición de datos principales del perfil 

Stakeholder 

Cliente 

ID 

EO-05 

Descripción general de la funcionalidad 

Permitir al cliente modificar su información personal en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere actualizar datos como nombre, correo, teléfono y dirección. 

Describa cualquier entrada provista o disponible al momento del inicio 

Datos actuales del perfil y nuevos datos ingresados por el cliente. 

Describa el contexto de la operación 

El cliente accede a la sección “Configuración” y selecciona “Editar”. 

Describa cómo el sistema debe responder 

Validar la nueva información y guardarla en la base de datos. 

Describa las salidas que el sistema produce como resultado de la acción 

Mensaje de confirmación y datos actualizados. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente verifica que sus datos estén correctos; el sistema actualiza la información para futuros procesos. 

Tabla No 5. Escenario operacional Edición de datos principales del perfil 

 

 

 

 

 

 

 

 

 

 

 

EO-06: Gestión de tarjetas de crédito 

Stakeholder 

Cliente 

ID 

EO-06 

Descripción general de la funcionalidad 

Permitir al cliente agregar o eliminar tarjetas de crédito en su cuenta. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere registrar nuevas tarjetas o eliminar las existentes. 

Describa cualquier entrada provista o disponible al momento del inicio 

Datos de la tarjeta (número, fecha de vencimiento, código de seguridad, titular) o tarjeta seleccionada para eliminación. 

Describa el contexto de la operación 

El cliente accede a “Configuración” > “Tarjetas de crédito”. 

Describa cómo el sistema debe responder 

Validar y registrar nueva tarjeta o eliminar tarjeta seleccionada, actualizando la base de datos. 

Describa las salidas que el sistema produce como resultado de la acción 

Lista actualizada de tarjetas y mensaje de confirmación. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente para gestionar sus métodos de pago; el sistema para procesar futuros cobros. 

Tabla No 6. Escenario operacional Gestión de tarjetas de crédito 

 

 

 

 

 

 

 

 

 

 

 

EO-07: Creación de un ticket de soporte 

Stakeholder 

Cliente 

ID 

EO-07 

Descripción general de la funcionalidad 

Permitir que el cliente cree un ticket para reportar problemas técnicos o solicitudes de soporte. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere notificar un problema y obtener asistencia técnica. 

Describa cualquier entrada provista o disponible al momento del inicio 

Asunto y descripción del problema ingresados por el cliente. 

Describa el contexto de la operación 

El cliente accede a “Crear ticket” en la plataforma. 

Describa cómo el sistema debe responder 

Generar un número de ticket, registrar fecha y hora, clasificarlo y enviarlo al equipo de soporte. 

Describa las salidas que el sistema produce como resultado de la acción 

Ticket creado con ID único y notificación al cliente. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente para hacer seguimiento; el equipo de soporte para atender la solicitud. 

Tabla No 7. Escenario operacional Creación de un ticket de soporte 

 

 

 

 

 

 

 

 

 

 

EO-08: Cerrar sesión 

Stakeholder 

Cliente / Administrador / Empleado / Distribuidor 

ID 

EO-07 

Descripción general de la funcionalidad 

Permitir que un usuario cierre su sesión de forma segura en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere salir de su cuenta y asegurarse de que nadie más acceda a su información sin iniciar sesión nuevamente. 

Describa cualquier entrada provista o disponible al momento del inicio 

Sesión activa del usuario en el sistema. 

Describa el contexto de la operación 

El usuario ha terminado de realizar sus actividades y selecciona “Cerrar sesión” en la interfaz. 

Describa cómo el sistema debe responder 

Invalidar la sesión, limpiar datos temporales, redirigir al usuario a la página de inicio y mostrar un mensaje de confirmación. 

Describa las salidas que el sistema produce como resultado de la acción 

Sesión cerrada, token de autenticación invalidado. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario confirma que ha salido correctamente; el sistema asegura la integridad y seguridad de la cuenta. 

Tabla No 8. Escenario operacional Cerrar sesión 

 

 

 

 

 

 

 

 

 

 

EO-09: Ver mis hosts 

Stakeholder 

Cliente 

ID 

EO-08 

Descripción general de la funcionalidad 

Permitir que un cliente consulte los sitios web que tiene alojados en su cuenta. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere ver un listado de sus hosts con detalles y opciones de gestión. 

Describa cualquier entrada provista o disponible al momento del inicio 

Sesión activa del cliente, datos de hosts registrados en la cuenta. 

Describa el contexto de la operación 

El cliente accede a la sección “Mis hosts” desde su panel principal. 

Describa cómo el sistema debe responder 

Mostrar lista de hosts con nombre, plan, estado, fecha de vencimiento y opciones de gestión. 

Describa las salidas que el sistema produce como resultado de la acción 

Listado de hosts y acceso a acciones como renovar, editar o eliminar. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente para administrar sus sitios web; el sistema para permitir operaciones sobre los hosts. 

Tabla No 9. Escenario operacional Ver mis hosts 

 

 

 

 

 

 

 

 

 

 

 

EO-10: Asignación de tickets por parte del supervisor 

Stakeholder 

Supervisor 

ID 

EO-09 

Descripción general de la funcionalidad 

Permitir que el supervisor gestione y asigne tickets a los agentes de soporte según el nivel y especialidad requeridos. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El supervisor quiere distribuir los tickets entrantes entre los agentes disponibles, priorizando según la complejidad. 

Describa cualquier entrada provista o disponible al momento del inicio 

Lista de tickets pendientes, información del nivel de servicio de cada ticket, disponibilidad de agentes y sus niveles de soporte. 

Describa el contexto de la operación 

El supervisor accede al dashboard de gestión de tickets desde su cuenta y revisa los casos pendientes. 

Describa cómo el sistema debe responder 

Mostrar todos los tickets sin asignar, permitir seleccionar un ticket y asignarlo a un agente específico, actualizar el estado del ticket. 

Describa las salidas que el sistema produce como resultado de la acción 

Ticket asignado con registro del agente responsable y fecha. 

Describa quién o qué usa la salida y para qué es utilizada 

El agente usa la notificación para iniciar la atención del caso; el sistema actualiza el flujo de trabajo y el historial del ticket. 

Tabla No 10. Escenario operacional Asignación de tickets por parte del supervisor 

 

 

 

 

 

 

 

 

 

EO-11: Gestión de empleados por parte del supervisor 

Stakeholder 

Empleado/Supervisor 

ID 

EO-10 

Descripción general de la funcionalidad 

Permitir que el supervisor gestione la información y estado de los empleados desde el panel de control. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El supervisor quiere visualizar, registrar, editar o desactivar empleados de su equipo. 

Describa cualquier entrada provista o disponible al momento del inicio 

Lista de empleados registrados, datos personales y de contacto, roles y estado laboral. 

Describa el contexto de la operación 

El supervisor accede a la sección “Gestión de empleados” ubicada en el panel inferior del dashboard. 

Describa cómo el sistema debe responder 

Mostrar lista de empleados, permitir añadir nuevos registros, editar información existente, asignar nivel. 

Describa las salidas que el sistema produce como resultado de la acción 

Datos actualizados de empleados o nuevos registros guardados; confirmación de cambios. 

Describa quién o qué usa la salida y para qué es utilizada 

El supervisor para administrar su equipo; el sistema para mantener actualizada la información de recursos humanos. 

Tabla No 11. Escenario operacional Gestión de empleados por parte del supervisor 

 

 

 

 

 

 

 

 

 

EO-12: Gestión de tickets por parte del agente 

Stakeholder 

Empleado / Agente de soporte 

ID 

EO-11 

Descripción general de la funcionalidad 

Permitir que el agente gestione los tickets que se le han asignado y consulte el historial de tickets resueltos. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El agente quiere ver los tickets que tiene asignados, actualizarlos conforme avanza su resolución y consultar los tickets que ya ha cerrado. 

Describa cualquier entrada provista o disponible al momento del inicio 

Lista de tickets asignados, detalles de cada ticket (ID, asunto, descripción, prioridad, fecha de asignación) e historial de tickets resueltos. 

Describa el contexto de la operación 

El agente accede a la sección “Mis tickets” desde su cuenta en la plataforma. 

Describa cómo el sistema debe responder 

Mostrar lista de tickets asignados con opciones para actualizar su estado y añadir comentarios, así como permitir la consulta del historial de tickets resueltos. 

Describa las salidas que el sistema produce como resultado de la acción 

Tickets actualizados con nuevo estado, comentarios añadidos, historial consultado. 

Describa quién o qué usa la salida y para qué es utilizada 

El agente para gestionar y hacer seguimiento de los tickets; el sistema para registrar el progreso y mantener actualizado el historial de soporte. 

Tabla No 12. Escenario operacional Gestión de tickets por parte del agente 

 

 

 

 

 

 

 

 

EO-13: Cargar y actualizar foto de perfil 

ID 

EO-12 

Descripción general de la funcionalidad 

Permitir que el usuario cargue y actualice su foto de perfil en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere personalizar su perfil agregando o cambiando su foto de perfil. 

Describa cualquier entrada provista o disponible al momento del inicio 

Archivo de imagen seleccionado por el usuario (jpg, png), sesión activa. 

Describa el contexto de la operación 

El usuario accede a su perfil y selecciona la opción “Cambiar foto de perfil”. 

Describa cómo el sistema debe responder 

Validar el formato y tamaño de la imagen, almacenar la foto y asociarla al perfil del usuario. 

Describa las salidas que el sistema produce como resultado de la acción 

Foto de perfil actualizada y mensaje de confirmación. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario visualiza su foto actualizada; el sistema la muestra en sesiones, tickets y paneles. 

Tabla No 13. Escenario operacional Cambio de foto de perfil por parte del usuario 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

EO-14: Visualización del historial de búsqueda de hosts 

ID 

EO-13 

Descripción general de la funcionalidad 

Permitir que el cliente consulte el historial de búsquedas realizadas sobre hosts en la plataforma. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El cliente quiere revisar los hosts que ha buscado previamente para retomar decisiones o comparaciones. 

Describa cualquier entrada provista o disponible al momento del inicio 

Sesión activa del cliente, registros históricos de búsqueda. 

Describa el contexto de la operación 

El cliente accede a la sección “Historial de búsquedas” desde su panel principal. 

Describa cómo el sistema debe responder 

Consultar y mostrar el historial ordenado por fecha, incluyendo filtros básicos. 

Describa las salidas que el sistema produce como resultado de la acción 

Listado de búsquedas realizadas con fecha, criterio y resultado. 

Describa quién o qué usa la salida y para qué es utilizada 

El cliente usa la información para comparar opciones; el sistema mantiene trazabilidad de uso. 

Tabla No 14. Escenario operacional consulta de historial por parte del cliente 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

EO-15: Cambio de idioma de la plataforma 

ID 

EO-14 

Descripción general de la funcionalidad 

Permitir al usuario cambiar el idioma de la interfaz entre español e inglés. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere navegar la plataforma en el idioma de su preferencia. 

Describa cualquier entrada provista o disponible al momento del inicio 

Idioma seleccionado por el usuario (español o inglés). 

Describa el contexto de la operación 

El usuario selecciona el idioma desde la página principal o configuración del perfil. 

Describa cómo el sistema debe responder 

Actualizar la interfaz de usuario y textos dinámicos al idioma seleccionado. 

Describa las salidas que el sistema produce como resultado de la acción 

Interfaz mostrada en el idioma seleccionado. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario para mejorar su experiencia; el sistema para internacionalización del producto. 

Tabla No 15. Escenario operacional cambio de idioma de la interfaz 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

 

EO-16: Guardar preferencia de idioma del usuario 

ID 

EO-15 

Descripción general de la funcionalidad 

Permitir que el sistema recuerde el idioma preferido del usuario para futuras sesiones. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere que la plataforma conserve su idioma seleccionado al volver a iniciar sesión. 

Describa cualquier entrada provista o disponible al momento del inicio 

Idioma seleccionado y sesión autenticada. 

Describa el contexto de la operación 

El usuario cambia el idioma y continúa usando la plataforma. 

Describa cómo el sistema debe responder 

Guardar la preferencia de idioma asociada al perfil del usuario. 

Describa las salidas que el sistema produce como resultado de la acción 

Idioma persistido en el perfil del usuario. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario para mantener consistencia; el sistema para personalizar la interfaz automáticamente. 

Tabla No 16. Escenario operacional persistencia de idioma.  

 

 

 

 

 

 

 

 

 

 

 

 

EO-17: Visualización responsive de la plataforma 

ID 

EO-16 

Descripción general de la funcionalidad 

Permitir que la plataforma se adapte correctamente a distintos tamaños de pantalla. 

Describa lo que el stakeholder hace ahora o le gustaría poder hacer 

El usuario quiere acceder al sistema desde computador, tablet o celular sin pérdida de funcionalidad. 

Describa cualquier entrada provista o disponible al momento del inicio 

Dispositivo del usuario y tamaño de pantalla. 

Describa el contexto de la operación 

El usuario accede a la plataforma desde diferentes dispositivos. 

Describa cómo el sistema debe responder 

Ajustar automáticamente la disposición visual y componentes de la interfaz. 

Describa las salidas que el sistema produce como resultado de la acción 

Interfaz adaptada correctamente al dispositivo. 

Describa quién o qué usa la salida y para qué es utilizada 

El usuario para una mejor experiencia; el sistema para garantizar accesibilidad y usabilidad. 

Tabla No 17. Escenario operacional diseño responsive de la interfaz. 