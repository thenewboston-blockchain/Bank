from rest_framework.pagination import LimitOffsetPagination as DRFLimitOffsetPagination

from config.settings.base import PAGINATION_DEFAULT_LIMIT, PAGINATION_MAX_LIMIT


class LimitOffsetPagination(DRFLimitOffsetPagination):
    default_limit = PAGINATION_DEFAULT_LIMIT
    max_limit = PAGINATION_MAX_LIMIT

    def get_limit(self, request):
        """Disable pagination by 'listening' for a zero value for limit_query_param"""
        if request.query_params.get(self.limit_query_param) != '0':
            return super().get_limit(request)
