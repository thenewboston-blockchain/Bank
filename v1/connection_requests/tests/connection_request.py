import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST
from thenewboston.third_party.factory.utils import build_json
from thenewboston.utils.signed_requests import generate_signed_request

from ..factories.connection_request import ConnectionRequestFactory


@pytest.fixture
def connection_request_data():
    yield build_json(
        ConnectionRequestFactory
    )


def test_banks_post_400_connect_to_self(client, connection_request_data, signing_key, self_configuration):

    connection_request_data['ip_address'] = self_configuration.ip_address
    connection_request_data['protocol'] = self_configuration.protocol

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response.get('non_field_errors')[0] == 'Unable to connect to self'
