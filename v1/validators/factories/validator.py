from factory import Faker

from .network_validator import NetworkValidatorFactory
from ..models.validator import Validator


class ValidatorFactory(NetworkValidatorFactory):
    trust = Faker('pydecimal', left_digits=3, right_digits=2)

    class Meta:
        model = Validator
