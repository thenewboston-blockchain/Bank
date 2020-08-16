from factory.fuzzy import FuzzyChoice
from thenewboston.constants.network import BANK, CONFIRMATION_VALIDATOR, PRIMARY_VALIDATOR
from thenewboston.factories.network_node import NetworkNodeFactory


class ConnectionRequestFactory(NetworkNodeFactory):
    node_type = FuzzyChoice([BANK, CONFIRMATION_VALIDATOR, PRIMARY_VALIDATOR])
