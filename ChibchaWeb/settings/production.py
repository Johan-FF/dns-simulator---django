"""Production settings."""
from .base import *  # noqa: F403

DEBUG = env.bool('DEBUG', default=False)  # noqa: F405

DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default='postgres://chibcha:chibcha@db:5432/chibcha',
    )
}

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
