# Reporte parcial de pruebas de eficiencia - ChibchaWeb

Ejecución generada por `python -m pytest -q` o por el intérprete Python disponible del entorno local.
Base de datos: SQLite. No se modificaron modelos ni migraciones.

| No. | Escenario | Módulo | Tipo de prueba | Tiempo promedio | Tiempo máximo | TPM | CPU/RAM | Umbral | Resultado | Evidencia sugerida |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | Consulta de disponibilidad de dominio | Dominios.verificar_url | Vista HTTP con Django Test Client | 0.014727 s | 0.014727 s | - | - | < 1.0 s y sin HTTP 500 | APROBADO | Salida pytest y fila de reporte de disponibilidad |
| 2 | Creación de dominio y configuración inicial | Dominios.agregar_dominio | Vista HTTP con red/correo simulados | 0.048733 s | 0.048733 s | - | - | < 3.0 s y sin HTTP 500 | APROBADO | POST agregar_dominio con creación ORM verificada |
| 3 | Listado de dominios del cliente | Clientes.mis_hosts | Vista HTTP con datos semilla bulk_create | 0.285564 s | 0.285564 s | - | - | < 1.0 s y sin HTTP 500 | APROBADO | Salida pytest y reporte de listado |
| 4 | Búsqueda/filtro de dominios | Dominios ORM/SQLite | Capa de datos por ausencia de URL/vista | 0.002868 s | 0.002868 s | - | - | < 1.0 s | APROBADO CON TODO | Consulta ORM filtrada por nombre y compraDistribuidor |
| 5 | Actualización de dominio | Dominios ORM/SQLite | Capa de datos por ausencia de URL/vista | 0.000862 s | 0.000862 s | - | - | < 3.0 s | APROBADO CON TODO | UPDATE ORM sobre nombreDominio |
| 6 | Eliminación de dominio | Dominios.eliminar_dominio | Vista HTTP con Django Test Client | 0.013273 s | 0.013273 s | - | - | < 3.0 s y sin HTTP 500 | APROBADO | POST eliminar_dominio con borrado ORM verificado |
| 7 | Uso CPU/RAM bajo carga normal | Proceso pytest/Django | psutil sobre proceso local | 0.063045 s | 0.063045 s | - | CPU 0.00% / RAM 108.51 MB | CPU <= 70%; RAM <= 1 GB; referencia acta 512 MB a 1 GB | APROBADO CON JUSTIFICACIÓN LOCAL | Métrica psutil Process.cpu_percent y memory_info.rss |
| 8 | Throughput controlado 200 a 500 TPM | Dominios ORM/SQLite | Simulación secuencial controlada | 0.032707 s | 0.032707 s | 36689.51 | - | 200 <= TPM <= 500 o justificación local; carga < 5.0 s | APROBADO CON JUSTIFICACIÓN LOCAL | Cálculo TPM = (total_transacciones / duración_segundos) * 60 |
| 9 | Alta carga/concurrencia de lectura | Dominios ORM/SQLite | ThreadPoolExecutor con consultas ORM | 0.039506 s | 0.039506 s | - | - | < 5.0 s | APROBADO | 16 lecturas concurrentes controladas sobre SQLite |
| 10 | Tamaño del proyecto comprimido | Repositorio ChibchaWeb | ZIP temporal excluyendo .git, venv y cachés | 1.462848 s | 1.462848 s | - | Tamaño 0.71 MB | < 250 MB | APROBADO | Archivo temporal comprimido: 0.71 MB |
