import pytest
from factory import Faker
from thenewboston.blocks.block import generate_block

from ..factories.block import BlockFactory


@pytest.fixture
def block_data_unique_recipients(
    account_data, account, encoded_account_number, random_encoded_account_number, self_configuration
):
    signing_key, account_number = account_data
    primary_validator = self_configuration.primary_validator

    yield generate_block(
        account_number=account_number,
        balance_lock=encoded_account_number,
        signing_key=signing_key,
        transactions=[
            {
                'amount': self_configuration.default_transaction_fee,
                'recipient': self_configuration.account_number
            },
            {
                'amount': primary_validator.default_transaction_fee,
                'recipient': primary_validator.account_number
            },
            {
                'amount': Faker('pyint').generate(),
                'recipient': self_configuration.account_number
            }
        ]
    )


@pytest.fixture
def blocks():
    yield BlockFactory.create_batch(100)
