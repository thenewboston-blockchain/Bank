from celery import shared_task
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.blocks.signatures import generate_signature
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.tools import sort_and_encode
from thenewboston.verify_keys.verify_key import encode_verify_key, get_verify_key


@shared_task
def sign_and_send_block(*, block, ip_address, port, protocol, url_path):
    """
    Sign block and send to recipient
    recipient - any NetworkNode
    """

    # TODO: Signing key
    signing_key = SigningKey('e0ba29c1c493d01a5f665db55a4bd77caa140cf9722d0ed367ce4183230d2e02', encoder=HexEncoder)
    confirmation_identifier = get_verify_key(signing_key=signing_key)
    confirmation_identifier = encode_verify_key(verify_key=confirmation_identifier)
    message = sort_and_encode(block)

    signed_block = {
        'block': block,
        'confirmation_identifier': confirmation_identifier,
        'signature': generate_signature(message=message, signing_key=signing_key)
    }

    node_address = format_address(ip_address=ip_address, port=port, protocol=protocol)
    url = f'{node_address}{url_path}'
    post(url=url, body=signed_block)
