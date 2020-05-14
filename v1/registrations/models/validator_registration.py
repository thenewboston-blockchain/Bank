from django.db import models

from v1.validators.models.validator import Validator
from .registration import Registration


class ValidatorRegistration(Registration):
    validator = models.ForeignKey(Validator, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'validator_registrations'

    def __str__(self):
        return f'{self.id} | {self.status}'
