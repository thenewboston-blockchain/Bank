from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts
from thenewboston.utils.signed_requests import generate_signed_request

from v1.self_configurations.helpers.signing_key import get_signing_key


def test_banks_list(client, banks, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('bank-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )
    assert_objects_vs_dicts(banks, response, key='node_identifier')
    assert response


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
        expected=HTTP_200_OK,
    )
    assert float(response['trust']) == bank_fake_data['trust']
