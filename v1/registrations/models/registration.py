from django.core.validators import MinValueValidator
from django.db import models

from v1.constants.models import PENDING, REGISTRATION_STATUS_CHOICES
from v1.general.models.created_modified import CreatedModified
from v1.utils.validators import validate_is_real_number


class Registration(CreatedModified):
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
