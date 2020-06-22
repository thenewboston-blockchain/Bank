import logging

from celery import shared_task
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.blocks.signatures import generate_signature
from thenewboston.environment.environment_variables import get_environment_variable
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.tools import sort_and_encode
from thenewboston.verify_keys.verify_key import encode_verify_key, get_verify_key

logger = logging.getLogger('thenewboston')


@shared_task
def send_signed_block(*, block, ip_address, port, protocol, url_path):
    """
    Sign block and send to recipient
    """

    network_signing_key = get_environment_variable('NETWORK_SIGNING_KEY')
    signing_key = SigningKey(network_signing_key, encoder=HexEncoder)
    node_identifier = get_verify_key(signing_key=signing_key)
    node_identifier = encode_verify_key(verify_key=node_identifier)
    message = sort_and_encode(block)

    signed_block = {
        'block': block,
        'node_identifier': node_identifier,
        'signature': generate_signature(message=message, signing_key=signing_key)
    }

    node_address = format_address(ip_address=ip_address, port=port, protocol=protocol)
    url = f'{node_address}{url_path}'

    try:
        post(url=url, body=signed_block)
    except Exception as e:
        logger.exception(e)
