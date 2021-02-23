from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from thenewboston.utils.signed_requests import generate_signed_request


def set_primary_validator(client, self_configuration, signing_key, status):

    return client.post_json(
        reverse('upgrade_notice-list'),
        generate_signed_request(
            data={
                'bank_node_identifier': self_configuration.node_identifier
            },
            nid_signing_key=signing_key
        ),
        expected=status
    )


def test_upgrade_notice_200(client, self_configuration, validator, signing_key, celery_worker):
    validator.trust = self_configuration.primary_validator.trust + 1
    validator.save()

    assert set_primary_validator(client, self_configuration, signing_key, HTTP_200_OK) == {}


def test_upgrade_notice_200_same_validator(client, self_configuration, validator, signing_key, celery_worker):
    validator.trust = self_configuration.primary_validator.trust + 1
    validator.save()

    set_primary_validator(client, self_configuration, signing_key, HTTP_200_OK)
    set_primary_validator(client, self_configuration, signing_key, HTTP_200_OK)


def test_upgrade_notice_400_low_trust(client, self_configuration, validator, signing_key, celery_worker):
    validator.trust = self_configuration.primary_validator.trust - 1
    validator.save()

    response = set_primary_validator(client, self_configuration, signing_key, HTTP_400_BAD_REQUEST)
    assert response == ['Networks out of sync']
