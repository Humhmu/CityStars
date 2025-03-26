# CityStars_project/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from CityStars_app import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CityStars_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
    }
)

ASGI_APPLICATION = "ChatApp.asgi.application"
