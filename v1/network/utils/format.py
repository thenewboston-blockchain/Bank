def format_node_address(node):
    """
    Format address for node
    """

    ip_address = node.ip_address
    port = f':{node.port}' if node.port else ''
    protocol = node.protocol
    return f'{protocol}://{ip_address}{port}/'
