from django.db import models

from v1.validators.models.validator import Validator
from .registration import Registration


class BankRegistration(Registration):
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'bank_registrations'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'Validator IP: {self.validator.ip_address} | '
            f'Status: {self.status}'
        )
