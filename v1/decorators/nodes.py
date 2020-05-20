from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from v1.validators.helpers.validator_configuration import get_primary_validator


def is_primary_validator(func):
    """
    Verify that the client making the request is the primary validator
    """

    @wraps(func)
    def inner(request, *args, **kwargs):

        if not request.user.is_authenticated:
            ip_address = request.META.get('REMOTE_ADDR')

            if not ip_address:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            # TODO: This should be hitting the cache
            primary_validator = get_primary_validator()

            if ip_address != primary_validator.ip_address:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)

    return inner
