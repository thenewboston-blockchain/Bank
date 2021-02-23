import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.self_configurations.helpers.signing_key import get_signing_key


def test_banks_list(client, banks, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('bank-list'),
            {'limit': 0},
            expected=status.HTTP_200_OK,
        )
    assert_objects_vs_dicts(banks, response, key='node_identifier')
    assert response


def test_banks_post(client, bank_fake_data, self_configuration):
    response = client.post_json(
        reverse('bank-list'),
        generate_signed_request(
            data=bank_fake_data,
            nid_signing_key=get_signing_key(),
        ),
        expected=status.HTTP_201_CREATED
    )
    bank_fake_data['trust'] = f'{bank_fake_data["trust"]:.2f}'
    assert response == bank_fake_data


def test_banks_patch(client, bank, bank_fake_data, self_configuration):
    response = client.patch_json(
        reverse(
            'bank-detail',
            args=[bank.node_identifier]
        ),
        generate_signed_request(
            data=bank_fake_data,
            nid_signing_key=get_signing_key(),
        ),
        expected=status.HTTP_200_OK,
    )
    assert response['trust'] == f'{bank_fake_data["trust"]:.2f}'


@pytest.mark.parametrize(
    'trust, response_msg',
    [(55.178, 'Ensure that there are no more than 2 decimal places.'),
     (-1, 'Ensure this value is greater than or equal to 0.'),
     (192, 'Ensure this value is less than or equal to 100.')]
)
def test_create_bank_with_invalid_trust_value(
    client, bank, bank_fake_data, self_configuration, trust, response_msg
):
    bank_fake_data['trust'] = trust
    response = client.post_json(
        reverse('bank-list'),
        generate_signed_request(
            data=bank_fake_data,
            nid_signing_key=get_signing_key(),
        ),
        expected=status.HTTP_400_BAD_REQUEST,
    )

    assert response['trust'] == [response_msg]


@pytest.mark.parametrize(
    'trust, response_msg',
    [(55.178, 'Ensure that there are no more than 2 decimal places.'),
     (-1, 'Ensure this value is greater than or equal to 0.'),
     (192, 'Ensure this value is less than or equal to 100.')]
)
def test_update_bank_with_invalid_trust_value(
    client, bank, self_configuration, trust, response_msg
):
    response = client.patch_json(
        reverse(
            'bank-detail',
            args=[bank.node_identifier]
        ),
        generate_signed_request(
            data={'trust': trust},
            nid_signing_key=get_signing_key(),
        ),
        expected=status.HTTP_400_BAD_REQUEST,
    )

    assert response['trust'] == [response_msg]


def test_banks_detail(client, bank, django_assert_max_num_queries):
    with django_assert_max_num_queries(1):
        response = client.get_json(
            reverse(
                'bank-detail',
                args=[bank.node_identifier],
            ),
            expected=status.HTTP_200_OK,
        )
    assert bank.node_identifier == response['node_identifier']
    assert response


def test_banks_detail_not_found(client, django_assert_max_num_queries):
    with django_assert_max_num_queries(1):
        client.get_json(
            reverse(
                'bank-detail',
                args=['thisisafakebanknodeidentifier'],
            ),
            expected=status.HTTP_404_NOT_FOUND,
        )
