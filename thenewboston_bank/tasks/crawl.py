import logging

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from thenewboston.constants.crawl import CRAWL_STATUS_NOT_CRAWLING, CRAWL_STATUS_STOP_REQUESTED
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.cache_tools.cache_keys import CRAWL_LAST_COMPLETED, CRAWL_STATUS
from thenewboston_bank.connection_requests.helpers.connect import is_self_known_to_node, send_connection_request
from thenewboston_bank.connection_requests.serializers.bank_configuration import BankConfigurationSerializer
from thenewboston_bank.connection_requests.serializers.validator_configuration import ValidatorConfigurationSerializer
from thenewboston_bank.notifications.crawl_status import send_crawl_status_notification
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.validators.helpers.validator_configuration import (
    create_bank_from_config_data,
    create_validator_from_config_data
)
from thenewboston_bank.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def create_banks(*, known_nodes, results):
    """
    For each unknown bank, attempt to:

    - fetch config data
    - create new Bank object
    """
    for bank in get_unknown_nodes(known_nodes=known_nodes, results=results):

        try:
            address = format_address(
                ip_address=bank.get('ip_address'),
                port=bank.get('port'),
                protocol=bank.get('protocol')
            )
            config_address = f'{address}/config'
            config_data = fetch(url=config_address, headers={})
            serializer = BankConfigurationSerializer(data=config_data)

            if serializer.is_valid():
                create_bank_from_config_data(config_data=config_data)
                continue

            logger.exception(serializer.errors)
        except Exception as e:
            logger.exception(e)


def crawl_banks(*, primary_validator_address, self_node_identifier):
    """Crawl all banks from primary validator and create any new banks"""
    known_nodes = get_known_nodes(node_class=Bank)
    next_url = f'{primary_validator_address}/banks'

    while next_url:

        if cache.get(CRAWL_STATUS) == CRAWL_STATUS_STOP_REQUESTED:
            break

        try:
            response = fetch(url=next_url, headers={})
            next_url = response.get('next')
            results = response.get('results')
            results = [i for i in results if i['node_identifier'] != self_node_identifier]
            create_banks(known_nodes=known_nodes, results=results)
        except Exception as e:
            logger.exception(e)
            break


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


def crawl_validators(*, primary_validator_address):
    """Crawl all validators from primary validator and create any new validators"""
    known_nodes = get_known_nodes(node_class=Validator)
    next_url = f'{primary_validator_address}/validators'

    while next_url:

        if cache.get(CRAWL_STATUS) == CRAWL_STATUS_STOP_REQUESTED:
            break

        try:
            response = fetch(url=next_url, headers={})
            next_url = response.get('next')
            results = response.get('results')
            create_validators(known_nodes=known_nodes, results=results)
        except Exception as e:
            logger.exception(e)
            break


def get_known_nodes(*, node_class):
    """Return IP address and NID for known validations"""
    nodes = node_class.objects.all().values('ip_address', 'node_identifier')
    return {
        'ip_addresses': {i['ip_address'] for i in nodes},
        'node_identifiers': {i['node_identifier'] for i in nodes},
    }


def get_unknown_nodes(*, known_nodes, results):
    """Filter a results list for unknown nodes"""
    return [
        node for node in results if (
            node['ip_address'] not in known_nodes['ip_addresses']
            and node['node_identifier'] not in known_nodes['node_identifiers']
        )
    ]


def send_connection_requests(*, node_class, self_configuration):
    """Send a connection request to any nodes where self is unknown"""
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
    """Start a network crawl"""
    self_configuration = get_self_configuration(exception_class=RuntimeError)
    self_node_identifier = self_configuration.node_identifier
    primary_validator = self_configuration.primary_validator

    primary_validator_address = format_address(
        ip_address=primary_validator.ip_address,
        port=primary_validator.port,
        protocol=primary_validator.protocol
    )

    crawl_banks(primary_validator_address=primary_validator_address, self_node_identifier=self_node_identifier)
    crawl_validators(primary_validator_address=primary_validator_address)

    send_connection_requests(node_class=Bank, self_configuration=self_configuration)
    send_connection_requests(node_class=Validator, self_configuration=self_configuration)

    cache.set(CRAWL_LAST_COMPLETED, str(timezone.now()), None)
    cache.set(CRAWL_STATUS, CRAWL_STATUS_NOT_CRAWLING, None)

    send_crawl_status_notification()
