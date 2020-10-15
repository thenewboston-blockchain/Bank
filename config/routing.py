from channels.routing import ProtocolTypeRouter, URLRouter

from v1.clean import routing as clean_routing
from v1.confirmation_blocks import routing as confirmation_blocks_routing
from v1.crawl import routing as crawl_routing
from v1.status_updates import routing as status_updates_routing
from v1.validator_confirmation_services import routing as validator_confirmation_services_routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        clean_routing.websocket_urlpatterns +
        confirmation_blocks_routing.websocket_urlpatterns +
        crawl_routing.websocket_urlpatterns +
        status_updates_routing.websocket_urlpatterns +
        validator_confirmation_services_routing.websocket_urlpatterns
    )
})
