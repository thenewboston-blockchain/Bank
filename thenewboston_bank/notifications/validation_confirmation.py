import channels.layers
from asgiref.sync import async_to_sync

from thenewboston_bank.validator_confirmation_services.consumers.validator_confirmation_service import (
    ValidatorConfirmationServiceConsumer
)
from .constants import VALIDATOR_CONFIRMATION_SERVICE_NOTIFICATION
from .helpers import standardize_notification


def send_validator_confirmation_service_notification(*, payload):
    """Send validation confirmation created notification to all recipients"""
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        ValidatorConfirmationServiceConsumer.group_name(),
        {
            'type': 'send.validator.confirmation.service',
            'message': standardize_notification(
                notification_type=VALIDATOR_CONFIRMATION_SERVICE_NOTIFICATION,
                payload=payload
            )
        }
    )
