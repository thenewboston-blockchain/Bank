from thenewboston.base_classes.initialize_node import InitializeNode
from thenewboston.constants.network import BANK

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.self_configurations.models.self_configuration import SelfConfiguration

"""
python3 manage.py initialize_bank

Prerequisites:
- python3 manage.py makemigrations
- python3 manage.py migrate
- python3 manage.py createsuperuser (optional)

Running this script will:
- delete existing SelfConfiguration and related Bank objects
- create SelfConfiguration and related Bank objects
"""


class Command(InitializeNode):
    help = 'Initialize bank'  # noqa: A003

    def __init__(self, *args, **kwargs):
        """Initialize bank"""
        super().__init__(*args, **kwargs)

        self.required_input = {
            'account_number': None,
            'default_transaction_fee': None,
            'ip_address': None,
            'node_identifier': None,
            'port': None,
            'protocol': None,
            'version': None
        }

    def handle(self, *args, **options):
        """Run script"""
        # Input values
        self.get_verify_key(
            attribute_name='node_identifier',
            human_readable_name='node identifier',
            value=options.get('node_identifier')
        )
        self.get_verify_key(
            attribute_name='account_number',
            human_readable_name='account number',
            value=options.get('account_number')
        )
        self.get_fee(
            attribute_name='default_transaction_fee',
            human_readable_name='default transaction fee',
            value=options.get('default_transaction_fee')
        )
        self.get_protocol(value=options.get('protocol'))
        self.get_ip_address(value=options.get('ip_address'))
        self.get_port(value=options.get('port'))
        self.get_version_number(value=options.get('version_number'))

        self.initialize_bank()

    def initialize_bank(self):
        """
        Process to initialize bank:

        - delete existing SelfConfiguration and related Bank objects
        - create SelfConfiguration and related Bank objects
        """
        # Delete existing SelfConfiguration and related Bank objects
        SelfConfiguration.objects.all().delete()
        Bank.objects.filter(ip_address=self.required_input['ip_address']).delete()

        # Create SelfConfiguration and related Bank objects
        SelfConfiguration.objects.create(
            **self.required_input,
            node_type=BANK
        )

        self.stdout.write(self.style.SUCCESS('Bank initialization complete'))
