from django.db import models
from thenewboston.models.network_transaction import NetworkTransaction

from thenewboston_bank.blocks.models.block import Block


class BankTransaction(NetworkTransaction):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bank_transactions'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Amount: {self.amount} | '
            f'Recipient: {self.recipient} | '
            f'Fee: {self.fee or "-"}'
        )
