from thenewboston.constants.network import BANK, CONFIRMATION_VALIDATOR
from thenewboston.factories.network_node import NetworkNodeFactory
from thenewboston.factories.network_validator import NetworkValidatorFactory


class BankConnectionRequestFactory(NetworkNodeFactory):
    node_type = BANK


class ValidatorConnectionRequestFactory(NetworkValidatorFactory):
    node_type = CONFIRMATION_VALIDATOR
