from thenewboston.utils.fields import standard_field_names

from thenewboston_bank.banks.models.bank import Bank
from thenewboston_bank.self_configurations.helpers.self_configuration import get_self_configuration
from thenewboston_bank.validators.models.validator import Validator


def create_bank_from_config_data(*, config_data):
    """Create bank from config data"""
    fields = standard_field_names(Bank)
    data = {field: config_data[field] for field in fields if field != 'trust'}
    Bank.objects.create(**data, trust=0)


def create_validator_from_config_data(*, config_data):
    """Create validator from config data"""
    fields = standard_field_names(Validator)
    data = {field: config_data[field] for field in fields if field != 'trust'}
    Validator.objects.create(**data, trust=0)


def get_primary_validator():
    """Return primary validator"""
    # TODO: This should be hitting the cache

    self_configuration = get_self_configuration(exception_class=RuntimeError)
    primary_validator = self_configuration.primary_validator

    if not primary_validator:
        raise RuntimeError('No primary validator')

    return primary_validator


def update_bank_from_config_data(*, bank, config_data):
    """Update bank from config data"""
    fields = standard_field_names(Bank)
    data = {field: config_data[field] for field in fields if field != 'trust'}
    Bank.objects.filter(pk=bank.pk).update(**data)


def update_validator_from_config_data(*, validator, config_data):
    """Update validator from config data"""
    fields = standard_field_names(Validator)
    data = {field: config_data[field] for field in fields if field != 'trust'}
    Validator.objects.filter(pk=validator.pk).update(**data)
