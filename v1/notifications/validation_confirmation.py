from asgiref.sync import async_to_sync
import channels.layers

from .constants import VALIDATOR_CONFIRMATION_SERVICES_NOTIFICATION
from .helpers import standardize_notification
from ..validator_confirmation_services.consumers.validation_confirmation_created import ValidationConfirmationConsumer


def send_validation_confirmation_created_notification(*, payload):
    """
    Send validation confirmation created notification to all recipients
    """

    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        ValidationConfirmationConsumer.group_name(),
        {
            'type': 'send.validation.confirmation.created',
            'message': standardize_notification(
                notification_type=VALIDATOR_CONFIRMATION_SERVICES_NOTIFICATION,
                payload=payload
            )
        }
    )
