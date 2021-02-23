from ..models.self_configuration import SelfConfiguration


def get_self_configuration(*, exception_class):
    """Return self configuration"""
    self_configuration = SelfConfiguration.objects.first()

    if not self_configuration:
        raise exception_class('No self configuration')

    return self_configuration
