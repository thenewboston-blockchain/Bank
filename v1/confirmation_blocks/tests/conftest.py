import pytest
from thenewboston.third_party.factory.utils import build_json
from thenewboston.utils.signed_requests import generate_signed_request

from ..factories.confirmation_block import ConfirmationBlockFactory


@pytest.fixture
def confirmation_block_data(block_data, signing_key, confirmation_block_fake_data):
    yield generate_signed_request(
        data={
            'block': block_data,
            'block_identifier': confirmation_block_fake_data['block_identifier'],
            'updated_balances': [],
        },
        nid_signing_key=signing_key
    )


@pytest.fixture
def confirmation_block_data_unique_recipients(
    block_data_unique_recipients,
    signing_key,
    confirmation_block_fake_data,
):
    yield generate_signed_request(
        data={
            'block': block_data_unique_recipients,
            'block_identifier': confirmation_block_fake_data['block_identifier'],
            'updated_balances': [],
        },
        nid_signing_key=signing_key
    )


@pytest.fixture
def confirmation_block_fake_data():
    yield build_json(ConfirmationBlockFactory)


@pytest.fixture
def confirmation_blocks():
    yield ConfirmationBlockFactory.create_batch(100)
