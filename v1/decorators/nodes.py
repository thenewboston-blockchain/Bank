from functools import wraps

from nacl.exceptions import BadSignatureError
from rest_framework import status
from rest_framework.response import Response
from thenewboston.blocks.signatures import verify_signature
from thenewboston.utils.tools import sort_and_encode

from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.helpers.validator_configuration import get_primary_validator


def is_primary_validator(func):
    """
    Verify that the client making the request is the primary validator
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        message = request.data.get('message')
        network_identifier = request.data.get('network_identifier')
        signature = request.data.get('signature')

        # TODO: This should be hitting the cache
        primary_validator = get_primary_validator()

        if network_identifier != primary_validator.network_identifier:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            verify_signature(
                message=sort_and_encode(message),
                signature=signature,
                verify_key=network_identifier
            )
        except BadSignatureError:
            # TODO: Standardize error messages
            return Response(
                {'Error': 'Bad signature'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            # TODO: Standardize error messages
            print(e)
            return Response(
                {'Error': 'Unknown error'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return func(request, *args, **kwargs)

    return inner


def is_self(func):
    """
    Verify that the client making the request is self
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        message = request.data.get('message')
        network_identifier = request.data.get('network_identifier')
        signature = request.data.get('signature')

        self_configuration = get_self_configuration(exception_class=RuntimeError)

        if network_identifier != self_configuration.network_identifier:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            verify_signature(
                message=sort_and_encode(message),
                signature=signature,
                verify_key=network_identifier
            )
        except BadSignatureError:
            # TODO: Standardize error messages
            return Response(
                {'Error': 'Bad signature'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            # TODO: Standardize error messages
            print(e)
            return Response(
                {'Error': 'Unknown error'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return func(request, *args, **kwargs)

    return inner
