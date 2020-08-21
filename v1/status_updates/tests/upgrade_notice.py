from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.utils.signed_requests import generate_signed_request


def test_upgrade_notice_post(client, self_configuration, validator, signing_key):
    validator.trust = self_configuration.primary_validator.trust + 1
    validator.save()

    client.post_json(
        reverse('upgrade_notice-list'),
        generate_signed_request(
            data={
                'bank_node_identifier': self_configuration.node_identifier
            },
            nid_signing_key=signing_key
        ),
        expected=HTTP_200_OK
    )
