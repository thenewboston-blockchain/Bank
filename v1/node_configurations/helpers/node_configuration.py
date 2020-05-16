from ..models.node_configuration import NodeConfiguration


def get_node_configuration():
    """
    Return current node configuration details
    """

    return NodeConfiguration.objects.first()
