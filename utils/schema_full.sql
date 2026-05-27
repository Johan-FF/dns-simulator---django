PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

CREATE TABLE "Administradores_administrador" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "activo" bool NOT NULL, "fecha_registro" datetime NOT NULL, "ultimo_acceso" datetime NULL, "puede_gestionar_usuarios" bool NOT NULL, "puede_ver_estadisticas" bool NOT NULL, "puede_gestionar_pagos" bool NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Clientes_cliente" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "telefono" integer NOT NULL, "tiene_suscripcion" bool NOT NULL, "plan" varchar(50) NULL, "fecha_inicio_suscripcion" datetime NULL, "fecha_fin_suscripcion" datetime NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "es_distribuidor" bool NOT NULL);

CREATE TABLE "Distribuidor_distribuidor" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tipo" varchar(10) NOT NULL, "cantidad_dominios" integer unsigned NOT NULL CHECK ("cantidad_dominios" >= 0), "cliente_id" bigint NOT NULL UNIQUE REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED, "paginas_vendidas" integer unsigned NOT NULL CHECK ("paginas_vendidas" >= 0));

CREATE TABLE "Dominios" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombreDominio" varchar(255) NOT NULL UNIQUE, "clienteId" bigint NOT NULL REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED, "compraDistribuidor" bool NOT NULL);

CREATE TABLE "Empleados_empleado" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "telefono" integer NOT NULL, "activo" bool NOT NULL, "rol" varchar(50) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "nivel" integer NOT NULL);

CREATE TABLE "Estado" ("idEstado" integer NOT NULL PRIMARY KEY, "nombreEstado" varchar(50) NOT NULL);

CREATE TABLE "HistoriaTicket" ("idCambioTicket" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "modDescripcion" varchar(250) NOT NULL, "fecha_modificacion" date NOT NULL, "idEmpleado" bigint NULL REFERENCES "Empleados_empleado" ("id") DEFERRABLE INITIALLY DEFERRED, "idEstado" integer NULL REFERENCES "Estado" ("idEstado") DEFERRABLE INITIALLY DEFERRED, "idTicket" integer NOT NULL REFERENCES "Ticket" ("idTicket") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Pagos_direccion" ("direccionId" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ubicacion" varchar(50) NOT NULL, "codigoPostal" varchar(10) NOT NULL, "cliente_id" bigint NOT NULL REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED, "pais_id" integer NOT NULL REFERENCES "Pagos_pais" ("paisId") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Pagos_pago" ("pagoId" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "monto" decimal NOT NULL, "fecha" datetime NOT NULL, "cliente_id" bigint NOT NULL REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED, "direccion_id" integer NULL REFERENCES "Pagos_direccion" ("direccionId") DEFERRABLE INITIALLY DEFERRED, "tarjeta_usada_id" bigint NULL REFERENCES "Pagos_tarjetacredito" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Pagos_pagodistribuidor" ("pago_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "Pagos_pago" ("pagoId") DEFERRABLE INITIALLY DEFERRED, "cantidad_paginas" integer unsigned NOT NULL CHECK ("cantidad_paginas" >= 0), "descripcion" varchar(255) NOT NULL);

CREATE TABLE "Pagos_pais" ("paisId" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(20) NOT NULL);

CREATE TABLE "Pagos_tarjetacredito" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "numero" varchar(16) NOT NULL, "nombre_titular" varchar(50) NOT NULL, "fecha_expiracion" varchar(5) NOT NULL, "cvv" varchar(4) NOT NULL, "cliente_id" bigint NOT NULL REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "Ticket" ("idTicket" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombreTicket" varchar(50) NOT NULL, "descripcionTicket" varchar(250) NOT NULL, "fechar_creacion" date NOT NULL, "clienteId" bigint NOT NULL REFERENCES "Clientes_cliente" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);

CREATE TABLE "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);

CREATE TABLE "auth_user" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "username" varchar(150) NOT NULL UNIQUE, "last_name" varchar(150) NOT NULL, "email" varchar(254) NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "date_joined" datetime NOT NULL, "first_name" varchar(150) NOT NULL);

CREATE TABLE "auth_user_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "auth_user_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);

CREATE TABLE "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);

CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);

CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE INDEX "Dominios_clienteId_abec4a6a" ON "Dominios" ("clienteId");

CREATE INDEX "HistoriaTicket_idEmpleado_394684c9" ON "HistoriaTicket" ("idEmpleado");

CREATE INDEX "HistoriaTicket_idEstado_14001385" ON "HistoriaTicket" ("idEstado");

CREATE INDEX "HistoriaTicket_idTicket_67202fe4" ON "HistoriaTicket" ("idTicket");

CREATE INDEX "Pagos_direccion_cliente_id_3001a4a9" ON "Pagos_direccion" ("cliente_id");

CREATE INDEX "Pagos_direccion_pais_id_d25b4e83" ON "Pagos_direccion" ("pais_id");

CREATE INDEX "Pagos_pago_cliente_id_b529f3bb" ON "Pagos_pago" ("cliente_id");

CREATE INDEX "Pagos_pago_direccion_id_306565ab" ON "Pagos_pago" ("direccion_id");

CREATE INDEX "Pagos_pago_tarjeta_usada_id_709fbc03" ON "Pagos_pago" ("tarjeta_usada_id");

CREATE INDEX "Pagos_tarjetacredito_cliente_id_907e9346" ON "Pagos_tarjetacredito" ("cliente_id");

CREATE INDEX "Ticket_clienteId_7c4b08ec" ON "Ticket" ("clienteId");

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");

CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");

CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");

CREATE INDEX "auth_user_groups_group_id_97559544" ON "auth_user_groups" ("group_id");

CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" ("user_id");

CREATE UNIQUE INDEX "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" ("user_id", "group_id");

CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" ("permission_id");

CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" ("user_id");

CREATE UNIQUE INDEX "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" ("user_id", "permission_id");

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");

CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

COMMIT;
PRAGMA foreign_keys = ON;
