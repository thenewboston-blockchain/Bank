import factory


def build_batch_json(klass, size, **kwargs):
    """
    Build json representation for objects batch using factory.
    """
    return factory.build_batch(
        dict,
        size,
        FACTORY_CLASS=klass,
        **kwargs,
    )


def build_json(klass, **kwargs):
    """
    Build json representation for object using factory.
    """
    return factory.build(
        dict,
        FACTORY_CLASS=klass,
        **kwargs,
    )
