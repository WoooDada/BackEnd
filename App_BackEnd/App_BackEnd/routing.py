
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
import yolo.routing


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
            URLRouter(
                    yolo.routing.websocket_urlpatterns
            )
        ),

})