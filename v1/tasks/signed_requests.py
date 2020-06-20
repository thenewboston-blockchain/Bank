from celery import shared_task
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.environment.environment_variables import get_environment_variable
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.signed_requests import generate_signed_request


@shared_task
def send_signed_post_request(*, data, ip_address, port, protocol, url_path):
    """
    Sign data and send to recipient
    """

    network_signing_key = get_environment_variable('NETWORK_SIGNING_KEY')
    signing_key = SigningKey(network_signing_key, encoder=HexEncoder)

    signed_request = generate_signed_request(
        data=data,
        nid_signing_key=signing_key
    )

    node_address = format_address(ip_address=ip_address, port=port, protocol=protocol)
    url = f'{node_address}{url_path}'
    post(url=url, body=signed_request)
