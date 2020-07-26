import random

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from v1.utils.functools import rgetattr
from ..factories.bank_transaction import BankTransactionFactory


@pytest.fixture
def bank_transactions():
    yield BankTransactionFactory.create_batch(100)


@pytest.mark.parametrize(
    'filter, attribute',
    [
        ('account_number', 'block.sender'),
        ('account_number', 'recipient'),
        ('block__sender', 'block.sender'),
        ('recipient', 'recipient'),
    ],
)
def test_bank_transaction_filter(anonymous_client, bank_transactions, filter, attribute, django_assert_max_num_queries):
    target_transaction = random.choice(bank_transactions)

    with django_assert_max_num_queries(2):
        response = anonymous_client.get_json(
            reverse('bank_transactions:banktransaction-list'),
            {
                'limit': 0,
                filter: rgetattr(target_transaction, attribute),
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(target_transaction.id)
