from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts
from thenewboston.utils.signed_requests import generate_signed_request

from thenewboston_bank.self_configurations.helpers.signing_key import get_signing_key


def test_validator_list(client, validators, django_assert_max_num_queries):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('validator-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )
    assert_objects_vs_dicts(validators, response, key='node_identifier')
    assert response


def test_validator_patch(client, validator, validator_fake_data, self_configuration):
    response = client.patch_json(
        reverse(
            'validator-detail',
            args=[validator.node_identifier]
        ),
        generate_signed_request(
            data=validator_fake_data,
            nid_signing_key=get_signing_key(),
        ),
        expected=HTTP_200_OK,
    )
    assert float(response['trust']) == validator_fake_data['trust']
