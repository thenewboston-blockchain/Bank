from django.db import models
from thenewboston.models.network_registration import NetworkRegistration

from v1.validators.models.validator import Validator


class BankRegistration(NetworkRegistration):
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bank_registrations'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Validator IP: {self.validator.ip_address} | '
            f'Fee: {self.fee} | '
            f'Status: {self.status}'
        )
