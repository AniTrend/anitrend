"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from .otel_config import setup_otel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.production')

# Initialize OpenTelemetry before creating the WSGI application
APP_NAME = os.environ.get("OTEL_SERVICE_NAME", "anitrend")
setup_otel(APP_NAME)

application = get_wsgi_application()
