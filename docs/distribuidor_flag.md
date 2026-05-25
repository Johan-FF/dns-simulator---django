# Distributor flag (`es_distribuidor`)

**Single source of truth:** `Cliente.es_distribuidor` on the `Clientes.Cliente` model.

- Setting `es_distribuidor = True` triggers `Distribuidor` app signals to create/update `perfil_distribuidor`.
- UI and decorators (`distribuidor_required`) read `cliente.es_distribuidor`.
- Do not duplicate distributor status on `User` or other models; use the `Distribuidor` profile for inventory (`cantidad_dominios`, pages sold, etc.).
