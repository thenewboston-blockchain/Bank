from django.db import models
from thenewboston.constants.network import VERIFY_KEY_LENGTH
from thenewboston.models.network_registration import NetworkRegistration

from v1.accounts.models.account import Account


class AccountRegistration(NetworkRegistration):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH)

    class Meta:
        default_related_name = 'account_registrations'

    def __str__(self):
        return (
            f'Account number: {self.account_number} | '
            f'Status: {self.status}'
        )
