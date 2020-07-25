from factory import SubFactory

from v1.blocks.factories.block import BlockFactory
from .network_transaction import NetworkTransactionFactory
from ..models.bank_transaction import BankTransaction


class BankTransactionFactory(NetworkTransactionFactory):

    class Meta:
        model = BankTransaction

    block = SubFactory(BlockFactory)
