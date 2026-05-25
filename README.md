# ChibchaWeb

Django hosting and domain management platform.

## Requirements

- Python 3.11+
- Conda env `p` (recommended) or virtualenv
- PostgreSQL (Docker) or SQLite (local dev)

## Local setup

```bash
conda activate p
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set SECRET_KEY
python manage.py migrate
python manage.py runserver
```

Settings are split under `ChibchaWeb/settings/` (`development` by default, `production` for Docker).

## Docker

```bash
cp .env.example .env
# Set SECRET_KEY and DATABASE_URL in .env
docker compose build
docker compose up
```

App: http://localhost:8000/

PostgreSQL runs as service `db`. Migrations and `collectstatic` run via `docker/entrypoint.sh`.

## i18n

See [docs/i18n.md](docs/i18n.md). Quick workflow:

```bash
python manage.py makemessages -l en -l pt
python scripts/translate_po.py --all
python manage.py compilemessages
```

## Tests

```bash
conda activate p
python manage.py test ChibchaWeb.tests
python manage.py check
```

## URLs (overview)

- `/` — public home
- `/login/` — client login
- `/Clientes/` — registration and client area
- `/administradores/` — admin panel
- `/empleados/` — staff portal
- `/pagos/` — payments and subscriptions
- `/dominios/` — domain verification (`verificar-url` lives here only)

## Security notes

- Secrets via environment variables (see `.env.example`)
- Credit cards store `last4` + `payment_token` only (no PAN/CVV)
- Admin client list: `Clientes/admin/lista/` (not public)
