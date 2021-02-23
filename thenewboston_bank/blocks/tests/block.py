import random

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts


def test_blocks_list(client, blocks, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('block-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )

    assert_objects_vs_dicts(blocks, response)
    assert response


def test_blocks_list_filter(client, blocks, django_assert_max_num_queries):
    block = random.choice(blocks)

    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('block-list'),
            {
                'limit': 0,
                'sender': block.sender,
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(block.id)


def test_blocks_post(client, block_data):
    response = client.post_json(
        reverse('block-list'),
        block_data,
        expected=HTTP_201_CREATED,
    )
    assert block_data['signature'] == response['signature']
    assert block_data['message']['balance_key'] == response['balance_key']


def test_blocks_post_400_unique_recipients(client, block_data_unique_recipients):
    response = client.post_json(
        reverse('block-list'),
        block_data_unique_recipients,
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response['non_field_errors'] == ['Tx recipients must be unique']
