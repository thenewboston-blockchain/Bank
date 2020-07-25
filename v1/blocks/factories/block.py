from factory import Faker
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.constants.network import BALANCE_LOCK_LENGTH
from thenewboston.constants.network import SIGNATURE_LENGTH

from v1.blocks.models.block import Block
from .created_modified import CreatedModifiedFactory


class BlockFactory(CreatedModifiedFactory):

    class Meta:
        model = Block

    balance_key = Faker('text', max_nb_chars=BALANCE_LOCK_LENGTH)
    sender = Faker('text', max_nb_chars=VERIFY_KEY_LENGTH)
    signature = Faker('text', max_nb_chars=SIGNATURE_LENGTH)
