from django.db import models
from thenewboston.models.confirmation_service import ConfirmationService

from thenewboston_bank.validators.models.validator import Validator


class ValidatorConfirmationService(ConfirmationService):
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'validator_confirmation_services'

    def __str__(self):
        return (
            f'ID: {self.id} | '
            f'{self.start} - {self.end}'
        )
