import pytest
from django.conf import settings
from django.core.management import call_command
from factory import Faker
from pytest_django.migrations import DisableMigrations
from thenewboston.accounts.manage import create_account
from thenewboston.blocks.block import generate_block
from thenewboston.third_party.pytest.client import UserWrapper
from thenewboston.verify_keys.verify_key import encode_verify_key

from v1.accounts.factories.account import AccountFactory
from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.utils.blocks import create_block_and_bank_transactions
from v1.validators.factories.validator import ValidatorFactory


@pytest.fixture
def account(encoded_account_number):
    yield AccountFactory(account_number=encoded_account_number)


@pytest.fixture
def account_data():
    yield create_account()


@pytest.fixture
def account_number(account_data):
    signing_key, account_number = account_data
    yield account_number


@pytest.fixture
def block(block_data):
    yield create_block_and_bank_transactions(block_data)


@pytest.fixture
def block_data(account_data, account, encoded_account_number, random_encoded_account_number, self_configuration):
    signing_key, account_number = account_data
    primary_validator = self_configuration.primary_validator

    yield generate_block(
        account_number=account_number,
        balance_lock=encoded_account_number,
        signing_key=signing_key,
        transactions=[
            {
                'amount': self_configuration.default_transaction_fee,
                'recipient': self_configuration.account_number
            },
            {
                'amount': primary_validator.default_transaction_fee,
                'recipient': primary_validator.account_number
            },
            {
                'amount': Faker('pyint').generate(),
                'recipient': random_encoded_account_number
            }
        ]
    )


@pytest.fixture
def client():
    yield UserWrapper(None)


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def encoded_account_number(account_number):
    yield encode_verify_key(verify_key=account_number)


@pytest.fixture(scope='session', autouse=True)
def migrations_disabled():
    settings.MIGRATION_MODULES = DisableMigrations()
    yield None


@pytest.fixture
def no_requests(monkeypatch):
    monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def random_encoded_account_number():
    _, account_number = create_account()
    yield encode_verify_key(verify_key=account_number)


@pytest.fixture
def signing_key(account_data):
    key, account_number = account_data
    yield key


@pytest.fixture
def self_configuration(monkeypatch):
    call_command('loaddata', 'validator', 'self_configuration', 'user')
    monkeypatch.setenv('NETWORK_SIGNING_KEY', 'e5e5fec0dcbbd8b0a76c67204823678d3f243de7a0a1042bb3ecf66285cd9fd4')
    yield get_self_configuration(exception_class=RuntimeError)


@pytest.fixture(autouse=True)
def use_fake_redis(settings):
    """
    Using fake Redis for running tests in parallel.
    """

    settings.DJANGO_REDIS_CONNECTION_FACTORY = 'thenewboston.third_party.django_redis.pool.FakeConnectionFactory'
    settings.CACHES['default']['OPTIONS']['REDIS_CLIENT_CLASS'] = 'fakeredis.FakeStrictRedis'


@pytest.fixture
def validator(encoded_account_number):
    yield ValidatorFactory(node_identifier=encoded_account_number)
