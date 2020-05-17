from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from v1.validators.helpers.validator_configuration import get_primary_validator


def signed_by_primary_validator(func):
    """
    Verify that the request body has been signed by the primary validator
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        primary_validator = get_primary_validator()

        signed_request = request.data
        signed_data = signed_request.get('signed_data')
        signed_identifier = signed_request.get('verifying_key_hex')

        if not signed_data:
            return Response(
                {
                    'error_message': 'Request must include signed_data'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # TODO: Actual block verification
        if signed_identifier != primary_validator.identifier:
            return Response(
                {
                    'error_message': 'Invalid identifier',
                    'expected_identifier': primary_validator.identifier,
                    'received_identifier': signed_request.get('verifying_key_hex')
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return func(request, *args, **kwargs)

    return inner
