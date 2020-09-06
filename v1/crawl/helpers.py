from django.core.cache import cache

from v1.cache_tools.cache_keys import CRAWL_LAST_COMPLETED, CRAWL_STATUS


def get_crawl_info():
    """
    Return standardized crawl data for use in:
    - HTTP responses
    - WS messages
    """

    return {
        'crawl_last_completed': cache.get(CRAWL_LAST_COMPLETED),
        'crawl_status': cache.get(CRAWL_STATUS)
    }
