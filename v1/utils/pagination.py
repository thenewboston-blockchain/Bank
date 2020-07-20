from rest_framework.pagination import LimitOffsetPagination

from config.settings.base import (
    PAGINATION_DEFAULT_LIMIT,
    PAGINATION_MAX_LIMIT,
)


class APIPagination(LimitOffsetPagination):
    """ Overrides `default_limit` and `max_limit` of LimitOffsetPagination """
    default_limit = PAGINATION_DEFAULT_LIMIT
    max_limit = PAGINATION_MAX_LIMIT
