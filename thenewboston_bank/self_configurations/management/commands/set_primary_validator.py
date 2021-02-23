from django.db.models import Q
from thenewboston.base_classes.fetch_primary_validator_config import FetchPrimaryValidatorConfig
from thenewboston.utils.fields import standard_field_names

from thenewboston_bank.connection_requests.helpers.connect import set_primary_validator
from thenewboston_bank.validators.models.validator import Validator

"""
python3 manage.py set_primary_validator

Running this script will:
- fetch config data from primary validator
- create a Validator instance using config data
- set that Validator as this nodes primary validator
- connect to the primary validator
"""


class Command(FetchPrimaryValidatorConfig):
    help = 'Set primary validator'  # noqa: A003

    def handle_primary_validator_config(self, primary_validator_config):
        """Set primary validator"""
        validator_field_names = standard_field_names(Validator)
        validator_data = {k: v for k, v in primary_validator_config.items() if k in validator_field_names}

        Validator.objects.filter(
            Q(ip_address=validator_data.get('ip_address'))
            | Q(node_identifier=validator_data.get('node_identifier'))
        ).delete()

        validator = Validator.objects.create(
            **validator_data,
            trust=self.required_input['trust']
        )

        set_primary_validator(validator=validator)
