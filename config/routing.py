from channels.routing import ProtocolTypeRouter, URLRouter

from thenewboston_bank.clean import routing as clean_routing
from thenewboston_bank.confirmation_blocks import routing as confirmation_blocks_routing
from thenewboston_bank.crawl import routing as crawl_routing
from thenewboston_bank.status_updates import routing as status_updates_routing
from thenewboston_bank.validator_confirmation_services import routing as validator_confirmation_services_routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        clean_routing.websocket_urlpatterns
        + confirmation_blocks_routing.websocket_urlpatterns
        + crawl_routing.websocket_urlpatterns
        + status_updates_routing.websocket_urlpatterns
        + validator_confirmation_services_routing.websocket_urlpatterns
    )
})
