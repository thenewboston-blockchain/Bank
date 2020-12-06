import random
from datetime import datetime, timedelta

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from thenewboston.third_party.pytest.asserts import assert_objects_vs_dicts
from thenewboston.utils.signed_requests import generate_signed_request


def test_validator_confirmation_service_list(
    client, validator_confirmation_services, django_assert_max_num_queries,
):
    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('validatorconfirmationservice-list'),
            {'limit': 0},
            expected=HTTP_200_OK,
        )
    assert_objects_vs_dicts(validator_confirmation_services, response)
    assert response


def test_validator_confirmation_service_filter(
    client, validator_confirmation_services, django_assert_max_num_queries,
):
    validator_confirmation_service = random.choice(validator_confirmation_services)

    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('validatorconfirmationservice-list'),
            {
                'limit': 0,
                'validator__node_identifier': validator_confirmation_service.validator.node_identifier,
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(validator_confirmation_service.id)


def test_validator_confirmation_service_post_async(
    client, django_assert_max_num_queries, validator, signing_key
):
    start = datetime.now().isoformat()
    end = (datetime.now() + timedelta(days=2)).isoformat()

    payload = generate_signed_request(
        data={
            'start': start,
            'end': end
        },
        nid_signing_key=signing_key
    )
    with django_assert_max_num_queries(2):
        response = client.post_json(
            reverse('validatorconfirmationservice-list'),
            payload,
            expected=HTTP_201_CREATED
        )

    assert response['end'][:-1] == end
    assert response['start'][:-1] == start
    assert response['validator'] == str(validator.pk)
