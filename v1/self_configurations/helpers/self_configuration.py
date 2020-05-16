from ..models.self_configuration import SelfConfiguration


def get_self_configuration():
    """
    Return self configuration details
    """

    return SelfConfiguration.objects.first()
