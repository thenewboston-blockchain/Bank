from django.core.cache import cache

from v1.cache_tools.cache_keys import CLEAN_LAST_COMPLETED, CLEAN_STATUS


def get_clean_info():
    """
    Return standardized clean data for use in:
    - HTTP responses
    - WS messages
    """

    return {
        'clean_last_completed': cache.get(CLEAN_LAST_COMPLETED),
        'clean_status': cache.get(CLEAN_STATUS)
    }
