from channels.routing import ProtocolTypeRouter, URLRouter

from v1.confirmation_blocks import routing as confirmation_blocks_routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        confirmation_blocks_routing.websocket_urlpatterns,
    )
})
