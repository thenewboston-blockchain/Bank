import channels.layers
from asgiref.sync import async_to_sync

from thenewboston_bank.crawl.consumers.crawl_status import CrawlStatusConsumer
from thenewboston_bank.crawl.helpers import get_crawl_info
from .constants import CRAWL_STATUS_NOTIFICATION
from .helpers import standardize_notification


def send_crawl_status_notification():
    """Send crawl status notification to all recipients"""
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        CrawlStatusConsumer.group_name(),
        {
            'type': 'send.crawl.status',
            'message': standardize_notification(
                notification_type=CRAWL_STATUS_NOTIFICATION,
                payload=get_crawl_info()
            )
        }
    )
