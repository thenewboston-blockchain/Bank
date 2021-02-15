from factory import Iterator, SubFactory
from thenewboston.constants.network import ACCEPTED_FEE_LIST
from thenewboston.factories.network_transaction import NetworkTransactionFactory

from v1.blocks.factories.block import BlockFactory
from ..models.bank_transaction import BankTransaction


class BankTransactionFactory(NetworkTransactionFactory):
    block = SubFactory(BlockFactory)
    # Will remove when thenewboston-python lib is updated
    fee = Iterator(ACCEPTED_FEE_LIST + [''])

    class Meta:
        model = BankTransaction
