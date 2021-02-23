import channels.layers
from asgiref.sync import async_to_sync

from thenewboston_bank.confirmation_blocks.consumers.confirmation_block import ConfirmationBlockConsumer
from .constants import CONFIRMATION_BLOCK_NOTIFICATION
from .helpers import standardize_notification


def send_confirmation_block_notifications(*, payload, sender_account_number, recipient_account_numbers):
    """Send confirmation block notifications to all recipients"""
    channel_layer = channels.layers.get_channel_layer()

    for account_number in (*recipient_account_numbers, sender_account_number):
        async_to_sync(channel_layer.group_send)(
            ConfirmationBlockConsumer.group_name(account_number),
            {
                'type': 'send.confirmation.block',
                'message': standardize_notification(
                    notification_type=CONFIRMATION_BLOCK_NOTIFICATION,
                    payload=payload
                )
            }
        )
