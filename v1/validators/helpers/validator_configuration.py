def get_primary_validator_configuration():
    """
    Return current primary validator configuration details
    """

    # TODO: Connect to actual validator
    # TODO: Read validator Tx from cache

    return {
        'identifier': 'validator123',
        'node_type': 'VALIDATOR',
        'registration_fee': '64.0000000000000000',
        'transaction_fee': '8.0000000000000000',
        'version': 'v1.0'
    }
