import random

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK


def test_validator_confirmation_service_filter(
    client, validator_confirmation_services, django_assert_max_num_queries,
):
    validator_confirmation_service = random.choice(validator_confirmation_services)

    with django_assert_max_num_queries(2):
        response = client.get_json(
            reverse('validator_confirmation_services:validatorconfirmationservice-list'),
            {
                'limit': 0,
                'validator__node_identifier': validator_confirmation_service.validator.node_identifier,
            },
            expected=HTTP_200_OK,
        )
    assert response[0]['id'] == str(validator_confirmation_service.id)
