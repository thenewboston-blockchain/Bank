import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_400_BAD_REQUEST
from thenewboston.constants.network import BANK, PRIMARY_VALIDATOR
from thenewboston.third_party.factory.utils import build_json
from thenewboston.utils.format import format_address
from thenewboston.utils.signed_requests import generate_signed_request

from ..factories.connection_request import BankConnectionRequestFactory, ValidatorConnectionRequestFactory
from ..serializers.primary_validator_configuration import PrimaryValidatorConfigurationSerializer
from ...banks.factories.bank import BankFactory
from ...banks.models.bank import Bank
from ...validators.factories.validator import ValidatorFactory
from ...validators.models.validator import Validator


@pytest.fixture
def bank_connection_request_data():
    yield build_json(
        BankConnectionRequestFactory
    )


@pytest.fixture
def validator_connection_request_data():
    yield build_json(
        ValidatorConnectionRequestFactory
    )


def test_banks_post_400_connect_to_self(client, bank_connection_request_data, signing_key, self_configuration):
    bank_connection_request_data['ip_address'] = self_configuration.ip_address
    bank_connection_request_data['protocol'] = self_configuration.protocol
    bank_connection_request_data['port'] = self_configuration.port

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=bank_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response == {'non_field_errors': ['Unable to connect to self']}


def test_banks_post_400_connect_to_existing_bank(client, bank_connection_request_data, signing_key, self_configuration):
    bank = BankFactory()

    bank_connection_request_data['ip_address'] = bank.ip_address
    bank_connection_request_data['protocol'] = bank.protocol
    bank_connection_request_data['port'] = bank.port

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=bank_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response == {'non_field_errors': ['Already connected to bank']}


def test_banks_post_400_connect_to_existing_validator(
    client, validator_connection_request_data, signing_key, self_configuration
):
    validator = ValidatorFactory()

    validator_connection_request_data['ip_address'] = validator.ip_address
    validator_connection_request_data['protocol'] = validator.protocol
    validator_connection_request_data['port'] = validator.port

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=validator_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response == {'non_field_errors': ['Already connected to validator']}


def test_banks_post_400_node_id_bank_exists(client, bank_connection_request_data, signing_key, self_configuration):
    payload = generate_signed_request(
        data=bank_connection_request_data,
        nid_signing_key=signing_key
    )
    BankFactory(node_identifier=payload['node_identifier'])

    response = client.post_json(
        reverse('connection_requests-list'),
        payload,
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response == {'node_identifier': ['Bank with that node identifier already exists']}


def test_banks_post_400_node_id_validator_exists(
    client, validator_connection_request_data, signing_key, self_configuration
):
    payload = generate_signed_request(
        data=validator_connection_request_data,
        nid_signing_key=signing_key
    )
    ValidatorFactory(node_identifier=payload['node_identifier'])

    response = client.post_json(
        reverse('connection_requests-list'),
        payload,
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response == {'node_identifier': ['Validator with that node identifier already exists']}


def test_banks_post_400_primary_validator(
    client, validator_connection_request_data, signing_key, self_configuration, requests_mock
):
    validator_connection_request_data['node_type'] = PRIMARY_VALIDATOR
    address = format_address(
        ip_address=validator_connection_request_data['ip_address'],
        port=validator_connection_request_data.get('port'),
        protocol=validator_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=validator_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=validator_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_400_BAD_REQUEST
    )

    assert response == {'non_field_errors': ['Unable to accept connection requests from primary validators']}


def test_banks_post_400_invalid_node_type(
    client, bank_connection_request_data, signing_key, self_configuration, requests_mock
):
    bank_connection_request_data['node_type'] = 'BLAH_BLAH'
    address = format_address(
        ip_address=bank_connection_request_data['ip_address'],
        port=bank_connection_request_data.get('port'),
        protocol=bank_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=bank_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=bank_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_400_BAD_REQUEST
    )

    assert response == {'non_field_errors': ['Invalid node_type']}


def test_banks_post_400_remote_response_bank_no_primary_validator(
    client, bank_connection_request_data, signing_key, self_configuration, requests_mock
):
    bank_connection_request_data['node_type'] = BANK
    address = format_address(
        ip_address=bank_connection_request_data['ip_address'],
        port=bank_connection_request_data.get('port'),
        protocol=bank_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=bank_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=bank_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_400_BAD_REQUEST
    )

    assert response == {'primary_validator': ['This field is required.']}


def test_banks_post_400_remote_response_confirmation_validator_no_primary_validator(
    client, validator_connection_request_data, signing_key, self_configuration, requests_mock
):
    address = format_address(
        ip_address=validator_connection_request_data['ip_address'],
        port=validator_connection_request_data.get('port'),
        protocol=validator_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=validator_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=validator_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_400_BAD_REQUEST
    )

    assert response == {'primary_validator': ['This field is required.']}


def test_banks_post_201_bank(
    client, bank_connection_request_data, signing_key, self_configuration, requests_mock
):
    primary_validator = PrimaryValidatorConfigurationSerializer(self_configuration.primary_validator)

    bank_connection_request_data['primary_validator'] = primary_validator.data
    address = format_address(
        ip_address=bank_connection_request_data['ip_address'],
        port=bank_connection_request_data.get('port'),
        protocol=bank_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=bank_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=bank_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_201_CREATED
    )

    assert response == {}
    assert Bank.objects.get(ip_address=bank_connection_request_data['ip_address'])


def test_banks_post_201_confirmation_validator(
    client, validator_connection_request_data, signing_key, self_configuration, requests_mock
):
    primary_validator = PrimaryValidatorConfigurationSerializer(self_configuration.primary_validator)

    validator_connection_request_data['primary_validator'] = primary_validator.data
    address = format_address(
        ip_address=validator_connection_request_data['ip_address'],
        port=validator_connection_request_data.get('port'),
        protocol=validator_connection_request_data['protocol']
    )
    requests_mock.get(f'{address}/config', json=validator_connection_request_data)

    response = client.post_json(
        reverse('connection_requests-list'),
        generate_signed_request(
            data=validator_connection_request_data,
            nid_signing_key=signing_key,
        ),
        expected=status.HTTP_201_CREATED
    )

    assert response == {}
    assert Validator.objects.get(ip_address=validator_connection_request_data['ip_address'])
