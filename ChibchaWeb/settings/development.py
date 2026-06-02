"""Development settings."""
from .base import *  # noqa: F403

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

# In local development we always use the console email backend so flows that
# send email (e.g. account activation) work without real SMTP credentials.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
