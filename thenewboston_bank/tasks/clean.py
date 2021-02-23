import logging

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from sentry_sdk import capture_exception
from thenewboston.constants.clean import CLEAN_STATUS_NOT_CLEANING, CLEAN_STATUS_STOP_REQUESTED
from thenewboston.constants.network import BANK, CONFIRMATION_VALIDATOR
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.cache_tools.cache_keys import CLEAN_LAST_COMPLETED, CLEAN_STATUS
from thenewboston_bank.connection_requests.serializers.bank_configuration import BankConfigurationSerializer
from thenewboston_bank.connection_requests.serializers.validator_configuration import ValidatorConfigurationSerializer
from thenewboston_bank.notifications.clean_status import send_clean_status_notification
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.validators.helpers.validator_configuration import (
    update_bank_from_config_data,
    update_validator_from_config_data
)
from thenewboston_bank.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def clean_nodes(*, nodes_type):  # noqa: C901
    """Clean nodes: delete or update nodes of type BANK or CONFIRMATION_VALIDATOR"""
    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator

    excluded_node_identifiers = [self_configuration.node_identifier, primary_validator.node_identifier]

    if nodes_type == BANK:
        model = Bank
    elif nodes_type == CONFIRMATION_VALIDATOR:
        model = Validator
    else:
        raise RuntimeError(f'Invalid nodes_type of {nodes_type}')

    nodes = model.objects.all().exclude(node_identifier__in=excluded_node_identifiers)
    nodes_to_delete = []

    for node in nodes:

        if cache.get(CLEAN_STATUS) == CLEAN_STATUS_STOP_REQUESTED:
            break

        try:
            address = format_address(
                ip_address=node.ip_address,
                port=node.port,
                protocol=node.protocol
            )
            config_address = f'{address}/config'
            config_data = fetch(url=config_address, headers={})
        except Exception as e:
            capture_exception(e)
            logger.exception(e)
            nodes_to_delete.append(node.id)
            continue

        for field in ['ip_address', 'port', 'protocol', 'node_identifier']:

            if config_data.get(field) != getattr(node, field):
                nodes_to_delete.append(node.id)
                continue

        if nodes_type == BANK:
            serializer = BankConfigurationSerializer(data=config_data)

            if serializer.is_valid():
                update_bank_from_config_data(bank=node, config_data=config_data)
            else:
                logger.exception(serializer.errors)
                nodes_to_delete.append(node.id)
                continue

        if nodes_type == CONFIRMATION_VALIDATOR:
            serializer = ValidatorConfigurationSerializer(data=config_data)

            if serializer.is_valid():
                update_validator_from_config_data(validator=node, config_data=config_data)
            else:
                logger.exception(serializer.errors)
                nodes_to_delete.append(node.id)
                continue

    nodes.filter(id__in=nodes_to_delete).delete()


@shared_task
def start_clean():
    """Start a network clean"""
    clean_nodes(nodes_type=BANK)
    clean_nodes(nodes_type=CONFIRMATION_VALIDATOR)

    cache.set(CLEAN_LAST_COMPLETED, str(timezone.now()), None)
    cache.set(CLEAN_STATUS, CLEAN_STATUS_NOT_CLEANING, None)

    send_clean_status_notification()
