from rest_framework import status
from thenewboston.constants.network import BANK

from v1.test_tools.test_base import TestBase


class TestSelfConfiguration(TestBase):

    def test_get(self):
        """
        Get self configuration details
        """

        bank_response = self.validate_get('/config', status.HTTP_200_OK)
        bank_config = bank_response.json()

        primary_validator = bank_config['primary_validator']
        node_type = bank_config['node_type']

        self.assertIsInstance(primary_validator, dict)
        self.assertEqual(node_type, BANK)
