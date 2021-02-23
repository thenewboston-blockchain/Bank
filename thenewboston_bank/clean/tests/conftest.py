import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def bank_configuration(self_configuration):
    pass


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
