from ..models.validator import Validator


def get_primary_validator():
    """
    Return primary validator
    """

    # TODO: Connect to actual validator
    # TODO: Read validator Tx from cache

    primary_validator = Validator.objects.filter(primary=True).first()

    if not primary_validator:
        raise RuntimeError('No primary validator')

    return primary_validator
