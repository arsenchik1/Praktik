"""
ASGI config for API only (без сессий и статики)
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_api')

application = get_asgi_application()