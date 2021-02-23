import logging

from celery import shared_task
from thenewboston.constants.network import PRIMARY_VALIDATOR
from thenewboston.utils.format import format_address
from thenewboston.utils.network import post
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.notifications.status_updates import send_primary_validator_updated_notification
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.self_configurations.helpers.signing_key import get_signing_key
from thenewboston_bank.validators.models.validator import Validator

logger = logging.getLogger('thenewboston')


def get_primary_validator_candidates(*, current_primary_validator):
    """Return queryset of validators more trusted than the current primary validator"""
    return Validator.objects.filter(
        trust__gt=current_primary_validator.trust
    ).exclude(
        node_identifier=current_primary_validator.node_identifier
    ).order_by('-trust')


@shared_task
def send_primary_validator_updated_notices():
    """
    Send a notice to all validators that the banks primary validator has been updated

    - 200 response > validator is syncing to new primary validator
    - 400 response > validator is not syncing to new primary validator (can be deleted)
    """
    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator
    confirmation_validators = Validator.objects.all().exclude(node_identifier=primary_validator.node_identifier)

    data = {
        'ip_address': primary_validator.ip_address,
        'port': primary_validator.port,
        'protocol': primary_validator.protocol
    }

    for confirmation_validator in confirmation_validators:
        signed_request = generate_signed_request(
            data=data,
            nid_signing_key=get_signing_key()
        )
        node_address = format_address(
            ip_address=confirmation_validator.ip_address,
            port=confirmation_validator.port,
            protocol=confirmation_validator.protocol,
        )
        url = f'{node_address}/primary_validator_updated'

        try:
            post(url=url, body=signed_request)
        except Exception as e:
            confirmation_validator.delete()
            logger.exception(e)


@shared_task
def set_primary_validator():
    """
    Set the primary validator to the validator that is the:

    - most trusted
    - online
    - configured as a primary validator
    """
    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator
    primary_validator_candidates = get_primary_validator_candidates(current_primary_validator=primary_validator)

    for validator in primary_validator_candidates:
        signed_request = generate_signed_request(
            data={
                'validator_node_identifier': validator.node_identifier
            },
            nid_signing_key=get_signing_key()
        )
        node_address = format_address(
            ip_address=validator.ip_address,
            port=validator.port,
            protocol=validator.protocol,
        )
        url = f'{node_address}/upgrade_request'

        try:
            validator_config = post(url=url, body=signed_request)

            if validator_config['node_type'] != PRIMARY_VALIDATOR:
                continue

            self_configuration.primary_validator = validator
            self_configuration.save()

            send_primary_validator_updated_notices.delay()
            send_primary_validator_updated_notification()
            return
        except Exception as e:
            logger.exception(e)
