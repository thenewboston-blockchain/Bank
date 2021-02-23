import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.constants.crawl import CRAWL_COMMAND_START, CRAWL_STATUS_NOT_CRAWLING
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.notifications.constants import CRAWL_STATUS_NOTIFICATION
from thenewboston_bank.self_configurations.helpers.signing_key import get_signing_key
from ..consumers.crawl_status import CrawlStatusConsumer


@pytest.mark.asyncio
async def test_crawl_status_async(client, self_configuration, celery_worker):

    communicator = WebsocketCommunicator(
        CrawlStatusConsumer,
        'ws/crawl_status'
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    await sync_to_async(
        client.post_json
    )(
        reverse('crawl-list'),
        generate_signed_request(
            data={
                'crawl': CRAWL_COMMAND_START
            },
            nid_signing_key=get_signing_key()
        ),
        expected=HTTP_200_OK
    )
    async_response = await communicator.receive_json_from(timeout=3)
    await communicator.disconnect()
    crawl_status = async_response['payload']

    assert async_response['notification_type'] == CRAWL_STATUS_NOTIFICATION
    assert crawl_status['crawl_last_completed']
    assert crawl_status['crawl_status'] == CRAWL_STATUS_NOT_CRAWLING
