from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from v1.third_party.pytest.asserts import assert_objects_vs_dicts


def test_confirmation_block_list(client, confirmation_blocks, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('confirmationblock-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )

    assert_objects_vs_dicts(confirmation_blocks, response)
    assert response


def test_confirmation_block_post(client, validator, block, confirmation_block_data):

    response = client.post_json(
        reverse('confirmationblock-list'),
        confirmation_block_data,
        expected=HTTP_201_CREATED,
    )
    assert confirmation_block_data['message']['block_identifier'] == response['block_identifier']
