from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from thenewboston.environment.environment_variables import get_environment_variable


def get_signing_key():
    """
    Return signing key
    """

    network_signing_key = get_environment_variable('NETWORK_SIGNING_KEY')
    return SigningKey(network_signing_key, encoder=HexEncoder)
