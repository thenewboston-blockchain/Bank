from factory import Faker
from thenewboston.constants.network import BALANCE_LOCK_LENGTH, SIGNATURE_LENGTH, VERIFY_KEY_LENGTH
from thenewboston.factories.created_modified import CreatedModifiedFactory

from ..models.block import Block


class BlockFactory(CreatedModifiedFactory):
    balance_key = Faker('text', max_nb_chars=BALANCE_LOCK_LENGTH)
    sender = Faker('text', max_nb_chars=VERIFY_KEY_LENGTH)
    signature = Faker('text', max_nb_chars=SIGNATURE_LENGTH)

    class Meta:
        model = Block
