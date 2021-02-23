import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.constants.clean import CLEAN_COMMAND_START, CLEAN_STATUS_NOT_CLEANING
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.notifications.constants import CLEAN_STATUS_NOTIFICATION
from thenewboston_bank.self_configurations.helpers.signing_key import get_signing_key
from ..consumers.clean_status import CleanStatusConsumer


@pytest.mark.asyncio
async def test_clean_status_async(client, no_requests, celery_worker):
    communicator = WebsocketCommunicator(
        CleanStatusConsumer,
        'ws/clean_status'
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    await sync_to_async(
        client.post_json
    )(
        reverse('clean-list'),
        generate_signed_request(
            data={
                'clean': CLEAN_COMMAND_START
            },
            nid_signing_key=get_signing_key()
        ),
        expected=HTTP_200_OK
    )
    async_response = await communicator.receive_json_from(timeout=3)
    await communicator.disconnect()
    clean_status = async_response['payload']

    assert async_response['notification_type'] == CLEAN_STATUS_NOTIFICATION
    assert clean_status['clean_last_completed']
    assert clean_status['clean_status'] == CLEAN_STATUS_NOT_CLEANING
