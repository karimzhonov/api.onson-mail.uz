"""
ASGI config for api_onson_mail project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_onson_mail.settings')
django.setup()

from .routing import websocket_urlpatterns
from .middleware import WebsocketMiddlewareStack

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebsocketMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
