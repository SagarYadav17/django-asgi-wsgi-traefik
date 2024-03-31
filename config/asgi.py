import os

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_asgi_application()


from config.consumers import ChatConsumer  # noqa: E402


# Create the ProtocolTypeRouter
application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            URLRouter(
                [
                    path("ws/chat/", ChatConsumer.as_asgi()),
                ],
            )
        ),
    }
)
