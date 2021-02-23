from factory import Faker
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.factories.created_modified import CreatedModifiedFactory

from ..models.account import Account


class AccountFactory(CreatedModifiedFactory):
    account_number = Faker('pystr', max_chars=VERIFY_KEY_LENGTH)

    trust = Faker(
        'pyfloat',
        left_digits=3,
        right_digits=2,
        min_value=0,
        max_value=100,
    )

    class Meta:
        model = Account
