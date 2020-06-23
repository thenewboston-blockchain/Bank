from v1.self_configurations.helpers.self_configuration import get_self_configuration


def get_primary_validator():
    """
    Return primary validator
    """

    # TODO: This should be hitting the cache

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator

    if not primary_validator:
        raise RuntimeError('No primary validator')

    return primary_validator
