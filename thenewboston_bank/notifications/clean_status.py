import channels.layers
from asgiref.sync import async_to_sync

from thenewboston_bank.clean.consumers.clean_status import CleanStatusConsumer
from thenewboston_bank.clean.helpers import get_clean_info
from .constants import CLEAN_STATUS_NOTIFICATION
from .helpers import standardize_notification


def send_clean_status_notification():
    """Send clean status notification to all recipients"""
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        CleanStatusConsumer.group_name(),
        {
            'type': 'send.clean.status',
            'message': standardize_notification(
                notification_type=CLEAN_STATUS_NOTIFICATION,
                payload=get_clean_info()
            )
        }
    )
