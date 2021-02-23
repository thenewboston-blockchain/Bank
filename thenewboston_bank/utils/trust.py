def calculate_weighted_trust(*, node, node_list):
    """Calculate the weighted trust (0-100) for the given node using the node_list"""
    total_trust = sum([node.trust for node in node_list])
    return (node.trust / total_trust) * 100


def decrease_trust(*, amount, node):
    """Decrease trust of the given node"""
    current_trust = node.trust
    updated_trust = current_trust - amount
    node.trust = max([updated_trust, 0])
    node.save()
