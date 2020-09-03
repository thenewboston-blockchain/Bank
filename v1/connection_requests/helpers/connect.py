import logging

from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch, post
from thenewboston.utils.signed_requests import generate_signed_request

from v1.banks.models.bank import Bank
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.self_configurations.helpers.signing_key import get_signing_key
from v1.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def get_node_url_resource_name(*, node):
    """
    Return the default related name for the given node
    - used in URL formatting
    """

    if isinstance(node, Bank):
        return 'banks'

    if isinstance(node, Validator):
        return 'validators'


def is_node_connected(*, node, self_configuration):
    """
    Return boolean to indicate if node is connected to self
    """

    node_address = format_address(
        ip_address=node.ip_address,
        port=node.port,
        protocol=node.protocol,
    )

    url_resource_name = get_node_url_resource_name(node=node)
    url = f'{node_address}/{url_resource_name}/{self_configuration.node_identifier}'

    try:
        fetch(url=url, headers={})
        return True
    except Exception as e:
        logger.exception(e)

    return False


def send_connection_request(*, node, self_configuration):
    """
    Send connection request to node
    """

    node_address = format_address(
        ip_address=node.ip_address,
        port=node.port,
        protocol=node.protocol,
    )

    signed_request = generate_signed_request(
        data={
            'ip_address': self_configuration.ip_address,
            'port': self_configuration.port,
            'protocol': self_configuration.protocol
        },
        nid_signing_key=get_signing_key()
    )
    url = f'{node_address}/connection_requests'

    try:
        post(url=url, body=signed_request)
    except Exception as e:
        logger.exception(e)
        raise e


def set_primary_validator(*, validator):
    """
    Set validator as primary validator
    """

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    self_configuration.primary_validator = validator
    self_configuration.save()

    if is_node_connected(
        node=validator,
        self_configuration=self_configuration
    ):
        return

    send_connection_request(node=validator, self_configuration=self_configuration)
