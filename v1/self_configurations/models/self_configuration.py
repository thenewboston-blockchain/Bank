from django.core.exceptions import ValidationError
from django.db import models

from v1.constants.models import NODE_TYPE_CHOICES
from thenewboston.constants.nodes import BANK
from thenewboston.models.network_node import NetworkNode


class SelfConfiguration(NetworkNode):
    node_type = models.CharField(choices=NODE_TYPE_CHOICES, default=BANK, max_length=4)

    class Meta:
        default_related_name = 'self_configurations'

    def __str__(self):
        return (
            f'Node type: {self.node_type} | '
            f'Version: {self.version}'
        )

    def _validate(self, error):
        """
        Ensure only one SelfConfiguration exists
        """

        if not self.id and SelfConfiguration.objects.exists():
            raise error('Only one SelfConfiguration allowed')

    def clean(self):
        self._validate(ValidationError)

    def save(self, *args, **kwargs):
        self._validate(RuntimeError)
        super().save(*args, **kwargs)
