import random

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts

from v1.utils.functools import rgetattr


def test_bank_transactions_list(client, bank_transactions, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('banktransaction-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )

    assert_objects_vs_dicts(bank_transactions, response)
    assert response


@pytest.mark.parametrize(
    'field, attribute',
    [
        ('account_number', 'block.sender'),
        ('account_number', 'recipient'),
        ('block__sender', 'block.sender'),
        ('recipient', 'recipient'),
    ],
)
def test_bank_transactions_filter(client, bank_transactions, field, attribute, django_assert_max_num_queries):
    target_transaction = random.choice(bank_transactions)

    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('banktransaction-list'),
            {
                'limit': 0,
                field: rgetattr(target_transaction, attribute),
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(target_transaction.id)
