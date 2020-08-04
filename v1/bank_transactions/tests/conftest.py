import pytest

from ..factories.bank_transaction import BankTransactionFactory


@pytest.fixture
def bank_transactions():
    yield BankTransactionFactory.create_batch(100)
