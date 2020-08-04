from factory import Faker
from thenewboston.constants.network import VERIFY_KEY_LENGTH

from v1.blocks.factories.created_modified import CreatedModifiedFactory
from ..models.account import Account


class AccountFactory(CreatedModifiedFactory):
    account_number = Faker('text', max_nb_chars=VERIFY_KEY_LENGTH)

    trust = Faker(
        'pyfloat',
        left_digits=3,
        right_digits=2,
        min_value=0,
        max_value=100,
    )

    class Meta:
        model = Account
