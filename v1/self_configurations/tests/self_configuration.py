from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from thenewboston.constants.network import BANK


def test_self_configuration_get(client, self_configuration):
    response = client.get_json(
        reverse('config-list'),
        expected=HTTP_200_OK,
    )

    primary_validator = response['primary_validator']
    node_type = response['node_type']

    assert isinstance(primary_validator, dict)
    assert node_type == BANK
