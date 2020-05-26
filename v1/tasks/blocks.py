from celery import shared_task
from celery.utils.log import get_task_logger
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.accounts.account_numbers import encode_account_number, get_account_number
from thenewboston.blocks.signatures import generate_signature, verify_signature
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.tools import sort_and_encode

logger = get_task_logger(__name__)


@shared_task
def sign_and_send_block(*, block, ip_address, port, protocol, url_path):
    """
    Sign block and send to recipient
    recipient - any NetworkNode
    """

    # TODO: Signing key
    signing_key = SigningKey('e0ba29c1c493d01a5f665db55a4bd77caa140cf9722d0ed367ce4183230d2e02', encoder=HexEncoder)
    account_number = get_account_number(signing_key=signing_key)
    account_number = encode_account_number(account_number=account_number)

    message = sort_and_encode(block)
    signed_block = {
        'account_number': account_number,
        'signature': generate_signature(message=message, signing_key=signing_key),
        'block': block
    }

    verify_signature(
        account_number=account_number,
        signature=signed_block['signature'],
        message=message
    )

    node_address = format_address(ip_address=ip_address, port=port, protocol=protocol)
    url = f'{node_address}{url_path}'
    results = post(url=url, body=signed_block)
    logger.warning(results)
