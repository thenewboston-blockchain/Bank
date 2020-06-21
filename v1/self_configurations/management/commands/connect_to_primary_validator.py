import logging

from django.core.exceptions import ValidationError
from django.db.models import Q
from thenewboston.base_classes.initialize_node import InitializeNode
from thenewboston.constants.network import VALIDATOR
from thenewboston.utils.fields import standard_field_names
from thenewboston.utils.format import format_address
from thenewboston.utils.network import fetch
from thenewboston.utils.validators import validate_is_real_number

from v1.self_configurations.models.self_configuration import SelfConfiguration
from v1.validators.models.validator import Validator

"""
python3 manage.py connect_to_primary_validator

Running this script will:
- connect to Validator and download config
- create a Validator object using config data
- set that Validator as the primary validator
"""

logger = logging.getLogger('thenewboston')


class Command(InitializeNode):
    help = 'Connect to primary validator'

    def __init__(self):
        super().__init__()

        self.required_input = {
            'ip_address': None,
            'port': None,
            'protocol': None,
            'trust': None
        }

    def get_trust(self):
        """
        Get trust from user
        """

        valid = False

        while not valid:
            trust = input('Enter trust (required): ')

            if not trust:
                self._error('trust required')
                continue

            is_valid_decimal, trust = self.validate_and_convert_to_decimal(trust)

            if not is_valid_decimal:
                continue

            try:
                validate_is_real_number(trust)
            except ValidationError:
                self._error('Value must be a real number')
                continue

            if trust < 0:
                self._error(f'Value can not be less than 0')
                continue

            if trust > 100:
                self._error(f'Value can not be greater than 100')
                continue

            self.required_input['trust'] = trust
            valid = True

    def get_validator_config(self):
        """
        Return config
        """

        address = format_address(
            ip_address=self.required_input['ip_address'],
            port=self.required_input['port'],
            protocol=self.required_input['protocol']
        )
        url = f'{address}/config'
        results = fetch(url=url, headers={})
        return results

    def handle(self, *args, **options):
        """
        Run script
        """

        connected = False

        while not connected:
            self.required_input = {
                'ip_address': None,
                'port': None,
                'protocol': None
            }

            self.get_ip_address()
            self.get_protocol()
            self.get_port()

            try:
                config = self.get_validator_config()

                if not self.is_config_valid(config):
                    continue

                self.get_trust()
                self.set_primary_validator(config)
            except Exception as e:
                self._error('Unable to connect')
                logger.exception(e)
                continue

            connected = True

        self.stdout.write(self.style.SUCCESS('Connection to primary validator established'))

    def is_config_valid(self, config):
        """
        Validate config response data from the validator
        """

        if config.get('node_type') != VALIDATOR:
            self._error(f'node_type is not {VALIDATOR}')
            return False

        primary_validator = config.get('primary_validator')

        if (
            (not primary_validator) or
            (config.get('ip_address') != primary_validator.get('ip_address')) or
            (config.get('port') != primary_validator.get('port')) or
            (config.get('protocol') != primary_validator.get('protocol'))
        ):
            self._error('Validator not set as primary validator')
            return False

        return True

    def set_primary_validator(self, validator_config):
        """
        Set primary validator
        """

        validator_field_names = standard_field_names(Validator)
        validator_data = {k: v for k, v in validator_config.items() if k in validator_field_names}

        Validator.objects.filter(
            Q(ip_address=validator_data.get('ip_address')) |
            Q(network_identifier=validator_data.get('network_identifier'))
        ).delete()

        validator = Validator.objects.create(
            **validator_data,
            trust=self.required_input['trust']
        )
        self_configuration = SelfConfiguration.objects.first()
        self_configuration.primary_validator = validator
        self_configuration.save()
