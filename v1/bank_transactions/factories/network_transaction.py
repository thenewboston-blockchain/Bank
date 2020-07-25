from factory import DjangoModelFactory, Faker
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.models.network_transaction import NetworkTransaction


class NetworkTransactionFactory(DjangoModelFactory):

    class Meta:
        model = NetworkTransaction

    amount = Faker(
        'pydecimal',
        left_digits=16,
        right_digits=16,
    )
    recipient = Faker(
        'text',
        max_nb_chars=VERIFY_KEY_LENGTH,
    )
