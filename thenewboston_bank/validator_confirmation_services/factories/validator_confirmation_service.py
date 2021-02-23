from factory import SubFactory
from thenewboston.factories.confirmation_service import ConfirmationServiceFactory

from thenewboston_bank.validators.factories.validator import ValidatorFactory
from ..models.validator_confirmation_service import ValidatorConfirmationService


class ValidatorConfirmationServiceFactory(ConfirmationServiceFactory):
    validator = SubFactory(ValidatorFactory)

    class Meta:
        model = ValidatorConfirmationService
