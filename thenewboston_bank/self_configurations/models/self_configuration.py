from django.core.exceptions import ValidationError
from django.db import models
from thenewboston.constants.network import BANK
from thenewboston.models.network_node import NetworkNode
from thenewboston.utils.fields import common_field_names

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.constants.models import NODE_TYPE_CHOICES
from thenewboston_bank.validators.models.validator import Validator


class SelfConfiguration(NetworkNode):
    primary_validator = models.ForeignKey(Validator, on_delete=models.SET_NULL, blank=True, null=True)
    node_type = models.CharField(choices=NODE_TYPE_CHOICES, default=BANK, max_length=4)

    class Meta(NetworkNode.Meta):
        default_related_name = 'self_configurations'

    def __str__(self):
        return (
            f'Node type: {self.node_type} | '
            f'Version: {self.version}'
        )

    def _update_related_bank(self):
        """Update related row in the bank table"""
        bank = Bank.objects.filter(ip_address=self.ip_address, protocol=self.protocol, port=self.port)
        field_names = common_field_names(self, Bank)
        data = {f: getattr(self, f) for f in field_names}

        if bank:
            bank.update(**data)
        else:
            Bank.objects.create(**data, trust=100)

    def _validate(self, error):
        """Ensure only one SelfConfiguration exists"""
        if not self.id and SelfConfiguration.objects.exists():
            raise error('Only one SelfConfiguration allowed')

    def clean(self):
        self._validate(ValidationError)

    def save(self, *args, **kwargs):
        self._validate(RuntimeError)
        super().save(*args, **kwargs)
        self._update_related_bank()
