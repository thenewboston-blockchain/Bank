from factory import SubFactory

from v1.validators.factories.validator import ValidatorFactory
from .confirmation_service import ConfirmationServiceFactory
from ..models.validator_confirmation_service import ValidatorConfirmationService


class ValidatorConfirmationServiceFactory(ConfirmationServiceFactory):
    validator = SubFactory(ValidatorFactory)

    class Meta:
        model = ValidatorConfirmationService
