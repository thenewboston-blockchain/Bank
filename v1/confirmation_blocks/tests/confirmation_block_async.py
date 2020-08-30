import json

import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED

from ..consumers.confirmation_block import ConfirmationBlockConsumer


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_confirmation_block_async(client, validator, block, confirmation_block_data):
    inner_block = confirmation_block_data['message']['block']
    sender_account_number = inner_block['account_number']
    recipient_account_number = inner_block['message']['txs'][0]['recipient']

    communicators = []

    for account_number in (recipient_account_number, sender_account_number):
        communicators.append(
            WebsocketCommunicator(
                ConfirmationBlockConsumer,
                'ws/confirmation_blocks/%s' % account_number
            )
        )

    for communicator in communicators:
        connected, subprotocol = await communicator.connect()
        assert connected

    response = await sync_to_async(
        client.post_json
    )(
        reverse('confirmationblock-list'),
        confirmation_block_data,
        expected=HTTP_201_CREATED,
    )

    sender_response = json.loads(await communicators[0].receive_from())
    assert sender_response['message']['block_identifier'] == response['block_identifier']

    recipient_response = json.loads(await communicators[1].receive_from())
    assert recipient_response['message']['block']['message']['txs'][0]['recipient'] == recipient_account_number

    for communicator in communicators:
        await communicator.disconnect()
