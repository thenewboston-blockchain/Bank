from django.core.cache import cache

from thenewboston_bank.cache_tools.cache_keys import CRAWL_LAST_COMPLETED, CRAWL_STATUS
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration


def get_crawl_info():
    """
    Return standardized crawl data for use in:

    - HTTP responses
    - WS messages
    """
    self_configuration = get_self_configuration(exception_class=RuntimeError)

    return {
        'crawl_last_completed': cache.get(CRAWL_LAST_COMPLETED),
        'crawl_status': cache.get(CRAWL_STATUS),
        'ip_address': self_configuration.ip_address,
        'port': self_configuration.port,
        'protocol': self_configuration.protocol
    }
