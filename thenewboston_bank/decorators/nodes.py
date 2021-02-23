import logging
from functools import wraps

from nacl.exceptions import BadSignatureError
from rest_framework import status
from rest_framework.response import Response
from thenewboston.blocks.signatures import verify_signature
from thenewboston.constants.errors import BAD_SIGNATURE, ERROR, UNKNOWN
from thenewboston.utils.tools import sort_and_encode

from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration

logger = logging.getLogger('thenewboston')


def is_self_signed_message(func):
    """Verify that the client making the request is self"""
    @wraps(func)
    def inner(obj, request, *args, **kwargs):
        request, error = verify_request_signature(request=request, signed_data_key='message')

        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        node_identifier = request.data['node_identifier']
        self_configuration = get_self_configuration(exception_class=RuntimeError)

        if node_identifier != self_configuration.node_identifier:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return func(obj, request, *args, **kwargs)

    return inner


def is_signed_message(func):
    """Verify that the request has been signed"""
    @wraps(func)
    def inner(obj, request, *args, **kwargs):
        request, error = verify_request_signature(request=request, signed_data_key='message')

        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        return func(obj, request, *args, **kwargs)

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
