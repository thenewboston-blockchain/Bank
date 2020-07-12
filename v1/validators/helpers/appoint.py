from v1.self_configurations.helpers.self_configuration import get_self_configuration
from .validator_configuration import get_primary_validator
from ..models.validator import Validator


def appoint_primary_validator():
    """
    Appoint the most trusted validator as the primary validator
    """

    current_primary_validator = get_primary_validator()

    most_trusted_validator = Validator.objects.filter(
        primary_validator_invalid_blocks__isnull=True
    ).order_by('-trust').first()

    if current_primary_validator == most_trusted_validator:
        return

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    self_configuration.primary_validator = most_trusted_validator
    self_configuration.save()
