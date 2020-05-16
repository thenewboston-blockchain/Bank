from ..models.self_configuration import SelfConfiguration


def get_self_configuration():
    """
    Return self configuration
    """

    self_configuration = SelfConfiguration.objects.first()

    if not self_configuration:
        raise RuntimeError('No self configuration')

    return self_configuration
