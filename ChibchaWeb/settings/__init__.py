"""
Default to development settings for local runs and backward compatibility.
Set DJANGO_SETTINGS_MODULE=ChibchaWeb.settings.production in production.
"""
from .development import *  # noqa: F403
