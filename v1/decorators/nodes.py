import logging
from functools import wraps

from nacl.exceptions import BadSignatureError
from rest_framework import status
from rest_framework.response import Response
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.errors import BAD_SIGNATURE, ERROR, UNKNOWN
from thenewboston.utils.tools import sort_and_encode

from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.helpers.validator_configuration import get_primary_validator

logger = logging.getLogger('thenewboston')


def is_primary_validator(func):
    """
    Verify that the client making the request is the primary validator
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        message = request.data.get('message')
        node_identifier = request.data.get('node_identifier')
        signature = request.data.get('signature')

        primary_validator = get_primary_validator()

        if node_identifier != primary_validator.node_identifier:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            verify_signature(
                message=sort_and_encode(message),
                signature=signature,
                verify_key=node_identifier
            )
        except BadSignatureError as e:
            logger.exception(e)
            return Response(
                {ERROR: BAD_SIGNATURE},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.exception(e)
            return Response(
                {ERROR: UNKNOWN},
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
        node_identifier = request.data.get('node_identifier')
        signature = request.data.get('signature')

        self_configuration = get_self_configuration(exception_class=RuntimeError)

        if node_identifier != self_configuration.node_identifier:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            verify_signature(
                message=sort_and_encode(message),
                signature=signature,
                verify_key=node_identifier
            )
        except BadSignatureError as e:
            logger.exception(e)
            return Response(
                {ERROR: BAD_SIGNATURE},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.exception(e)
            return Response(
                {ERROR: UNKNOWN},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return func(request, *args, **kwargs)

    return inner


def is_signed_message(func):
    """
    Decorator to verify the request signature
    """

    @wraps(func)
    def inner(request, *args, **kwargs):
        request, error = verify_request_signature(request=request, signed_data_key='message')

        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)

    return inner


def verify_request_signature(*, request, signed_data_key):
    """
    Verify the request signature
    signed_data - block or message
    """

    node_identifier = request.data.get('node_identifier')
    signature = request.data.get('signature')
    signed_data = request.data.get(signed_data_key)

    for field in ['node_identifier', 'signature', signed_data_key]:
        if not request.data.get(field):
            return request, {ERROR: f'{field} required'}

    error = None

    try:
        verify_signature(
            message=sort_and_encode(signed_data),
            signature=signature,
            verify_key=node_identifier
        )
    except BadSignatureError as e:
        logger.exception(e)
        error = {ERROR: BAD_SIGNATURE}
    except Exception as e:
        logger.exception(e)
        error = {ERROR: UNKNOWN}

    return request, error
