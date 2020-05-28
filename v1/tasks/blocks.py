from celery import shared_task
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.blocks.signatures import generate_signature
from thenewboston.environment.environment_variables import get_environment_variable
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.tools import sort_and_encode
from thenewboston.verify_keys.verify_key import encode_verify_key, get_verify_key


@shared_task
def sign_and_send_block(*, block, ip_address, port, protocol, url_path):
    """
    Sign block and send to recipient
    """

    network_signing_key = get_environment_variable('NETWORK_SIGNING_KEY')
    signing_key = SigningKey(network_signing_key, encoder=HexEncoder)
    network_identifier = get_verify_key(signing_key=signing_key)
    network_identifier = encode_verify_key(verify_key=network_identifier)
    message = sort_and_encode(block)

    signed_block = {
        'block': block,
        'network_identifier': network_identifier,
        'signature': generate_signature(message=message, signing_key=signing_key)
    }

    node_address = format_address(ip_address=ip_address, port=port, protocol=protocol)
    url = f'{node_address}{url_path}'
    post(url=url, body=signed_block)
