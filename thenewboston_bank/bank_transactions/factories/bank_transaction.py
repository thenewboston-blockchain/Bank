from factory import SubFactory
from thenewboston.factories.network_transaction import NetworkTransactionFactory

from thenewboston_bank.blocks.factories.block import BlockFactory
from ..models.bank_transaction import BankTransaction


class BankTransactionFactory(NetworkTransactionFactory):
    block = SubFactory(BlockFactory)

    class Meta:
        model = BankTransaction
