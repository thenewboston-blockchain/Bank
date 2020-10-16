from django.core.cache import cache

from v1.cache_tools.cache_keys import CLEAN_LAST_COMPLETED, CLEAN_STATUS
from v1.self_configurations.helpers.self_configuration import get_self_configuration


def get_clean_info():
    """
    Return standardized clean data for use in:
    - HTTP responses
    - WS messages
    """

    self_configuration = get_self_configuration(exception_class=RuntimeError)

    return {
        'clean_last_completed': cache.get(CLEAN_LAST_COMPLETED),
        'clean_status': cache.get(CLEAN_STATUS),
        'ip_address': self_configuration.ip_address,
        'port': self_configuration.port,
        'protocol': self_configuration.protocol
    }
