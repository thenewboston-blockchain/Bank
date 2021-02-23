import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from thenewboston_bank.notifications.constants import PRIMARY_VALIDATOR_UPDATED_NOTIFICATION
from thenewboston_bank.notifications.status_updates import send_primary_validator_updated_notification
from ..consumers.primary_validator_updated import PrimaryValidatorUpdatedConsumer


@pytest.mark.asyncio
async def test_primary_validator_updated_async(client, self_configuration):
    communicator = WebsocketCommunicator(
        PrimaryValidatorUpdatedConsumer,
        'ws/primary_validator_updated'
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    await sync_to_async(
        send_primary_validator_updated_notification
    )()
    response = await communicator.receive_json_from(timeout=3)
    await communicator.disconnect()

    assert response['notification_type'] == PRIMARY_VALIDATOR_UPDATED_NOTIFICATION
    assert response['payload']
