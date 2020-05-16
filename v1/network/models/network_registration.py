from django.core.validators import MinValueValidator
from django.db import models

from ..constants.models import PENDING, REGISTRATION_STATUS_CHOICES
from ..models.created_modified import CreatedModified
from ..utls.validators import validate_is_real_number


class NetworkRegistration(CreatedModified):
    fee = models.DecimalField(
        decimal_places=16,
        default=0,
        max_digits=32,
        validators=[
            MinValueValidator(0),
            validate_is_real_number
        ]
    )
    status = models.CharField(choices=REGISTRATION_STATUS_CHOICES, default=PENDING, max_length=8)

    class Meta:
        abstract = True
