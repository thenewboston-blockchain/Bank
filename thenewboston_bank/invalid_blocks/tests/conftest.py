import pytest
from thenewboston.third_party.factory.utils import build_json
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.validators.helpers.validator_configuration import get_primary_validator
from ..factories.invalid_block import InvalidBlockFactory


@pytest.fixture
def invalid_block_data(block_data, signing_key, invalid_block_fake_data):
    yield generate_signed_request(
        data={
            'block': block_data,
            'block_identifier': invalid_block_fake_data['block_identifier'],
            'primary_validator_node_identifier': get_primary_validator().node_identifier,
        },
        nid_signing_key=signing_key
    )


@pytest.fixture
def invalid_block_data_unique_recipients(block_data_unique_recipients, signing_key, invalid_block_fake_data):
    yield generate_signed_request(
        data={
            'block': block_data_unique_recipients,
            'block_identifier': invalid_block_fake_data['block_identifier'],
            'primary_validator_node_identifier': get_primary_validator().node_identifier,
        },
        nid_signing_key=signing_key
    )


@pytest.fixture
def invalid_block_fake_data():
    yield build_json(InvalidBlockFactory)


@pytest.fixture
def invalid_blocks():
    yield InvalidBlockFactory.create_batch(100)
