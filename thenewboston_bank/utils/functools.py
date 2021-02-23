import functools


def rgetattr(obj, attr, *args):
    """
    Applies a dotted attribute string to given object and returns the value

    obj - Python object (ex: 'BankTransaction | ID: 1')
    attr - dotted attribute string (ex: 'block.sender')
    """

    def _getattr(_obj, _attr):
        return getattr(_obj, _attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))
