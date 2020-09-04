import logging

from celery import shared_task
from django.core.cache import cache
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch

from v1.cache_tools.cache_keys import CRAWL_STATUS
from v1.connection_requests.helpers.connect import is_self_known_to_node, send_connection_request
from v1.connection_requests.serializers.validator_configuration import ValidatorConfigurationSerializer
from v1.crawl.constants import CRAWL_STATUS_NOT_CRAWLING, CRAWL_STATUS_STOP_REQUESTED
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.helpers.validator_configuration import create_validator_from_config_data
from v1.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def create_validators(*, known_nodes, results):
    """
    For each unknown validator, attempt to:
    - fetch config data
    - create new Validator object
    """

    for validator in get_unknown_nodes(known_nodes=known_nodes, results=results):

        try:
            address = format_address(
                ip_address=validator.get('ip_address'),
                port=validator.get('port'),
                protocol=validator.get('protocol')
            )
            config_address = f'{address}/config'
            config_data = fetch(url=config_address, headers={})
            serializer = ValidatorConfigurationSerializer(data=config_data)

            if serializer.is_valid():
                create_validator_from_config_data(config_data=config_data)
                continue

            logger.exception(serializer.errors)
        except Exception as e:
            logger.exception(e)


def crawl_validators(*, primary_validator):
    """
    Crawl all validators from primary validator and create any new validators
    """

    known_validators = get_known_nodes(node_class=Validator)

    primary_validator_address = format_address(
        ip_address=primary_validator.ip_address,
        port=primary_validator.port,
        protocol=primary_validator.protocol
    )
    next_url = f'{primary_validator_address}/validators'

    while next_url:

        if cache.get(CRAWL_STATUS) == CRAWL_STATUS_STOP_REQUESTED:
            break

        try:
            response = fetch(url=next_url, headers={})
            next_url = response.get('next')
            results = response.get('results')
            create_validators(known_nodes=known_validators, results=results)
        except Exception as e:
            logger.exception(e)


def get_known_nodes(*, node_class):
    """
    Return IP address and NID for known validations
    """

    nodes = node_class.objects.all().values('ip_address', 'node_identifier')
    return {
        'ip_addresses': {i['ip_address'] for i in nodes},
        'node_identifiers': {i['node_identifier'] for i in nodes},
    }


def get_unknown_nodes(*, known_nodes, results):
    """
    Filter a results list for unknown nodes
    """

    return [
        node for node in results if (
            node['ip_address'] not in known_nodes['ip_addresses'] and
            node['node_identifier'] not in known_nodes['node_identifiers']
        )
    ]


def send_connection_requests(*, node_class, self_configuration):
    """
    Send a connection request to any nodes where self is unknown
    """

    for node in node_class.objects.all():

        if cache.get(CRAWL_STATUS) == CRAWL_STATUS_STOP_REQUESTED:
            break

        try:
            if not is_self_known_to_node(node=node, self_configuration=self_configuration):
                send_connection_request(node=node, self_configuration=self_configuration)
        except Exception as e:
            logger.exception(e)


@shared_task
def start_crawl():
    """
    Start a network crawl
    """

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator

    crawl_validators(primary_validator=primary_validator)
    send_connection_requests(node_class=Validator, self_configuration=self_configuration)

    # TODO: Set crawl_last_completed date in cache
    # TODO: Send back notification with that information as well
    cache.set(CRAWL_STATUS, CRAWL_STATUS_NOT_CRAWLING, None)
