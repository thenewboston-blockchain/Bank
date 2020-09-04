from thenewboston.utils.fields import standard_field_names

from v1.self_configurations.helpers.self_configuration import get_self_configuration
from v1.validators.models.validator import Validator


def create_validator_from_config_data(*, config_data):
    """
    Create validator from config data
    """

    fields = standard_field_names(Validator)
    data = {field: config_data[field] for field in fields if field != 'trust'}
    validator = Validator.objects.create(**data, trust=0)
    return validator


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
