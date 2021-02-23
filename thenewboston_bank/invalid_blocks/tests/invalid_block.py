from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts


def test_invalid_block_list(client, invalid_blocks, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('invalidblock-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )

    assert_objects_vs_dicts(invalid_blocks, response)
    assert response


def test_invalid_block_post(client, validator, block_data, block, invalid_block_data):

    response = client.post_json(
        reverse('invalidblock-list'),
        invalid_block_data,
        expected=HTTP_201_CREATED,
    )
    assert invalid_block_data['message']['block_identifier'] == response['block_identifier']


def test_invalid_block_post_400_unique_recipients(
    client, validator, block, invalid_block_data_unique_recipients
):
    response = client.post_json(
        reverse('invalidblock-list'),
        invalid_block_data_unique_recipients,
        expected=HTTP_400_BAD_REQUEST,
    )
    assert response['message']['block']['non_field_errors'] == ['Tx recipients must be unique']
