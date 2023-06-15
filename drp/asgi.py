"""
ASGI config for drp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drp.settings')
django.setup()

django_asgi_app = get_asgi_application()

from channels.layers import get_channel_layer
from main.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
         "websocket": AllowedHostsOriginValidator(
             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
         ),
         'channel': get_channel_layer(),
    }
)
