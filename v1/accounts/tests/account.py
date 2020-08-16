from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts
from thenewboston.utils.signed_requests import generate_signed_request

from v1.self_configurations.helpers.signing_key import get_signing_key


def test_accounts_list(client, accounts, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('account-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )
    assert_objects_vs_dicts(accounts, response)
    assert response


def test_accounts_patch(client, account, account_fake_data, self_configuration):
    response = client.patch_json(
        reverse(
            'account-detail',
            args=[account.account_number]
        ),
        generate_signed_request(
            data=account_fake_data,
            nid_signing_key=get_signing_key()
        ),
        expected=HTTP_200_OK,
    )
    assert response['account_number'] != account_fake_data['account_number']
    assert float(response['trust']) == account_fake_data['trust']
