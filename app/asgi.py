"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from .otel_config import setup_otel  # Import the setup function
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

# Initialize OpenTelemetry before creating the ASGI application
# You might want to get the app name from settings or an environment variable
APP_NAME = os.environ.get("OTEL_SERVICE_NAME", "anitrend")
setup_otel(APP_NAME)

# Wrap the ASGI application with OpenTelemetryMiddleware
application = OpenTelemetryMiddleware(app=get_asgi_application())
