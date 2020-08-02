from factory import Faker

from ..models.validator import Validator
from .network_validator import NetworkValidatorFactory


class ValidatorFactory(NetworkValidatorFactory):
    trust = Faker('pydecimal', left_digits=3, right_digits=2)

    class Meta:
        model = Validator
