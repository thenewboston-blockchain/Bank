from django.db import models

from v1.network.models.created_modified import CreatedModified
from v1.network.models.network_transaction import NetworkTransaction

"""
created_date - Not stored on the network transaction log, stored by bank for member reference only
modified_date - Not stored on the network transaction log, stored by bank for member reference only
validated - Boolean indicating if the Tx had been validated by the primary validator

Note: If the Tx does not pass validation from the bank itself, the object is never stored in the database
"""


class BankTransaction(CreatedModified, NetworkTransaction):
    validated = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'bank_transactions'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Balance key: {self.balance_key} | '
            f'Validated: {self.validated}'
        )
