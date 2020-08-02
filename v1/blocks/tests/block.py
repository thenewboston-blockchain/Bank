import random

import pytest
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK

from ..factories.block import BlockFactory


@pytest.fixture
def blocks():
    yield BlockFactory.create_batch(100)


def test_bank_transaction_filter(anonymous_client, blocks, django_assert_max_num_queries):
    block = random.choice(blocks)

    with django_assert_max_num_queries(2):
        response = anonymous_client.get_json(
            reverse('blocks:block-list'),
            {
                'limit': 0,
                'sender': block.sender,
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(block.id)
