import pytest
from thenewboston.third_party.factory.utils import build_json

from ..factories.bank import BankFactory


@pytest.fixture
def bank(encoded_account_number):
    yield BankFactory(node_identifier=encoded_account_number)


@pytest.fixture
def bank_fake_data():
    yield build_json(BankFactory)


@pytest.fixture
def banks():
    yield BankFactory.create_batch(100)
