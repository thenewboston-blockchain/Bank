import logging

from celery import shared_task
from django.core.cache import cache
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch

from v1.cache_tools.cache_keys import CRAWL_STATUS
from v1.connection_requests.helpers.connect import send_connection_request
from v1.connection_requests.serializers.validator_configuration import ValidatorConfigurationSerializer
from v1.crawl.constants import CRAWL_STATUS_NOT_CRAWLING
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.helpers.validator_configuration import create_validator_from_config_data
from v1.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def connect_to_unknown_validators(*, self_configuration, unknown_validators):
    """
    For each validator in the list:
    - for any unknown validators, attempt to fetch config data and create new Validator object
    - if successful, send validator a connection request (if needed)
    """

    for unknown_validator in unknown_validators:

        try:
            address = format_address(
                ip_address=unknown_validator.get('ip_address'),
                port=unknown_validator.get('port'),
                protocol=unknown_validator.get('protocol')
            )
            config_address = f'{address}/config'
            config_data = fetch(url=config_address, headers={})
            serializer = ValidatorConfigurationSerializer(data=config_data)

            if serializer.is_valid():
                validator = create_validator_from_config_data(config_data=config_data)
            else:
                logger.exception(serializer.errors)
                continue

            if not is_known_to_node(node_address=address, self_configuration=self_configuration):
                send_connection_request(node=validator, self_configuration=self_configuration)

        except Exception as e:
            logger.exception(e)


def crawl_validators(*, primary_validator_address, self_configuration):
    """
    Crawl all validators from primary validator
    """

    known_validators = get_known_validators()
    next_url = f'{primary_validator_address}/validators'

    while next_url:

        try:
            response = fetch(url=next_url, headers={})
            next_url = response.get('next')
            results = response.get('results')
            unknown_validators = get_unknown_validators(
                known_validators=known_validators,
                validator_list=results
            )
            connect_to_unknown_validators(
                self_configuration=self_configuration,
                unknown_validators=unknown_validators
            )
        except Exception as e:
            logger.exception(e)


def get_known_validators():
    """
    Return IP address and NID for known validations
    - used in determining which new validators to connect to
    """

    validators = Validator.objects.all().values('ip_address', 'node_identifier')
    return {
        'ip_addresses': {i['ip_address'] for i in validators},
        'node_identifiers': {i['node_identifier'] for i in validators},
    }


def get_unknown_validators(*, known_validators, validator_list):
    """
    Filter a list of validators for unknown validators
    """

    return [
        validator for validator in validator_list if (
            validator['ip_address'] not in known_validators['ip_addresses'] and
            validator['node_identifier'] not in known_validators['node_identifiers']
        )
    ]


def is_known_to_node(*, node_address, self_configuration):
    """
    Return boolean to indicate if self is connected to primary validator
    """

    url = f'{node_address}/banks/{self_configuration.node_identifier}'

    try:
        fetch(url=url, headers={})
        return True
    except Exception as e:
        logger.exception(e)

    return False


@shared_task
def start_crawl():
    """
    Start a network crawl
    """

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator

    primary_validator_address = format_address(
        ip_address=primary_validator.ip_address,
        port=primary_validator.port,
        protocol=primary_validator.protocol
    )

    crawl_validators(primary_validator_address=primary_validator_address, self_configuration=self_configuration)

    cache.set(CRAWL_STATUS, CRAWL_STATUS_NOT_CRAWLING, None)
