import channels.layers
from asgiref.sync import async_to_sync

from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.status_updates.consumers.primary_validator_updated import PrimaryValidatorUpdatedConsumer
from v1.validators.serializers.validator import ValidatorSerializer
from .constants import PRIMARY_VALIDATOR_UPDATED_NOTIFICATION
from .helpers import standardize_notification


def send_primary_validator_updated_notification():
    """
    Send primary validator updated notification to all recipients
    """

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator
    primary_validator_data = ValidatorSerializer(primary_validator).data

    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        PrimaryValidatorUpdatedConsumer.group_name(),
        {
            'type': 'send.primary.validator.updated',
            'message': standardize_notification(
                notification_type=PRIMARY_VALIDATOR_UPDATED_NOTIFICATION,
                payload=primary_validator_data
            )
        }
    )
