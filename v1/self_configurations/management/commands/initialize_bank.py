from thenewboston.base_classes.initialize_node import InitializeNode
from thenewboston.constants.network import BANK

from v1.banks.models.bank import Bank
from v1.self_configurations.models.self_configuration import SelfConfiguration

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
    help = 'Initialize bank'

    def __init__(self):
        super().__init__()

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
        """
        Run script
        """

        # Input values
        self.get_verify_key(
            attribute_name='node_identifier',
            human_readable_name='node identifier'
        )
        self.get_verify_key(
            attribute_name='account_number',
            human_readable_name='account number'
        )
        self.get_fee(
            attribute_name='default_transaction_fee',
            human_readable_name='default transaction fee'
        )
        self.get_protocol()
        self.get_ip_address()
        self.get_port()
        self.get_version_number()

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
