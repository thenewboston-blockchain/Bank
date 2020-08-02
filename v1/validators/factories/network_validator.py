from factory import Faker
from thenewboston.constants.network import ACCOUNT_FILE_HASH_LENGTH, BLOCK_IDENTIFIER_LENGTH
from thenewboston.models.network_validator import NetworkValidator

from .network_node import NetworkNodeFactory


class NetworkValidatorFactory(NetworkNodeFactory):
    daily_confirmation_rate = Faker('pydecimal', left_digits=16, right_digits=16)

    root_account_file = Faker('url')
    root_account_file_hash = Faker('text', max_nb_chars=ACCOUNT_FILE_HASH_LENGTH)

    seed_block_identifier = Faker('text', max_nb_chars=BLOCK_IDENTIFIER_LENGTH)

    class Meta:
        model = NetworkValidator
        abstract = True
