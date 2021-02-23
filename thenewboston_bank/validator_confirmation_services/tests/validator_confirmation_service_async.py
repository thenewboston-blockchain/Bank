from datetime import datetime, timedelta

import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.notifications.constants import VALIDATOR_CONFIRMATION_SERVICE_NOTIFICATION
from ..consumers.validator_confirmation_service import ValidatorConfirmationServiceConsumer


@pytest.mark.asyncio
async def test_validator_confirmation_service_post_async(
    client, validator, signing_key
):
    communicator = WebsocketCommunicator(
        ValidatorConfirmationServiceConsumer,
        'ws/validator_confirmation_services'
    )
    connected, subprotocol = await communicator.connect()
    assert connected

    start = datetime.now().isoformat()
    end = (datetime.now() + timedelta(days=2)).isoformat()

    payload = generate_signed_request(
        data={
            'start': start,
            'end': end
        },
        nid_signing_key=signing_key
    )

    response = await sync_to_async(
        client.post_json
    )(
        reverse('validatorconfirmationservice-list'),
        payload,
        expected=HTTP_201_CREATED
    )
    communicator_response = await communicator.receive_json_from()

    assert response['end'][:-1] == end
    assert response['start'][:-1] == start
    assert response['validator'] == str(validator.pk)

    assert communicator_response == {
        'notification_type': VALIDATOR_CONFIRMATION_SERVICE_NOTIFICATION,
        'payload': {
            'bank_node_identifier': validator.node_identifier,
            'validator_confirmation_service': response
        }
    }

    await communicator.disconnect()
