from django.contrib.auth import get_user_model
from django.core import management
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata
from django.core.validators import validate_ipv46_address

from config.helpers.environment import ENVIRONMENT
from thenewboston_bank.accounts.models.account import Account
from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.self_configurations.models.self_configuration import SelfConfiguration
from thenewboston_bank.validators.models.validator import Validator

"""
python3 manage.py initialize_test_bank -ip [IP ADDRESS]

Running this script will:
- delete all Accounts, Banks, SelfConfigurations, Users, and Validators
- load in fixture data (same models as above)
- rebuild cache

Default superuser is:
username: bucky
password: pass1234
"""

User = get_user_model()


class Command(BaseCommand):
    help = 'Delete existing data, load in fixture data, and rebuild cache'  # noqa: A003

    def add_arguments(self, parser):
        """
        Required arguments:

        -ip_address - Public IP address
        """
        parser.add_argument('-ip', help='Public IP address', required=True)

    def handle(self, *args, **options):
        """Run script"""
        valid_environments = ['local', 'postgres_local']

        if ENVIRONMENT not in valid_environments:
            raise RuntimeError(f'DJANGO_APPLICATION_ENVIRONMENT must be in {valid_environments}')

        ip = options['ip']
        validate_ipv46_address(ip)

        self.install_fixture_data()

        self_configuration = get_self_configuration(exception_class=RuntimeError)
        SelfConfiguration.objects.filter(pk=self_configuration.id).update(ip_address=ip)
        cache.clear()

        self.stdout.write(self.style.SUCCESS('Bank initialization complete'))

    def install_fixture_data(self):
        """
        Delete all Accounts, Banks, SelfConfigurations, Users, and Validators

        Load in fixture data (same models as above)
        """
        self.stdout.write(self.style.SUCCESS('Installing fixture data...'))

        Account.objects.all().delete()
        Bank.objects.all().delete()
        SelfConfiguration.objects.all().delete()
        User.objects.all().delete()
        Validator.objects.all().delete()

        fixtures = [
            'validator',
            'self_configuration',
            'user'
        ]

        management.call_command(loaddata.Command(), *fixtures, verbosity=1)

        self.stdout.write(self.style.SUCCESS('Fixture data installed successfully'))
