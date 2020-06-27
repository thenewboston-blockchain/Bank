from django.db.models import Q
from thenewboston.base_classes.connect_to_primary_validator import ConnectToPrimaryValidator
from thenewboston.utils.fields import standard_field_names

from v1.self_configurations.models.self_configuration import SelfConfiguration
from v1.validators.models.validator import Validator

"""
python3 manage.py connect_to_primary_validator

Running this script will:
- connect to Validator and download config
- create a Validator object using config data
- set that Validator as the primary validator
"""


class Command(ConnectToPrimaryValidator):
    help = 'Connect to primary validator'

    def set_primary_validator(self, validator_config):
        """
        Set primary validator
        """

        validator_field_names = standard_field_names(Validator)
        validator_data = {k: v for k, v in validator_config.items() if k in validator_field_names}

        Validator.objects.filter(
            Q(ip_address=validator_data.get('ip_address')) |
            Q(node_identifier=validator_data.get('node_identifier'))
        ).delete()

        validator = Validator.objects.create(
            **validator_data,
            trust=self.required_input['trust']
        )
        self_configuration = SelfConfiguration.objects.first()
        self_configuration.primary_validator = validator
        self_configuration.save()
