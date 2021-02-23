from factory import Faker
from thenewboston.factories.network_validator import NetworkValidatorFactory

from ..models.validator import Validator


class ValidatorFactory(NetworkValidatorFactory):
    trust = Faker('pyfloat', left_digits=3, right_digits=2, min_value=0, max_value=100)

    class Meta:
        model = Validator
